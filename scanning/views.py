# scanning/views.py
from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from users.permissions import IsSecurityTesterOrAdmin, IsClientOrManager 

from .models import TestProfile, Scan, Vulnerability
from .serializers import TestProfileSerializer, ScanSerializer, VulnerabilitySerializer 

from .tasks import run_security_scan 

from reporting.models import Report 
from reporting.tasks import generate_report_pdf 



class TestProfileViewSet(viewsets.ModelViewSet):
    queryset = TestProfile.objects.all()
    serializer_class = TestProfileSerializer
    
    permission_classes = [IsSecurityTesterOrAdmin] 

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
        

    @action(detail=True, methods=['post'], permission_classes=[IsSecurityTesterOrAdmin])
    def run_scan(self, request, pk=None):
        try:
            profile = self.get_object() 

            scan = Scan.objects.create(
                profile=profile,
                status='pending',
                scheduled_by=request.user
            )

            run_security_scan.delay(scan.id)
            
            return Response(
                {'status': 'Scan initiated successfully', 'scan_id': scan.id}, 
                status=status.HTTP_202_ACCEPTED 
            )

        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )


class ScanViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin):
    serializer_class = ScanSerializer
    permission_classes = [IsSecurityTesterOrAdmin | IsClientOrManager] 

    def get_queryset(self):
        user = self.request.user
        
        if user.role in ['tester', 'admin']:
            return Scan.objects.all().order_by('-start_time')
        
        elif user.role == 'client':
            client_profiles = TestProfile.objects.filter(created_by=user)
            return Scan.objects.filter(profile__in=client_profiles).order_by('-start_time')
            
        return Scan.objects.none()


    @action(detail=True, methods=['post'], permission_classes=[IsSecurityTesterOrAdmin | IsClientOrManager])
    def export_report(self, request, pk=None):
        try:
            scan = self.get_object()

            if hasattr(scan, "report"):
                return Response({
                    "error": "Report already exists for this scan.",
                    "report_id": scan.report.id,
                    "status": scan.report.status,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

            report = Report.objects.create(
                scan=scan,
                report_type=request.data.get('report_type', 'PDF'), 
                status='PENDING'
            )

            generate_report_pdf.delay(report.id)
            
            return Response(
                {'status': 'Report generation initiated. Check report status later.', 'report_id': report.id}, 
                status=status.HTTP_202_ACCEPTED
            )

        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )



class VulnerabilityViewSet(viewsets.ReadOnlyModelViewSet):
    """
    مخصصة لعرض الثغرات فقط (Read-Only) مع تصفية حسب الدور
    """
    serializer_class = VulnerabilitySerializer

    permission_classes = [IsSecurityTesterOrAdmin | IsClientOrManager]

    def get_queryset(self):
        user = self.request.user
        

        if user.role in ['tester', 'admin']:
            return Vulnerability.objects.all()
        

        elif user.role == 'client':

            client_profiles = TestProfile.objects.filter(created_by=user)
            client_scans = Scan.objects.filter(profile__in=client_profiles)
            return Vulnerability.objects.filter(scan__in=client_scans)
            
        return Vulnerability.objects.none()
    
    