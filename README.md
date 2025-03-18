# Scam_BankingSystem

```markdown
# Scam Banking System

## Overview

Welcome to the **Scam Banking System**, a beginner-friendly banking system created for learning purposes under the guidance of IIT faculty. This system is designed to simulate basic banking operations like account creation, deposits, withdrawals, and an admin panel for managing accounts.

---

## Features

- **User Features**:
  - Account creation with validation for name, mobile number, and deposit.
  - Login functionality with OTP verification.
  - Deposit and withdrawal options (restrictions apply for Fixed Deposit accounts).

- **Admin Panel**:
  - View all accounts.
  - Delete accounts.

- **Security**:
  - Password hashing using SHA-256 for secure storage.
  - I used getpass() module, getpass.getpass() hides the input characters and replaces them with nothing.
  - OTP-based authentication for enhanced login security.

---

## File Structure

- `accounts.txt`: Stores account details.
- `transactions.txt`: Logs transactions for deposits and withdrawals.

---

## Prerequisites

- Python 3.x installed.
- Basic knowledge of Python programming.

---

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/<YourUsername>/ScamBankingSystem.git
   ```
2. Navigate to the project directory:
   ```bash
   cd ScamBankingSystem
   ```
3. Run the main script:
   ```bash
   python main.py
   ```
4. Ensure `accounts.txt` and `transactions.txt` are present in the same directory.

---

## Usage

1. Launch the program.
2. Choose from the following options in the main menu:
   - **Create Account**: Register a new account.
   - **Login**: Access your account for transactions.
   - **Admin Panel**: Restricted access for bank employees.
   - **Exit**: Quit the system.

---

## Future Improvements

- Implementation of account balance inquiry.
- Enhanced admin capabilities for generating account statements.
- Integration of a GUI for better user experience.

---

## Disclaimer

This project is for **educational purposes only**. It is not intended for real banking use. 

---

## Author

**Reddy Naresh**  
MCA Student at NSRIT | Minor in Computer Science Engineering & NextGen Technologies at IIT Mandi | Aspiring Software Developer

## Connect Through:-
- Mail ID:- 06.nareshreddy@gmail.com 
- LinkedIn:- https://www.linkedin.com/in/iamnaresh06/ 
