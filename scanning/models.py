# scanning/models.py
from django.db import models

class ScanProfile(models.Model):
    name = models.CharField(max_length=100)
    target_url = models.URLField(max_length=2000)
    created_by = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.SET_NULL,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Scan(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )

    target_url = models.URLField(max_length=2000)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    scheduled_by = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        related_name='scans_scheduled'
    )

    def __str__(self):
        return f"Scan for {self.target_url} - {self.status}"


class Vulnerability(models.Model):
    scan = models.ForeignKey(Scan, on_delete=models.CASCADE, related_name='vulnerabilities')
    alert = models.CharField(max_length=255)
    risk = models.CharField(max_length=50)
    confidence = models.CharField(max_length=50)
    url = models.URLField(max_length=2000)
    param = models.CharField(max_length=255, blank=True, null=True)
    attack = models.TextField(blank=True, null=True)
    description = models.TextField()
    found_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.alert} ({self.risk}) in Scan ID {self.scan.id}"
