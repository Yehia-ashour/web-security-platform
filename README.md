---

# 🛡️ Web Security Platform (BUGGY)

A scalable web-based platform for **automated security testing of web applications**, designed to help developers and small teams identify common web vulnerabilities without requiring deep security expertise.

---

## 📌 Project Overview

The **Web Security Platform (BUGGY)** allows users to:

* Create security test profiles for web applications.
* Run automated security scans asynchronously.
* Detect common web vulnerabilities (simulated for development).
* Generate **professional branded PDF security reports**.
* Access scan history and vulnerability details through a REST API.

The platform is built with a **modular backend architecture**, making it extensible for future integration with real-world security scanners such as **OWASP ZAP**.

---

## 🧩 System Architecture

```
Client (Frontend / API Consumer)
        |
        v
 Django REST API (JWT Auth)
        |
        +-- Scanning Module
        |     - Test Profiles
        |     - Scan Management
        |     - Vulnerabilities
        |
        +-- Reporting Module
        |     - Asynchronous PDF Reports
        |
        +-- Celery + Redis
              - Background Scan Execution
              - PDF Generation
```

---

## ⚙️ Tech Stack

### Backend

* Python
* Django
* Django REST Framework
* JWT Authentication (SimpleJWT)

### Background Processing

* Celery
* Redis

### Documentation

* drf-spectacular (OpenAPI / Swagger UI)

### Database

* SQLite (Development)
* PostgreSQL (Production-ready configuration)

### Reporting

* ReportLab
* Branded PDF reports with:

  * Logo
  * Severity summary
  * Vulnerability table

---

## 🗄️ Database Strategy

### SQLite (Development)

* Simple and fast setup
* Ideal for development and testing
* No external dependencies

### PostgreSQL (Production)

* Production-grade database
* Supports concurrent users
* Strong transactional guarantees
* Scalable and secure

The project is **fully prepared to switch to PostgreSQL** using environment variables without changing application logic.

```python
# PostgreSQL configuration (ready for production)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': config('POSTGRES_DB'),
#         'USER': config('POSTGRES_USER'),
#         'PASSWORD': config('POSTGRES_PASSWORD'),
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }
```

---

## 🔐 Authentication & Authorization

* JWT-based authentication
* Role-based access control:

  * Admin / Security Tester
  * Client
* Permissions enforced at API level

---

## 🔄 Asynchronous Processing

Long-running operations are executed in the background using **Celery**, preventing blocking requests.

### Background Jobs

* Security scan execution
* PDF report generation

---

## 📄 PDF Security Reports

Each scan can generate a **professional PDF report** containing:

* Platform logo
* Scan metadata
* Severity counters (Critical / High / Medium / Low)
* Vulnerabilities table
* Branded footer

Reports are generated asynchronously and served via `/media/`.

---

## 📑 API Documentation

Swagger UI (OpenAPI):

```
http://127.0.0.1:8000/api/schema/swagger-ui/
```

---

## 🚀 How to Run the Project

### 1️⃣ Clone Repository

```bash
git clone https://github.com/Yehia-ashour/web-security-platform.git
cd web-security-platform
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Environment Variables

Create a `.env` file:

```
SECRET_KEY=Secret-key
```

---

### 5️⃣ Run Redis

```bash
redis-server
```

---

### 6️⃣ Run Celery Worker

```bash
celery -A WSP worker --loglevel=info --pool=solo
```

---

### 7️⃣ Run Django Server

```bash
python manage.py migrate
python manage.py runserver
```

---

## 👥 Team Responsibilities

### Backend

* API design and implementation
* Authentication & permissions
* Background processing
* PDF report generation
* Database design

### Security

* Define vulnerability types
* Provide detection logic
* Prepare mitigation strategies

### Frontend

* Consume REST APIs
* Display scans and reports
* Handle authentication

### UI/UX

* User flow and experience
* Visual consistency
* Layout design

---

# 📦 Submission Guide

This section explains **how frontend and security team members should integrate their work** with the backend.

---

## 🎨 Frontend Submission Guide

### 🎯 Goal

Build a user interface that consumes backend APIs to manage scans and view reports.

---

### 🔐 Authentication

```
POST /api/token/
POST /api/token/refresh/
```

Use header:

```
Authorization: Bearer <access_token>
```

---

### 🧪 Scanning Flow

1. Create Test Profile

```
POST /api/scanning/profiles/
```

2. Run Scan

```
POST /api/scanning/profiles/{id}/run_scan/
```

3. View Scan History

```
GET /api/scanning/scans/
```

4. View Vulnerabilities

```
GET /api/scanning/vulnerabilities/
```

---

### 📄 Reports

* Generate report:

```
POST /api/scanning/scans/{id}/export_report/
```

* Get reports list:

```
GET /api/reporting/reports/
```

Each report includes a `download_url` for the PDF.

---

### 🎨 Frontend Responsibilities

* Login / logout
* Forms for test profiles
* Scan status display
* Vulnerability listing
* PDF report download
* Error handling (401 / 403 / 400)

---

## 🔐 Security Team Submission Guide

### 🎯 Goal

Provide the security logic and vulnerability definitions used by the platform.

---

### 📌 Required for Each Vulnerability

1. Name
2. Description
3. How it occurs
4. Impact
5. Detection logic
6. Mitigation / Fix

---

### 🔧 Integration Options

#### Option 1️⃣ (Current – Simulated)

* Vulnerabilities generated programmatically
* Used to test platform flow

#### Option 2️⃣ (Future – Recommended)

* Integrate real scanners (OWASP ZAP)
* Parse scan results into database models

---

### 📁 Expected Output Format

```json
{
  "name": "SQL Injection",
  "severity": "High",
  "description": "User input is not sanitized",
  "recommendation": "Use prepared statements"
}
```

---

## 🧠 Integration Notes

* Backend APIs are stable
* Database schema finalized
* Swagger documentation available
* PostgreSQL prepared for production

---

## 🔮 Future Improvements

* Real vulnerability scanning (OWASP ZAP)
* Dockerized deployment
* PostgreSQL production setup
* Frontend dashboard
* PDF customization options

---

## 📜 License

This project is developed for **educational purposes** as part of a graduation project.

---

## ✅ Project Status

✔ Backend core complete
✔ Asynchronous scanning
✔ PDF reporting
✔ API documentation
✔ Ready for frontend & security integration
