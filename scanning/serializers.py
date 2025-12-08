# scanning/serializers.py
from rest_framework import serializers
from .models import TestProfile, Scan, Vulnerability 


class TestProfileSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = TestProfile
        fields = [
            'id',
            'name',
            'target_url',
            'created_by',
            'created_by_username',
            'created_at'
        ]
        read_only_fields = ['created_by', 'created_by_username']



class VulnerabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vulnerability
        fields = '__all__' 



class ScanSerializer(serializers.ModelSerializer):
    vulnerabilities = VulnerabilitySerializer(many=True, read_only=True)
    profile_name = serializers.CharField(source='profile.name', read_only=True)
    scheduled_by_username = serializers.CharField(source='scheduled_by.username', read_only=True)

    class Meta:
        model = Scan
        fields = ['id', 'profile', 'profile_name', 'status', 'start_time', 'end_time', 'scheduled_by_username', 'vulnerabilities']
        read_only_fields = ['scheduled_by_username']