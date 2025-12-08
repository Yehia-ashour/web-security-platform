# reporting/tasks.py
from celery import shared_task
from django.conf import settings
from scanning.models import Scan, Vulnerability
from .models import Report
import time
import os
import uuid
from django.utils import timezone

@shared_task(bind=True)
def generate_report_pdf(self, report_id):
    """
    مهمة Celery لتوليد تقرير PDF بشكل غير متزامن (محاكاة).
    """
    try:
        report = Report.objects.get(id=report_id)
        scan = report.scan
        report.status = 'GENERATING'
        report.save()

        # 1. جمع البيانات
        vulnerabilities = scan.vulnerability_set.all()
        
        # 2. محاكاة توليد محتوى التقرير (نصي بدلاً من PDF)
        content = f"--- Security Scan Report (ID: {scan.id}) ---\n"
        content += f"Target URL: {scan.profile.target_url}\n"
        content += f"Status: {scan.status}\n"
        content += f"Total Vulnerabilities Found: {vulnerabilities.count()}\n\n"
        
        for vuln in vulnerabilities:
            content += f"- Severity: {vuln.severity} | Name: {vuln.name} | Description: {vuln.description[:50]}...\n"
            
        # 3. حفظ الملف في مجلد MEDIA_ROOT
        # نستخدم اسم ملف فريد لتجنب التعارض
        unique_id = uuid.uuid4().hex[:8]
        file_name = f"report_{scan.id}_{unique_id}.txt" 
        
        # تحديد مسار التخزين
        report_dir = os.path.join(settings.MEDIA_ROOT, 'reports')
        os.makedirs(report_dir, exist_ok=True) # إنشاء المجلد إذا لم يكن موجوداً
        file_path = os.path.join(report_dir, file_name)
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        # 4. تحديث سجل التقرير
        report.file_path = f"{settings.MEDIA_URL}reports/{file_name}" # حفظ المسار القابل للوصول عبر الويب
        report.status = 'COMPLETED'
        report.generated_at = timezone.now()
        report.save()
        
        return f"Report {report_id} generated successfully."

    except Report.DoesNotExist:
        return "Report ID not found."
    except Exception as exc:
        if 'report' in locals():
            report.status = 'FAILED'
            report.save()
        raise self.retry(exc=exc, countdown=60) # لإعادة محاولة المهمة في حالة الفشل