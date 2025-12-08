# scanning/views.py
from rest_framework import viewsets, status, mixins, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

# استيراد الصلاحيات المخصصة
from users.permissions import IsSecurityTesterOrAdmin, IsClientOrManager 

# استيراد النماذج والسيريالايزر
from .models import TestProfile, Scan, Vulnerability
from .serializers import TestProfileSerializer, ScanSerializer, VulnerabilitySerializer 

# استيراد مهمة Celery
from .tasks import run_security_scan 

# استيرادات جديدة لعملية التقرير (تم إضافتها)
from reporting.models import Report 
from reporting.tasks import generate_report_pdf 


# ----------------------------------------------------
# 1. TestProfile ViewSet (Create Test, Run Scan)
# ----------------------------------------------------
class TestProfileViewSet(viewsets.ModelViewSet):
    queryset = TestProfile.objects.all()
    serializer_class = TestProfileSerializer
    
    # تطبيق الصلاحية: يجب أن يكون المستخدم مختبراً أو مسؤولاً
    permission_classes = [IsSecurityTesterOrAdmin] 

    def perform_create(self, serializer):
        # قبل الحفظ، نحدد المستخدم الحالي كمنشئ للاختبار
        serializer.save(created_by=self.request.user)
        
    # وظيفة Run Scan
    # متاحة على مسار: /api/scanning/profiles/{id}/run_scan/
    @action(detail=True, methods=['post'], permission_classes=[IsSecurityTesterOrAdmin])
    def run_scan(self, request, pk=None):
        try:
            profile = self.get_object() 

            # 1. إنشاء سجل مسح جديد (Scan record) بحالة "pending"
            scan = Scan.objects.create(
                profile=profile,
                status='pending',
                scheduled_by=request.user
            )

            # 2. إرسال المهمة إلى Celery لتشغيلها في الخلفية
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

# ----------------------------------------------------
# 2. Scan ViewSet (View Results List/Detail & Export Report)
# ----------------------------------------------------
class ScanViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin):
    serializer_class = ScanSerializer
    # الصلاحية: إما مختبر/مسؤول أو عميل/مدير
    permission_classes = [IsSecurityTesterOrAdmin | IsClientOrManager] 

    def get_queryset(self):
        user = self.request.user
        
        # المختبرون والمسؤولون يرون جميع عمليات المسح
        if user.role in ['tester', 'admin']:
            return Scan.objects.all().order_by('-start_time')
        
        # العميل يرى فقط عمليات المسح المرتبطة بملفات الاختبار الخاصة به
        elif user.role == 'client':
            client_profiles = TestProfile.objects.filter(created_by=user)
            return Scan.objects.filter(profile__in=client_profiles).order_by('-start_time')
            
        # حالة أخرى (لأمان إضافي)
        return Scan.objects.none()

    # ----------------------------------------------------
    # وظيفة جديدة: Export Report (تصدير التقرير) (تم إضافتها)
    # متاحة على مسار: /api/scanning/scans/{id}/export_report/
    # ----------------------------------------------------
    @action(detail=True, methods=['post'], permission_classes=[IsSecurityTesterOrAdmin | IsClientOrManager])
    def export_report(self, request, pk=None):
        try:
            scan = self.get_object() # الحصول على سجل المسح بواسطة ID

            # 1. إنشاء سجل تقرير جديد بحالة "PENDING"
            report = Report.objects.create(
                scan=scan,
                report_type=request.data.get('report_type', 'PDF'), 
                status='PENDING'
            )

            # 2. إرسال مهمة توليد التقرير إلى Celery
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


# ----------------------------------------------------
# 3. Vulnerability ViewSet (View Vulnerability List/Detail)
# ----------------------------------------------------
class VulnerabilityViewSet(viewsets.ReadOnlyModelViewSet):
    """
    مخصصة لعرض الثغرات فقط (Read-Only) مع تصفية حسب الدور
    """
    serializer_class = VulnerabilitySerializer
    # الصلاحية: إما مختبر/مسؤول أو عميل/مدير
    permission_classes = [IsSecurityTesterOrAdmin | IsClientOrManager]

    def get_queryset(self):
        user = self.request.user
        
        # المختبرون والمسؤولون يرون جميع الثغرات
        if user.role in ['tester', 'admin']:
            return Vulnerability.objects.all()
        
        # العميل يرى فقط الثغرات المرتبطة بملفات الاختبار الخاصة به
        elif user.role == 'client':
            # تصفية الثغرات بناءً على عمليات المسح المرتبطة بملفات العميل
            client_profiles = TestProfile.objects.filter(created_by=user)
            client_scans = Scan.objects.filter(profile__in=client_profiles)
            return Vulnerability.objects.filter(scan__in=client_scans)
            
        return Vulnerability.objects.none()