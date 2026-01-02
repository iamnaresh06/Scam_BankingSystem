# Scam Banking System (Full Stack Edition)

Welcome to the future of banking - transparently shady, securely insecure, and beautifully animated.
This project has been migrated from a Python terminal script to a full-stack Django web application.

## 🚀 Key Features

*   **P2P Transfers**: Send money to other users instantly with a built-in "Scam Fee" logic (10-30% service charge).
*   **Secure Authentication**: Fully functional Login/Register with **Password Visibility Toggles (Eye Icon) Rendering**.
*   **Password Recovery**: Secure Forgot Password flow with OTP verification (via Console/Email).
*   **Banking Operations**:
    *   **Deposit & Withdraw**: Real-time balance updates and transaction logging.
    *   **Dashboard**: Premium glassmorphism interface with complete transaction history.
*   **Admin Panel**: Superuser dashboard to manage all user accounts and transactions.
*   **Mobile First**: Fully responsive UI optimized for all devices with no horizontal scrolling.

## 🛠 Tech Stack

*   **Backend**: Python, Django
*   **Database**: SQLite
*   **Frontend**: HTML5, CSS3 (Modern Glassmorphism), JavaScript
*   **Middleware**: WhiteNoise (Static Files), SMTP/Console Email Handling
*   **Deployment Ready**: Ready for Render with Gunicorn & Procfile.

## 📂 File Structure

```text
ScamBankingSystem/
│
├── scambank_project/          # Main Project Configuration
│   ├── settings.py            # Global Settings (Whitenoise, Security)
│   ├── urls.py                # Main URL Routing
│   └── wsgi.py                # WSGI Config for Production
│
├── banking/                   # Core App Logic
│   ├── migrations/            # Database Migrations
│   ├── models.py              # Account & Transaction Models
│   ├── views.py               # Functional Logic (Login, Transfer, etc)
│   ├── forms.py               # Validation Forms
│   ├── urls.py                # App-specific Routing
│   └── admin.py               # Admin Panel Configuration
│
├── templates/                 # UI Layouts
│   ├── base.html              # Main Layout Wrapper
│   └── banking/               # Page Templates (Login, Dashboard, etc)
│
├── static/                    # Assets
│   └── css/style.css          # Premium Stylings & Animations
│
├── manage.py                  # Django Management Script
├── Procfile                   # Deployment Config for Render
├── requirements.txt           # Python Dependencies
├── .gitignore                 # Files to Exclude from Git
├── EMAIL_SETUP.md             # Guide for SMTP production email
└── README.md                  # Project Documentation
```

## ⚙️ Installation

1.  **Clone the repository**.
2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run Migrations**:
    ```bash
    python manage.py migrate
    ```
4.  **Create Superuser (Admin)**:
    ```bash
    python manage.py createsuperuser
    ```
5.  **Run the Server**:
    ```bash
    python manage.py runserver
    ```

## 🌐 Deployment on Render

1.  **Push your code to GitHub**.
2.  **Create a New Web Service** on [Render](https://dashboard.render.com/).
3.  **Connect your Repo**.
4.  **Settings**:
    *   **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate`
    *   **Start Command**: `gunicorn scambank_project.wsgi`
5.  **Environment Variables**: Add `PYTHON_VERSION = 3.12.6` (optional) to match your local setup.

---
### 👤 Creator Information
**Name**: Reddy Naresh  
**Portfolio**: [reddynaresh.netlify.app](https://reddynaresh.netlify.app/)  
**Email**: [06.nareshreddy@gmail.com](mailto:06.nareshreddy@gmail.com)  

**Connect With Me**:
*   [**LinkedIn**](https://www.linkedin.com/in/iamnaresh06/)
*   [**GitHub**](https://github.com/iamnaresh06)
*   [**LeetCode**](https://leetcode.com/u/iamnaresh_06/)

*Developed with passion for modern web architecture.*