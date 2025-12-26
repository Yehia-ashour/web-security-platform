import zapv2
import time


class ZAPClient:
    def __init__(self, base_url='http://localhost:8080', api_key='demo'):
        self.zap = zapv2.ZAPv2(apikey=api_key, proxies={'http': base_url, 'https': base_url})

    def run_full_scan(self, target_url):
        print(f'🔍 ZAP scanning: {target_url}')

        try:
            # 1. Spider scan
            print('Starting spider scan...')
            scan_id = self.zap.spider.scan(url=target_url, maxchildren=10, recurse=True)
            print(f'Spider started with ID: {scan_id}')

            # Wait for spider to complete
            while True:
                status = self.zap.spider.status(scan_id)
                progress = int(status)
                print(f'Spider progress: {progress}%')
                if progress >= 100:
                    break
                time.sleep(2)

            # 2. Active Scan
            print('Starting active scan...')
            ascan_id = self.zap.ascan.scan(url=target_url, recurse=True)
            print(f'Active scan started with ID: {ascan_id}')

            # 3. Wait for active scan completion
            while True:
                status = self.zap.ascan.status(ascan_id)
                progress = int(status)
                print(f'Active scan progress: {progress}%')
                if progress >= 100:
                    break
                time.sleep(10)

            # 4. Get alerts
            alerts = self.zap.core.alerts(baseurl=target_url)
            print(f'✅ ZAP found {len(alerts)} vulnerabilities!')

            # Format alerts to match required structure
            formatted_alerts = []
            for alert in alerts:
                formatted_alerts.append({
                    'alert': alert.get('alert', 'Unknown'),
                    'risk': alert.get('risk', 'Medium'),
                    'confidence': alert.get('confidence', 'Medium'),
                    'url': alert.get('url', ''),
                    'param': alert.get('param', ''),
                    'attack': alert.get('attack', ''),
                    'description': alert.get('description', ''),
                })

            return formatted_alerts

        except Exception as e:
            print(f'ZAP scan failed: {e}')
            return []
