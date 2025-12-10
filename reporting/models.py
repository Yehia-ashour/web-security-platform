from django.db import models
from scanning.models import Scan


class Report(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('READY', 'Ready'),
        ('FAILED', 'Failed'),
    ]

    scan = models.OneToOneField(
        Scan,
        on_delete=models.CASCADE,
        related_name='report',
        verbose_name="Scan Operation"
    )

    report_type = models.CharField(max_length=50, default='PDF', verbose_name="Report Type")

    # مكان حفظ ملف PDF الفعلي
    file = models.FileField(upload_to='reports/', null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')

    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report for Scan {self.scan.id} ({self.status})"
