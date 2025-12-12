📝 **README – Developer Setup Guide**

> This guide helps new developers set up and run the Web Security Platform (WSP) on their own machine.

---

## ⚠️ **Important Notice (MUST READ)**

### **You MUST install Docker before running the project.**

Docker is required to run Redis, which is needed for Celery background tasks.

👉 Download Docker Desktop:
**[https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)**

---

# 🚀 **1. Clone the Project**

```bash
<<<<<<< HEAD
git clone https://github.com/Yehia-ashour/web-security-platform/tree/main
=======
git clone https://github.com/[YOUR_REPO_URL.git](https://github.com/Yehia-ashour/web-security-platform/tree/main)
>>>>>>> eeb7559634bec4b0e95f7ab51f6e74aebdb3e149
cd web-security-platform
```

---

# 🐍 **2. Create a Virtual Environment**

> ⚠️ Celery is NOT compatible with Python 3.14.
> You MUST use **Python 3.10 or Python 3.11**.

### Create venv:

```bash
python -m venv venv
```

### Activate it:

**Windows:**

```bash
venv\Scripts\activate
```

**Mac/Linux:**

```bash
source venv/bin/activate
```

---

# 📦 **3. Install Dependencies**

```bash
pip install -r requirements.txt
```

---

# 🐳 **4. Start Redis Using Docker**

Redis is required for Celery tasks.

```bash
docker run -d --name redis-server -p 6379:6379 redis
```

Check if it’s running:

```bash
docker ps
```

---

# 🌐 **5. Run Django Server**

```bash
python manage.py migrate
python manage.py runserver
```

Server URL:

```
http://127.0.0.1:8000/
```

---

# 🧵 **6. Start Celery Worker**

Open a new terminal (with venv activated):

```bash
celery -A WSP worker --loglevel=info
```

If Celery starts correctly, you'll see:

```
celery worker ready.
```

---

# 🧪 **7. Test the API**

## 7.1 Get JWT Token

```
POST /api/token/
```

Body:

```json
{
  "username": "your_username",
  "password": "your_password"
}
```

## 7.2 Create a Test Profile

```
POST /api/scanning/profiles/
```

```json
{
  "name": "Basic Scan",
  "target_url": "https://example.com"
}
```

## 7.3 Run a Scan

```
POST /api/scanning/profiles/1/run_scan/
```

Expected response:

```json
{
  "status": "Scan initiated successfully",
  "scan_id": 1
}
```

Celery terminal will show:

```
Task received...
Task started...
Task completed...
```

---

# 📂 **8. Project Structure Overview**

```
scanning/
│   models.py          # TestProfile, Scan, Vulnerability
│   views.py           # API endpoints
│   serializers.py     # JSON converters
│   tasks.py           # Celery scan logic
│   urls.py
│
reporting/
│   models.py
│   tasks.py           # PDF report generation (future)
│
users/
│   models.py          # Custom user model + roles
│   permissions.py     # Role-based access
│
WSP/
    settings.py
    celery.py          # Celery app configuration
    urls.py
```

---

# 📌 **9. Recommended Tasks for New Developer**

These are safe tasks the junior developer can work on:

### ✅ Task 1 — Write basic unit tests

For:

* Profiles API
* Scans API

### ✅ Task 2 — Improve serializers

Add validation, clean-up, required checks.

### ✅ Task 3 — API Documentation

Write a simple Markdown file describing all endpoints.

### ✅ Task 4 — Improve error handling

Example:

* URL validation
* Scan failure messages

### ✅ Task 5 — Add filtering in list APIs

Filter scans by status, filter vulnerabilities by severity.

---

# 🛠️ **10. Troubleshooting**

### ❗ Celery error: “not enough values to unpack”

Cause: using Python 3.14
Solution: use **Python 3.10 or 3.11**

---

# 🎉 **Welcome to the Project!**

If you face any issue:

* Take a screenshot
* Send the exact error message

We will guide you step-by-step.

---

## ⭐ Want a shorter version for beginners?

Just tell me and I'll generate it.

---
<<<<<<< HEAD

=======
>>>>>>> eeb7559634bec4b0e95f7ab51f6e74aebdb3e149
