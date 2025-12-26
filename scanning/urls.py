# scanning/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ScanProfileViewSet, ScanViewSet, VulnerabilityViewSet, RunScanView

router = DefaultRouter()
router.register(r'profiles', ScanProfileViewSet)
router.register(r'scans', ScanViewSet, basename='scan')
router.register(r'vulnerabilities', VulnerabilityViewSet, basename='vulnerability')

urlpatterns = [
    path('', include(router.urls)),
    path('run_scan/', RunScanView.as_view(), name='run_scan'),
]
