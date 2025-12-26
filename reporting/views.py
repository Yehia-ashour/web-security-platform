# reporting/views.py
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from reporting.models import Report
from reporting.serializers import ReportSerializer
from users.permissions import IsSecurityTesterOrAdmin, IsClientOrManager
from scanning.models import Scan, Vulnerability
from scanning.serializers import ScanSerializer, VulnerabilitySerializer


class ReportViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only API for viewing generated reports.
    """
    serializer_class = ReportSerializer
    permission_classes = [IsSecurityTesterOrAdmin | IsClientOrManager]

    def get_queryset(self):
        return Report.objects.all().order_by('-generated_at')


class ScanSummaryView(APIView):
    permission_classes = [IsSecurityTesterOrAdmin | IsClientOrManager]

    def get(self, request, scan_id):
        try:
            scan = Scan.objects.get(id=scan_id)
            vulnerabilities = Vulnerability.objects.filter(scan=scan)

            scan_serializer = ScanSerializer(scan)
            vulnerabilities_serializer = VulnerabilitySerializer(vulnerabilities, many=True)

            summary = {
                'scan': scan_serializer.data,
                'vulnerabilities': vulnerabilities_serializer.data,
                'total_vulnerabilities': len(vulnerabilities),
                'high_risk_count': sum(1 for v in vulnerabilities if v.risk == 'High'),
                'medium_risk_count': sum(1 for v in vulnerabilities if v.risk == 'Medium'),
                'low_risk_count': sum(1 for v in vulnerabilities if v.risk == 'Low'),
                'info_count': sum(1 for v in vulnerabilities if v.risk == 'Informational'),
            }

            return Response(summary)
        except Scan.DoesNotExist:
            return Response({'error': 'Scan not found'}, status=404)
