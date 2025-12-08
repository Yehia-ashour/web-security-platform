# WSP/celery.py
import os
from celery import Celery

# 1. تحديد إعدادات Django لـ Celery باستخدام اسم مشروعك 'WSP'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WSP.settings')

# 2. إنشاء تطبيق Celery
app = Celery('WSP')

# 3. استخدام إعدادات Celery الموجودة في settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# 4. اكتشاف المهام تلقائياً (في ملفات tasks.py داخل كل تطبيق)
app.autodiscover_tasks()