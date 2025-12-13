# scanning/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TestProfileViewSet, ScanViewSet, VulnerabilityViewSet

router = DefaultRouter()

router.register(r'profiles', TestProfileViewSet) 

router.register(r'scans', ScanViewSet, basename='scan') 

router.register(r'vulnerabilities', VulnerabilityViewSet, basename='vulnerability') 


urlpatterns = [
    path('', include(router.urls)),
]