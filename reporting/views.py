# reporting/views.py
from rest_framework import viewsets
from reporting.models import Report
from reporting.serializers import ReportSerializer
from users.permissions import IsSecurityTesterOrAdmin, IsClientOrManager
from scanning.models import Scan


class ReportViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only API for viewing generated reports.
    """
    serializer_class = ReportSerializer
    permission_classes = [IsSecurityTesterOrAdmin | IsClientOrManager]

    def get_queryset(self):
        user = self.request.user

        if user.role in ['tester', 'admin']:
            return Report.objects.all().order_by('-generated_at')

        elif user.role == 'client':
            client_scans = Scan.objects.filter(profile__created_by=user)
            return Report.objects.filter(scan__in=client_scans).order_by('-generated_at')

        return Report.objects.none()
