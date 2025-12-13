from rest_framework import serializers
from .models import Report


class ReportSerializer(serializers.ModelSerializer):
    download_url = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = [
            'id',
            'scan',
            'report_type',
            'status',
            'generated_at',
            'download_url',
        ]

    def get_download_url(self, obj):
        request = self.context.get('request')
        if obj.file:
            return request.build_absolute_uri(obj.file.url)
        return None
