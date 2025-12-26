# reporting/urls.py
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import ReportViewSet, ScanSummaryView

router = SimpleRouter()
router.register(r'reports', ReportViewSet, basename='report')

urlpatterns = [
    path('', include(router.urls)),
    path('scans/<int:scan_id>/summary/', ScanSummaryView.as_view(), name='scan_summary'),
]
