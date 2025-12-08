# reporting/models.py
from django.db import models
from scanning.models import Scan 
from django.conf import settings

class Report(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('GENERATING', 'Generating'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]

    scan = models.ForeignKey(Scan, on_delete=models.CASCADE, related_name='reports', verbose_name="Scan Operation")
    report_type = models.CharField(max_length=50, default='PDF', verbose_name="Report Type")
    file_path = models.CharField(max_length=255, null=True, blank=True, verbose_name="File Path")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING', verbose_name="Status")
    generated_at = models.DateTimeField(auto_now_add=True, verbose_name="Generation Date")
    
    def __str__(self):
        return f"Report for Scan {self.scan.id} ({self.status})"