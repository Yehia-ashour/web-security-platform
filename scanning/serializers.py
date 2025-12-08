# scanning/serializers.py
from rest_framework import serializers
from .models import TestProfile, Scan, Vulnerability # استيراد جميع النماذج

# ----------------------------------------------------
# 1. TestProfile Serializer (لـ Create Test API)
# ----------------------------------------------------
class TestProfileSerializer(serializers.ModelSerializer):
    # حقل للقراءة فقط لإظهار اسم المستخدم بدلاً من ID
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = TestProfile
        # يجب أن يتطابق هذا مع الحقول الموجودة في نموذجك
        fields = ['id', 'name', 'target_url', 'config_settings', 'created_by', 'created_by_username', 'created_at']
        # نجعل حقل created_by للقراءة فقط ليتم تعيينه تلقائيًا في View
        read_only_fields = ['created_by', 'created_by_username'] 

# ----------------------------------------------------
# 2. Vulnerability Serializer (لتمثيل الثغرات)
# ----------------------------------------------------
class VulnerabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vulnerability
        fields = '__all__' # عرض جميع الحقول


# ----------------------------------------------------
# 3. Scan Serializer (لتمثيل عملية المسح مع نتائجها)
# ----------------------------------------------------
class ScanSerializer(serializers.ModelSerializer):
    # إضافة حقل لإدراج قائمة الثغرات المرتبطة بهذا المسح مباشرة
    vulnerabilities = VulnerabilitySerializer(many=True, read_only=True)
    profile_name = serializers.CharField(source='profile.name', read_only=True)
    scheduled_by_username = serializers.CharField(source='scheduled_by.username', read_only=True)

    class Meta:
        model = Scan
        fields = ['id', 'profile', 'profile_name', 'status', 'start_time', 'end_time', 'scheduled_by_username', 'vulnerabilities']
        read_only_fields = ['scheduled_by_username']