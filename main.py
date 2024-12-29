#Welcome To My Scam Banking System...
#Created By Reddy Naresh Under The Guidance of IIT Faculty...

import os
import hashlib
import random
from datetime import datetime

# File paths
ACCOUNTS_FILE = "accounts.txt"
TRANSACTIONS_FILE = "transactions.txt"
ADMIN_USER = "naresh@scambank"
ADMIN_PASSWORD = "naresh@000"  # You can change this for better security

# Hashing passwords for security
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Create an account
def create_account():
    # Validate Full Name - Should only contain letters and spaces
    while True:
        name = input("Enter your Full Name: ")
        if name.isalpha() or " " in name:  # Allowing spaces in name as well
            break
        else:
            print("Invalid name. Please enter a valid name with only letters and spaces.")
    
    # Validate Mobile Number - Should be exactly 10 digits
    while True:
        mobile_number = input("Enter your Mobile Number: ")
        if len(mobile_number) == 10 and mobile_number.isdigit():
            break
        else:
            print("Invalid mobile number. Please enter a 10-digit number.")
    
    # Validate Initial Deposit - Should be a valid number
    while True:
        try:
            initial_deposit = float(input("Enter your initial deposit: "))
            if initial_deposit > 0:
                break
            else:
                print("Deposit must be greater than 0.")
        except ValueError:
            print("Invalid deposit amount. Please enter a valid number.")

    # Validate Password - Ensuring at least 6 characters
    while True:
        password = input("Create a password (at least 6 characters): ")
        if len(password) >= 6:
            break
        else:
            print("Password must be at least 6 characters long.")
    
    # Account type selection
    print("Select Account Type:")
    print("1. Savings Account")
    print("2. Fixed Deposit Account")
    account_type_choice = input("Enter your choice: ")

    # Generate unique account number
    account_number = str(hash(name + str(datetime.now())))[-6:]

    # Hash the password
    hashed_password = hash_password(password)

    account_type = "Savings" if account_type_choice == "1" else "Fixed Deposit"

    # Write to accounts file
    with open(ACCOUNTS_FILE, "a") as file:
        file.write(f"{account_number},{name},{mobile_number},{hashed_password},{initial_deposit},{account_type}\n")

    print(f"Your account has been created successfully!")
    print(f"Your account number is: {account_number} (Save this for next time login)")

# Simulate sending OTP
def send_otp(mobile_number):
    otp = random.randint(100000, 999999)  # Generate a 6-digit OTP
    print(f"OTP sent to {mobile_number}: {otp}")  # Display OTP in the terminal
    return otp

# Login functionality
def login():
    account_number = input("Enter your account number: ")
    password = input("Enter your password: ")
    hashed_password = hash_password(password)

    # Read account details
    with open(ACCOUNTS_FILE, "r") as file:
        for line in file:
            acc_no, name, mobile_number, hashed_pwd, balance, acc_type = line.strip().split(",")
            if acc_no == account_number and hashed_pwd == hashed_password:
                print("OTP is being sent to your registered mobile number...")
                otp = send_otp(mobile_number)
                entered_otp = input("Enter the OTP sent to your mobile: ")
                if str(otp) == entered_otp:
                    print(f"Login successful! Welcome, {name}.")
                    return account_number, float(balance), acc_type
                else:
                    print("Invalid OTP. Login failed.")
                    return None, None, None

    print("Invalid account number or password.")
    return None, None, None

# Deposit functionality
def deposit(account_number, current_balance):
    amount = float(input("Enter the amount to deposit: "))
    new_balance = current_balance + amount

    # Log transaction
    with open(TRANSACTIONS_FILE, "a") as file:
        file.write(f"{account_number},Deposit,{amount},{datetime.now().strftime('%Y-%m-%d')}\n")

    # Update account balance
    update_balance(account_number, new_balance)

    print(f"Deposit successful! Your new balance is: {new_balance}")
    return new_balance

# Withdrawal functionality
def withdraw(account_number, current_balance, account_type):
    if account_type == "Fixed Deposit":
        print("You cannot withdraw from a Fixed Deposit account!")
        return current_balance
    
    amount = float(input("Enter the amount to withdraw: "))
    if amount > current_balance:
        print("Insufficient balance!")
        return current_balance

    new_balance = current_balance - amount

    # Log transaction
    with open(TRANSACTIONS_FILE, "a") as file:
        file.write(f"{account_number},Withdrawal,{amount},{datetime.now().strftime('%Y-%m-%d')}\n")

    # Update account balance
    update_balance(account_number, new_balance)

    print(f"Withdrawal successful! Your new balance is: {new_balance}")
    return new_balance

# Update balance in accounts file
def update_balance(account_number, new_balance):
    with open(ACCOUNTS_FILE, "r") as file:
        lines = file.readlines()

    with open(ACCOUNTS_FILE, "w") as file:
        for line in lines:
            acc_no, name, mobile_number, hashed_pwd, balance, acc_type = line.strip().split(",")
            if acc_no == account_number:
                file.write(f"{acc_no},{name},{mobile_number},{hashed_pwd},{new_balance},{acc_type}\n")
            else:
                file.write(line)

# Admin Panel
def admin_panel():
    username = input("Enter admin username: ")
    password = input("Enter admin password: ")

    if username == ADMIN_USER and password == ADMIN_PASSWORD:
        print("Admin login successful.")
        while True:
            print("\n1. View All Accounts")
            print("2. Delete Account")
            print("3. Logout")
            admin_choice = input("Enter your choice: ")
            
            if admin_choice == "1":
                with open(ACCOUNTS_FILE, "r") as file:
                    for line in file:
                        print(line.strip())
            elif admin_choice == "2":
                account_number = input("Enter the account number to delete: ")
                delete_account(account_number)
            elif admin_choice == "3":
                print("Logged out successfully!")
                break
            else:
                print("Invalid choice.")
    else:
        print("Invalid admin credentials.")

# Delete Account functionality for Admin
def delete_account(account_number):
    with open(ACCOUNTS_FILE, "r") as file:
        lines = file.readlines()

    # Check if the account exists
    account_found = False
    with open(ACCOUNTS_FILE, "w") as file:
        for line in lines:
            # Skip the header line
            if line.strip().startswith("Account Number"):
                file.write(line)
                continue
            try:
                # Unpack the account details
                acc_no, name, mobile_number, hashed_pwd, balance, acc_type = line.strip().split(",")
                # If the account number doesn't match, write the line back to the file
                if acc_no != account_number:
                    file.write(line)
                else:
                    account_found = True
            except ValueError:
                print("Error processing line, skipping: ", line)
                continue

    if account_found:
        print(f"Account {account_number} deleted successfully.")
    else:
        print("Account number not found.")

# Initialize the accounts file with headers
def initialize_accounts_file():
    if not os.path.exists(ACCOUNTS_FILE):
        # Create the file and add headers
        with open(ACCOUNTS_FILE, "w") as file:
            file.write("Account Number,Account Holder,Mobile Number,Password,Balance,Account Type\n")
    else:
        # Check if headers already exist
        with open(ACCOUNTS_FILE, "r") as file:
            first_line = file.readline().strip()
        if first_line != "Account Number,Account Holder,Mobile Number,Password,Balance,Account Type":
            with open(ACCOUNTS_FILE, "w") as file:
                file.write("Account Number,Account Holder,Mobile Number,Password,Balance,Account Type\n")

# Main Menu
def main_menu():
    while True:
        print("\nWelcome to the Scam Banking System!")
        print("1. Create Account")
        print("2. Login")
        print("3. Admin Panel(Only Bank Employees Allowed)")
        print("4. Exit")

        choice = input("How can we help you: ")

        if choice == "1":
            create_account()
        elif choice == "2":
            account_number, balance, account_type = login()
            if account_number:
                while True:
                    print("\n1. Deposit")
                    print("2. Withdraw")
                    print("3. Logout")
                    sub_choice = input("Enter your choice: ")
                    if sub_choice == "1":
                        balance = deposit(account_number, balance)
                    elif sub_choice == "2":
                        balance = withdraw(account_number, balance, account_type)
                    elif sub_choice == "3":
                        print("Logged out successfully!")
                        break
                    else:
                        print("Invalid choice!")
        elif choice == "3":
            admin_panel()
        elif choice == "4":
            print("Thank you for using the Banking System. Goodbye!")
            break
        else:
            print("Invalid choice! Please try again.")

# Run the program
if __name__ == "__main__":
    # Initialize the accounts file with headers
    initialize_accounts_file()

    # Ensure files exist
    if not os.path.exists(ACCOUNTS_FILE):
        open(ACCOUNTS_FILE, "w").close()
    if not os.path.exists(TRANSACTIONS_FILE):
        open(TRANSACTIONS_FILE, "w").close()
        
    main_menu()