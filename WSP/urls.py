# project_name/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView, 
    TokenRefreshView,     
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # مسارات المصادقة (Login)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), 
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # ------------------ ربط مسارات تطبيق SCANNING ------------------
    # يتم الوصول إلى كل المسارات في scanning/urls.py عبر /api/scanning/
    path('api/scanning/', include('scanning.urls')), 
    # -----------------------------------------------------------------
]