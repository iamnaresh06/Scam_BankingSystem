# Scam Banking System (Full Stack Edition)

Welcome to the future of banking—transparently shady, yet securely engineered.
This project is a robust Full-Stack Django web application that simulates core banking features with a hidden twist: **Simulated Service Fees** (The "Scam" Logic).

It serves as a demonstration of **Advanced Django Logic**, **Atomic Transactions**, and **Modern UI Design**.

## 🚀 Key Features

- **P2P Transfers (The "Scam" Logic)**:
  - Seamless money transfer between users.
  - **Hidden Feature**: A random service fee (10-30%) is deducted from the sender during transfers and is "lost" to the system, simulating inflation or hidden banking charges.
- **Atomic Transactions**:
  - Uses `@transaction.atomic` to ensure data integrity. If a transfer fails halfway, the entire operation rolls back.
- **Secure Authentication**:
  - Login & Registration with Password Visibility Toggles.
  - **OTP-Based Password Reset**: Integrated with Email SMTP for real-world recovery flow.
- **Banking Operations**:
  - **Time-Zone Aware**: All transactions strictly follow local time (`Asia/Kolkata`).
  - **Dashboard**: Premium, glassmorphism-inspired UI with real-time balance updates.
- **Admin Panel**:
  - Superusers can manage accounts and oversee the "fees" collected.
- **Mobile First**: Fully responsive design optimized for all screen sizes.

## 🛠 Tech Stack

- **Backend**: Python, Django 5+
- **Database**: SQLite (Dev), PostgreSQL (Prod ready)
- **Frontend**: HTML5, CSS3 (Glassmorphism), JavaScript
- **Hosting**: Configuration for Render (Gunicorn + WhiteNoise)

## 📂 File Structure

```text
ScamBankingSystem/
│
├── scambank_project/          # Main Project Configuration
│   ├── settings.py            # Global Settings
│   └── urls.py                # Main URL Routing
│
├── banking/                   # Core App Logic
│   ├── models.py              # Account & Transaction Models
│   ├── views.py               # Business Logic (Atomic Transactions)
│   ├── forms.py               # Validation Forms
│   └── urls.py                # App Routings
│
├── templates/                 # UI Templates
│   ├── base.html              # Main Layout
│   └── banking/               # Dashboard, Login, etc.
│
├── static/                    # Static Assets
│   └── css/style.css          # Custom Glassmorphism CSS
│
├── manage.py                  # Django Management Script
├── Procfile                   # Deployment Config (Render)
├── requirements.txt           # Dependencies
└── README.md                  # Documentation
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

## 🌐 Deployment (Render)

1.  Push code to GitHub.
2.  Create a **Web Service** on [Render](https://render.com).
3.  **Build Command**: `pip install -r requirements.txt && python manage.py migrate`
4.  **Start Command**: `gunicorn scambank_project.wsgi`
5.  **Environment Variables**:
    - `SECRET_KEY`: (Generate a secure key)
    - `EMAIL_HOST_USER`: (Your email for OTPs)
    - `EMAIL_HOST_PASSWORD`: (Your App Password)

---

### 👤 Creator Information

**Name**: Reddy Naresh  
**Portfolio**: [reddynaresh.netlify.app](https://reddynaresh.netlify.app/)  
**Email**: [06.nareshreddy@gmail.com](mailto:06.nareshreddy@gmail.com)

**Connect With Me**:

- [**LinkedIn**](https://www.linkedin.com/in/iamnaresh06/)
- [**GitHub**](https://github.com/iamnaresh06)
- [**LeetCode**](https://leetcode.com/u/iamnaresh_06/)

_Developed with passion for modern web architecture._
