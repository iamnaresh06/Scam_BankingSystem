from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .models import Account, Transaction
from .forms import RegisterForm, DepositForm, WithdrawForm, TransferForm
from django.db import transaction
from django.core.mail import send_mail
from django.contrib.auth.models import User
import random
from decimal import Decimal

# ==========================================
# HELPER FUNCTIONS
# ==========================================

def is_admin(user):
    """
    Checks if the user is a superuser (Admin).
    Used for decorator @user_passes_test.
    """
    return user.is_superuser


# ==========================================
# PUBLIC VIEWS (No Login Required)
# ==========================================

def home(request):
    """
    Landing page view.
    - If user is logged in -> Redirect to Dashboard.
    - If user is admin -> Redirect to Admin Panel.
    - Otherwise -> Show the landing page (index.html).
    """
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_dashboard')
        return redirect('dashboard')
    return render(request, 'banking/index.html')


def register_view(request):
    """
    Handles user registration.
    - create a User object.
    - create an associated Account object (Savings/Fixed).
    - Handle initial deposit if provided.
    """
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # 1. Create the User
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # 2. Create the Bank Account linked to the User
            initial_deposit = form.cleaned_data['initial_deposit']
            account = Account.objects.create(
                user=user,
                mobile_number=form.cleaned_data['mobile_number'],
                balance=initial_deposit,
                account_type=form.cleaned_data['account_type']
            )

            # 3. Log Initial Deposit Transaction if valid
            if initial_deposit > 0:
                Transaction.objects.create(
                    account=account,
                    amount=initial_deposit,
                    transaction_type='Deposit'
                )

            messages.success(request, 'Account created successfully! Please login.')
            return redirect('login')
    else:
        form = RegisterForm()
    
    return render(request, 'banking/register.html', {'form': form})


def login_view(request):
    """
    Standard Login View.
    Uses Django's built-in AuthenticationForm.
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Redirect based on user role
            if user.is_superuser:
                return redirect('admin_dashboard')
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'banking/login.html', {'form': form})


def logout_view(request):
    """
    Logs out the user and redirects to the home page.
    """
    logout(request)
    return redirect('home')


# ==========================================
# PASSWORD RESET FEATURES (OTP via Email)
# ==========================================

def forgot_password_view(request):
    """
    Step 1: User enters email.
    - Generate 6-digit OTP.
    - Send OTP via Email.
    - Store OTP in session for verification.
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            # Check if user exists
            user = User.objects.get(email=email)
            
            # Generate OTP
            otp = str(random.randint(100000, 999999))
            
            # Store in session (temporary storage)
            request.session['reset_otp'] = otp
            request.session['reset_email'] = email
            
            # Send Email
            try:
                send_mail(
                    'Password Reset OTP',
                    f'Your OTP for password reset is: {otp}',
                    None,
                    [email],
                    fail_silently=False,
                )
                messages.success(request, f'OTP sent to {email}')
            except Exception as e:
                # Fallback for Development/Render Free Tier blocking SMTP
                print(f"!!! RENDER/LOCAL SMTP DEBUG !!!")
                print(f"OTP for {email} is: {otp}")
                messages.warning(request, f"Email delivery may be restricted. Check server logs for OTP.")
            
            return redirect('verify_otp')
        except User.DoesNotExist:
            messages.error(request, 'Email not found!')
            
    return render(request, 'banking/forgot_password.html')


def verify_otp_view(request):
    """
    Step 2: Verify the OTP entered by the user.
    """
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        if entered_otp == request.session.get('reset_otp'):
            # Mark as verified
            request.session['otp_verified'] = True
            return redirect('reset_password')
        else:
            messages.error(request, 'Invalid OTP!')
    return render(request, 'banking/verify_otp.html')


def reset_password_view(request):
    """
    Step 3: Allow user to set a new password.
    Requires 'otp_verified' flag in session.
    """
    if not request.session.get('otp_verified'):
        return redirect('forgot_password')
        
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password == confirm_password:
            email = request.session.get('reset_email')
            user = User.objects.get(email=email)
            
            # Set new password
            user.set_password(password)
            user.save()
            
            # Clean up session
            del request.session['reset_otp']
            del request.session['reset_email']
            del request.session['otp_verified']
            
            messages.success(request, 'Password reset successfully! Please login.')
            return redirect('login')
        else:
            messages.error(request, 'Passwords do not match!')
            
    return render(request, 'banking/reset_password.html')


# ==========================================
# BANKING FEATURES (Login Required)
# ==========================================

@login_required
def dashboard(request):
    """
    Main Dashboard.
    Shows account balance and the last 5 transactions.
    """
    if request.user.is_superuser:
        return redirect('admin_dashboard')
        
    account = request.user.account
    recent_transactions = account.transactions.order_by('-timestamp')[:5]
    
    return render(request, 'banking/dashboard.html', {
        'account': account,
        'transactions': recent_transactions
    })


@login_required
@transaction.atomic
def deposit_view(request):
    """
    Handles cash deposits.
    Updates balance and creates a transaction record.
    """
    account = request.user.account
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            
            # Update Balance
            account.balance += amount
            account.save()
            
            # Log Transaction
            Transaction.objects.create(
                account=account,
                amount=amount,
                transaction_type='Deposit'
            )
            messages.success(request, f'Deposited ${amount} successfully!')
            return redirect('dashboard')
    else:
        form = DepositForm()
    return render(request, 'banking/deposit.html', {'form': form})


@login_required
@transaction.atomic
def withdraw_view(request):
    """
    Handles withdrawals.
    - Checks for sufficient funds.
    - Prevents withdrawal from 'Fixed Deposit' accounts.
    """
    account = request.user.account
    if request.method == 'POST':
        form = WithdrawForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            
            # Validation
            if account.account_type == 'Fixed':
                messages.error(request, 'You cannot withdraw from a Fixed Deposit account!')
            elif account.balance >= amount:
                # Perform Withdrawal
                account.balance -= amount
                account.save()
                
                Transaction.objects.create(
                    account=account,
                    amount=amount,
                    transaction_type='Withdrawal'
                )
                messages.success(request, f'Withdrew ${amount} successfully!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Insufficient balance!')
    else:
        form = WithdrawForm()
    return render(request, 'banking/withdraw.html', {'form': form})


@login_required
@transaction.atomic
def transfer_view(request):
    """
    Peer-to-Peer Transfer (The "Scam" Feature).
    - Transfers money from User A to User B.
    - !!! HIDDEN FEATURE !!!: Deducts a random 'Service Fee' (10-30%) from the sender.
    - Uses database transactions (atomic) to ensure safety.
    """
    account = request.user.account
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            recipient_no = form.cleaned_data['recipient_account']
            amount = form.cleaned_data['amount']
            
            # Validation: Self-transfer check
            if recipient_no == account.account_number:
                messages.error(request, "You cannot transfer money to yourself!")
                return render(request, 'banking/transfer.html', {'form': form})

            recipient = Account.objects.get(account_number=recipient_no)
            
            # ---------------------------------------------------
            # THE "SCAM" LOGIC (Inflation/Service Fee Simulation)
            # ---------------------------------------------------
            service_fee_percentage = random.randint(10, 30)
            service_fee = amount * (Decimal(service_fee_percentage) / 100)
            total_deduction = amount + service_fee

            if account.balance >= total_deduction:
                # 1. Deduct Total (Amount + Random Fee) from Sender
                account.balance -= total_deduction
                account.save()
                
                # 2. Add Only Amount to Recipient (Fee is kept by "Bank")
                recipient.balance += amount
                recipient.save()

                # 3. Log Transactions
                Transaction.objects.create(
                    account=account,
                    amount=amount,
                    transaction_type='Transfer Out'
                )
                
                # Clearly log the Fee for tracking
                Transaction.objects.create(
                    account=account,
                    amount=service_fee,
                    transaction_type='Service Fee'
                )

                Transaction.objects.create(
                    account=recipient,
                    amount=amount,
                    transaction_type='Transfer In'
                )
                
                messages.success(request, f'Transferred ${amount}. Service Fee: ${service_fee:.2f} (applied automatically).')
                return redirect('dashboard')
            else:
                messages.error(request, f'Insufficient balance! You need ${total_deduction:.2f} to cover the amount + fees.')
    else:
        form = TransferForm()
    return render(request, 'banking/transfer.html', {'form': form})


# ==========================================
# ADMIN FEATURES
# ==========================================

@user_passes_test(is_admin)
def admin_dashboard(request):
    """
    Admin View: List all accounts to manage them.
    """
    accounts = Account.objects.all()
    return render(request, 'banking/admin_dashboard.html', {'accounts': accounts})


@user_passes_test(is_admin)
def delete_account(request, account_id):
    """
    Admin View: Deletes a user and their account.
    """
    account = get_object_or_404(Account, id=account_id)
    user = account.user
    user.delete()  # Cascade deletes account and transactions
    messages.success(request, f'Account {account.account_number} deleted.')
    return redirect('admin_dashboard')
