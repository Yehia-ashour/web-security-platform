# scanning/tasks.py
from celery import shared_task
from .models import Scan, Vulnerability
from .zap_client import ZAPClient  # <-- ZAPClient مش ZAPScanner
from django.utils import timezone

@shared_task(bind=True)
def run_security_scan(self, scan_id):
    scan = None
    try:
        scan = Scan.objects.get(id=scan_id)
        scan.status = 'running'
        scan.start_time = timezone.now()
        scan.save()

        print(f'🚀 ZAP Scan: {scan.target_url}')
        zap = ZAPClient()
        alerts = zap.run_full_scan(scan.target_url)

        vuln_count = 0
        for alert in alerts[:50]:
            try:
                Vulnerability.objects.create(
                    scan=scan,
                    alert=alert.get('alert', 'Unknown'),
                    risk=alert.get('risk', 'Medium'),
                    confidence=alert.get('confidence', 'Medium'),
                    url=alert.get('url', ''),
                    param=alert.get('param', ''),
                    attack=alert.get('attack', ''),
                    description=alert.get('description', '')[:500],
                )
                vuln_count += 1
            except Exception as e:
                print(f'Error saving vulnerability: {e}')
                continue

        scan.status = 'completed'
        scan.end_time = timezone.now()
        scan.save()
        print(f'✅ {vuln_count} vulnerabilities saved!')
        return f'ZAP found {vuln_count} vulnerabilities'

    except Exception as exc:
        print(f'❌ Error: {str(exc)}')
        if scan:
            scan.status = 'failed'
            scan.save()
        raise self.retry(exc=exc, countdown=60)
