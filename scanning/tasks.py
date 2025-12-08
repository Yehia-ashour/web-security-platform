# scanning/tasks.py
from celery import shared_task
from .models import Scan, Vulnerability
import time
import random
from django.utils import timezone

# ----------------------------------------------------
# المهمة الرئيسية لتشغيل المسح في الخلفية
# ----------------------------------------------------
@shared_task(bind=True)
def run_security_scan(self, scan_id):
    """
    تقوم بتشغيل عملية مسح أمنية طويلة الأمد (Async).
    """
    try:
        scan = Scan.objects.get(id=scan_id)
        
        # 1. تحديث حالة المسح (بدأ التشغيل)
        scan.status = 'running'
        scan.start_time = timezone.now()
        scan.save()

        # 2. محاكاة عملية المسح الفعلية (هنا يتم استدعاء محرك الفحص الخارجي مستقبلاً)
        # نستخدم هنا محاكاة بسيطة للوقت والنتائج
        print(f"Starting deep scan for: {scan.profile.target_url}")
        time.sleep(random.randint(5, 10)) # محاكاة انتظار المسح

        # 3. محاكاة إنشاء النتائج (الثغرات)
        vulnerability_count = random.randint(2, 5)
        
        for i in range(vulnerability_count):
            Vulnerability.objects.create(
                scan=scan,
                name=f"SQL Injection (Simulated #{i+1})",
                description="Potential risk of unauthorized data access.",
                severity=random.choice(['Critical', 'High', 'Medium']),
                is_fixed=False
            )

        # 4. تحديث حالة المسح (اكتمل بنجاح)
        scan.status = 'completed'
        scan.end_time = timezone.now()
        scan.save()
        
        return f"Scan ID {scan_id} completed successfully with {vulnerability_count} vulnerabilities found."

    except Scan.DoesNotExist:
        print(f"Scan ID {scan_id} not found.")
        return "Scan ID not found."
    except Exception as exc:
        # هنا يمكنك استخدام self.retry() لإعادة المحاولة إذا فشل المسح
        scan.status = 'failed'
        scan.save()
        raise self.retry(exc=exc, countdown=60)