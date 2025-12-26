import requests
import json

# Get token
token_response = requests.post('http://127.0.0.1:8000/api/token/', json={
    'username': 'admin',
    'password': 'admin123'
})
token_data = token_response.json()
access_token = token_data['access']

print(f"Access token: {access_token}")

# Run scan directly
headers = {'Authorization': f'Bearer {access_token}'}
scan_response = requests.post('http://127.0.0.1:8000/api/scanning/run_scan/', headers=headers, json={
    'target_url': 'http://testphp.vulnweb.com'
})

if scan_response.status_code == 202:
    scan_data = scan_response.json()
    scan_id = scan_data['scan_id']
    print(f"Scan initiated: {scan_data}")
else:
    print(f"Scan failed: {scan_response.status_code} - {scan_response.text}")
    scan_id = None

# Poll scan status until completed
import time
print("Polling scan status...")
while True:
    scan_status_response = requests.get(f'http://127.0.0.1:8000/api/scanning/scans/{scan_id}/', headers=headers)
    scan_data = scan_status_response.json()
    status = scan_data['status']
    print(f"Scan status: {status}")
    if status == 'completed':
        break
    elif status == 'failed':
        print("Scan failed!")
        break
    time.sleep(10)

# Check vulnerabilities
vuln_response = requests.get('http://127.0.0.1:8000/api/scanning/vulnerabilities/', headers=headers)
print(f"Vulnerabilities: {vuln_response.status_code} - {vuln_response.json()}")

# Check scan summary
summary_response = requests.get(f'http://127.0.0.1:8000/api/reporting/scans/{scan_id}/summary/', headers=headers)
print(f"Scan summary: {summary_response.status_code} - {summary_response.json()}")
