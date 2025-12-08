# users/permissions.py
from rest_framework import permissions

# ----------------------------------------------------
# 1. صلاحية مختبر الأمن أو المسؤول (Security Tester or Admin)
# لـ: إنشاء/تشغيل/جدولة الاختبارات (Create Test, Run Scan, Schedule Scan)
# ----------------------------------------------------
class IsSecurityTesterOrAdmin(permissions.BasePermission):
    """
    يسمح بالوصول للمستخدمين الذين لديهم دور 'tester' أو 'admin'.
    """
    def has_permission(self, request, view):
        # التحقق من تسجيل الدخول ودور المستخدم
        if not request.user.is_authenticated:
            return False
            
        user_role = request.user.role
        return user_role in ['tester', 'admin']

# ----------------------------------------------------
# 2. صلاحية المسؤول (System Administrator)
# لـ: إدارة المستخدمين، تهيئة محرك المسح، المراقبة (Manage Users, Configure Scan Engine, Monitor System)
# ----------------------------------------------------
class IsSystemAdmin(permissions.BasePermission):
    """
    يسمح بالوصول للمستخدمين الذين لديهم دور 'admin' فقط.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

# ----------------------------------------------------
# 3. صلاحية العميل أو المدير (Client/Manager)
# لـ: عرض النتائج، تصدير التقارير (View Results, Export Report)
# ----------------------------------------------------
class IsClientOrManager(permissions.BasePermission):
    """
    يسمح بالوصول للمستخدمين الذين لديهم دور 'client' أو 'manager'.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
            
        user_role = request.user.role
        return user_role in ['client', 'manager']