
# 🛡️ Web Security Platform Backend

This repository contains the backend implementation for a comprehensive Web Security Testing Platform, built using **Django** and **Django Rest Framework (DRF)**.

The system is designed to handle user roles (Testers, Admins, Clients), schedule security scans, and manage vulnerability reports, following the provided Use Case and Sequence Diagrams.

## 🚀 Getting Started

Follow these steps to set up the project locally and start development.

### 1. Prerequisites

Before starting, ensure you have the following installed on your system:

* **Python (3.9+)**
* **Git**
* **PostgreSQL** (Database server must be running)

### 2. Clone the Repository

Clone the project from GitHub and navigate into the directory:

```bash
git clone <YOUR_REPOSITORY_URL>
cd web-security-platform
````

### 3\. Setup Virtual Environment

Create and activate a Python virtual environment to manage dependencies:

```bash
# Create the environment
python -m venv venv

# Activate the environment (Linux/macOS)
source venv/bin/activate

# Activate the environment (Windows)
# .\venv\Scripts\activate
```

### 4\. Install Dependencies

Install all necessary Python packages (Django, DRF, psycopg2, etc.). **Make sure to run `pip freeze > requirements.txt` and push that file first.**

```bash
pip install -r requirements.txt
```

### 5\. Configure Local Secrets (`.env` file)

You must create a local environment file to hold sensitive information, as it is ignored by Git.

1.  Create a file named **`.env`** in the project's root directory.

2.  Add the following required variables (Get the `SECRET_KEY` from the Project Leader):

    ```
    SECRET_KEY='YOUR_ACTUAL_SECRET_KEY_HERE'

    # Local PostgreSQL Settings
    # NOTE: You must create this database in your PostgreSQL server manually.
    DATABASE_NAME='web_security_db'
    DATABASE_USER='your_local_pg_user'
    DATABASE_PASSWORD='your_local_pg_password'
    DATABASE_HOST='localhost'
    DATABASE_PORT=5432
    ```

### 6\. Database Setup and Migrations

Ensure your local PostgreSQL server is running and the database specified in the `.env` file is created.

Then, run the Django migrations:

```bash
python manage.py migrate
```

### 7\. Create a Superuser

Create an administrative user for testing the Django Admin interface:

```bash
python manage.py createsuperuser
```

### 8\. Run the Development Server

Start the Django local server:

```bash
python manage.py runserver
```

The API will be running at `http://127.0.0.1:8000/`.

## ⚙️ API Endpoints

The project uses Django Rest Framework. Key API endpoints include:

| Functionality | Endpoint | HTTP Method | Authentication |
| :--- | :--- | :--- | :--- |
| **Login / Token Generation** | `/api/token/` | `POST` | None |
| **Token Refresh** | `/api/token/refresh/` | `POST` | None |
| **Create/List Test Profiles** | `/api/scanning/profiles/` | `GET`, `POST` | Token Required |
| **Manage Users (Admin Only)** | `/api/users/...` | `GET`, `POST`, etc. | Role-Based |
| **View Scans & Results** | `/api/scanning/scans/...` | `GET` | Role-Based |

## 🛠️ Key Libraries Used

  * **Django:** Core Web Framework.
  * **Django Rest Framework (DRF):** For building the RESTful API.
  * **`psycopg2`:** PostgreSQL database adapter.
  * **`djangorestframework-simplejwt`:** For Token-based Authentication (JWT).
  * **`python-decouple`:** For managing environment variables securely.

## 🧑‍💻 Contribution Guide

1.  Always work on a feature branch (e.g., `git checkout -b feature/implement-permissions`).
2.  Commit frequently with clear messages.
3.  Ensure your code adheres to Python standards (PEP 8).
4.  Submit a Pull Request to the `main` branch once the feature is complete and tested.

<!-- end list -->

```
```
