# Scam Banking System (Full Stack Edition)

Welcome to the future of banking - transparently shady, securely insecure, and beautifully animated.
This project has been migrated from a Python terminal script to a full-stack Django web application.

## 🚀 Key Features

*   **P2P Transfers**: Send money to other users instantly with a built-in "Scam Fee" logic (10-30% service charge).
*   **Secure Authentication**: Fully functional Login/Register with **Password Visibility Toggles (Eye Icon)**.
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
6.  **Access the App**:
    *   Open `http://127.0.0.1:8000/` in your browser.

## 📂 Project Structure

*   `scambank_project/`: Main Django project configuration.
*   `banking/`: The core banking application (models, views, urls, forms).
*   `templates/`: Modern HTML5 templates including Dashboard, Auth, and Transfers.
*   `static/`: Premium CSS with custom animations and responsive media queries.

---
### 👤 Creator Information
**Name**: Reddy Naresh  
**Portfolio**: [reddynaresh.netlify.app](https://reddynaresh.netlify.app/)  
**Email**: iamnaresh06@gmail.com  

**Connect With Me**:
*   [**LinkedIn**](https://www.linkedin.com/in/iamnaresh06/)
*   [**GitHub**](https://github.com/iamnaresh06)
*   [**LeetCode**](https://leetcode.com/u/iamnaresh_06/)

*Developed with passion for modern web architecture.*