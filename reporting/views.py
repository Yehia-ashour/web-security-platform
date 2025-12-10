from reporting.models import Report
from reporting.tasks import generate_report_pdf
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response


class ScanViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin):
    
    ...

    @action(detail=True, methods=['post'])
    def export_report(self, request, pk=None):
        try:
            scan = self.get_object()

            # Prevent generating duplicate reports
            if hasattr(scan, "report"):
                return Response(
                    {
                        "error": "Report already exists for this scan.",
                        "report_id": scan.report.id,
                        "status": scan.report.status
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Create new Report record
            report = Report.objects.create(
                scan=scan,
                report_type='PDF',
                status="PENDING"
            )

            # Run Celery task
            generate_report_pdf.delay(report.id)

            return Response(
                {
                    "message": "Report generation started.",
                    "report_id": report.id,
                    "status": "PENDING"
                },
                status=status.HTTP_202_ACCEPTED
            )

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
