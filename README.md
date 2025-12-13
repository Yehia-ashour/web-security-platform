```markdown
# 🛡️ Web Security Platform (WSP)

A scalable web-based platform for automated security testing of web applications.  
The platform allows users to submit a target URL, run asynchronous security scans, detect vulnerabilities, and generate downloadable security reports.

---

## 🚀 Project Overview

Web Security Platform (WSP) is designed to help developers and small teams perform automated web security assessments without requiring deep security expertise.

The system focuses on:
- Asynchronous security scanning
- Role-based access control
- Clean RESTful APIs
- Report generation and file delivery
- Future integration with external security testing engines

---

## 🧠 System Architecture

The platform follows a **modular and scalable architecture**:

- **Backend:** Django + Django REST Framework
- **Authentication:** JWT (SimpleJWT)
- **Async Tasks:** Celery + Redis
- **Database:** SQLite (development) → PostgreSQL (production-ready)
- **Reports:** Generated as PDF files and served via media endpoints

### Core Modules

| Module | Responsibility |
|------|---------------|
| `users` | Authentication, roles, permissions |
| `scanning` | Scan lifecycle, vulnerabilities, async execution |
| `reporting` | Report storage and read-only access |
| `security engine` | External (planned integration) |

---

## 🔐 Authentication & Roles

The system uses **JWT authentication** with role-based permissions.

### Supported Roles
- **Admin**
- **Security Tester**
- **Client**

Each role has controlled access to scans, vulnerabilities, and reports.

---

## 🔄 Scan & Report Flow

1. User creates a **Test Profile** with a target URL
2. User triggers a **Scan**
3. Scan runs asynchronously using **Celery**
4. Vulnerabilities are collected
5. A **Report** is generated asynchronously
6. A **PDF report** becomes available for download

---

## 📡 API Flow Summary

### Authentication
```

POST /api/token/
POST /api/token/refresh/

```

### Scanning
```

POST /api/scanning/profiles/
POST /api/scanning/profiles/{id}/run_scan/
GET  /api/scanning/scans/
GET  /api/scanning/scans/{id}/
POST /api/scanning/scans/{id}/export_report/

```

### Reporting
```

GET /api/reporting/reports/
GET /api/reporting/reports/{id}/

````

Each report includes a direct `download_url` for the generated PDF.

---

## 📄 Reports

- Reports are generated asynchronously
- Stored as PDF files under `/media/reports/`
- Each scan has **one report only**
- Download is handled via a secure media endpoint

---

## 🔌 Security Engine Integration (Planned)

The platform is designed to integrate with **external security testing engines**.

### Current State
- Security scanning is simulated
- Vulnerability data structure is finalized
- Async execution pipeline is ready

### Planned Integration
- External security tools (e.g. OWASP ZAP, custom scripts)
- Deployed independently on a server
- Triggered via Celery tasks
- Results parsed and stored in the platform database

This design allows replacing the simulated scan logic with real-world security engines **without changing the API or database structure**.

---

## 🧩 Team Integration Guide

### 🔐 Security Team
The security engine should provide:
- Vulnerability name
- Description
- Severity (Critical / High / Medium / Low)
- Affected endpoint or component

The backend will handle:
- Execution
- Storage
- Reporting
- Permissions

---

### 🎨 Frontend Team
The frontend can start immediately using the provided APIs.

Frontend responsibilities:
- Authentication flow (JWT)
- Profile creation
- Scan triggering
- Scan status tracking
- Report listing
- PDF download via `download_url`

All endpoints are stable and documented above.

---

## ⚙️ Local Setup

### Requirements
- Python 3.10+ (recommended)
- Redis
- Docker (optional, recommended)

### Installation
```bash
git clone https://github.com/Yehia-ashour/web-security-platform.git
cd web-security-platform
pip install -r requirements.txt
````

### Run Redis

```bash
redis-server
```

### Run Django

```bash
python manage.py migrate
python manage.py runserver
```

### Run Celery

```bash
celery -A WSP worker --loglevel=info --pool=solo
```

---

## 🧪 Development Notes

* SQLite is used for development
* PostgreSQL migration is planned
* Media files are served only in DEBUG mode

---

## 📌 Project Status

* Backend core: ✅ Completed
* Async scanning: ✅ Completed
* Reporting system: ✅ Completed
* Security engine: 🔄 In progress
* Frontend integration: 🔄 In progress
