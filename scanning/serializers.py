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

    # NEW → URL to download the PDF if exists
    report_download_url = serializers.SerializerMethodField()

    class Meta:
        model = Scan
        fields = [
            'id',
            'profile',
            'profile_name',
            'status',
            'start_time',
            'end_time',
            'scheduled_by_username',
            'vulnerabilities',
            'report_download_url',
        ]

    def get_report_download_url(self, obj):
        """
        Returns URL for the report PDF if exists.
        """
        request = self.context.get('request')

        # If no report yet → return None
        if not hasattr(obj, "report"):
            return None

        report = obj.report

        if not report.file:
            return None
        
        # Build absolute download URL
        return request.build_absolute_uri(report.file.url)
