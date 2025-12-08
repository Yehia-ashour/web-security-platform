# scanning/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TestProfileViewSet, ScanViewSet, VulnerabilityViewSet # تم إضافة استيراد الواجهتين الجديدتين

router = DefaultRouter()
# مسار ملفات الاختبار
router.register(r'profiles', TestProfileViewSet) 
# مسار عمليات المسح
router.register(r'scans', ScanViewSet, basename='scan') # تم إضافة هذا
# مسار الثغرات
router.register(r'vulnerabilities', VulnerabilityViewSet, basename='vulnerability') # تم إضافة هذا


urlpatterns = [
    path('', include(router.urls)),
]