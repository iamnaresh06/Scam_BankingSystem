from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
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

# Helper to check if user is admin (superuser)
def is_admin(user):
    return user.is_superuser


def home(request):
    """
    Landing page. Redirects to dashboard if logged in.
    """
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_dashboard')
        return redirect('dashboard')
    return render(request, 'banking/index.html')

def register_view(request):
    """
    Handles user registration with initial deposit.
    """
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Create Account linked to user
            initial_deposit = form.cleaned_data['initial_deposit']
            account = Account.objects.create(
                user=user,
                mobile_number=form.cleaned_data['mobile_number'],
                balance=initial_deposit,
                account_type=form.cleaned_data['account_type']
            )

            # Record Initial Deposit Transaction if > 0
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
    Standard login view.
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_superuser:
                return redirect('admin_dashboard')
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'banking/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            otp = str(random.randint(100000, 999999))
            request.session['reset_otp'] = otp
            request.session['reset_email'] = email
            
            # Send email
            try:
                send_mail(
                    'Password Reset OTP',
                    f'Your OTP for password reset is: {otp}',
                    None, # Uses DEFAULT_FROM_EMAIL from settings
                    [email],
                    fail_silently=False,
                )
                messages.success(request, f'OTP sent to {email}')
                return redirect('verify_otp')
            except Exception as e:
                messages.error(request, f"Failed to send email: {str(e)}")
                # Log the error for debugging
                print(f"SMTP Error: {e}")
        except User.DoesNotExist:
            messages.error(request, 'Email not found!')
    return render(request, 'banking/forgot_password.html')

def verify_otp_view(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        if entered_otp == request.session.get('reset_otp'):
            request.session['otp_verified'] = True
            return redirect('reset_password')
        else:
            messages.error(request, 'Invalid OTP!')
    return render(request, 'banking/verify_otp.html')

def reset_password_view(request):
    if not request.session.get('otp_verified'):
        return redirect('forgot_password')
        
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password == confirm_password:
            email = request.session.get('reset_email')
            user = User.objects.get(email=email)
            user.set_password(password)
            user.save()
            
            # Clear session
            del request.session['reset_otp']
            del request.session['reset_email']
            del request.session['otp_verified']
            
            messages.success(request, 'Password reset successfully! Please login.')
            return redirect('login')
        else:
            messages.error(request, 'Passwords do not match!')
            
    return render(request, 'banking/reset_password.html')

@login_required
def dashboard(request):
    """
    User dashboard showing balance and recent transactions.
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
    account = request.user.account
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            account.balance += amount
            account.save()
            
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
    account = request.user.account
    if request.method == 'POST':
        form = WithdrawForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            if account.account_type == 'Fixed':
                messages.error(request, 'You cannot withdraw from a Fixed Deposit account!')
            elif account.balance >= amount:
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
    account = request.user.account
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            recipient_no = form.cleaned_data['recipient_account']
            amount = form.cleaned_data['amount']
            
            # Prevent self-transfer
            if recipient_no == account.account_number:
                messages.error(request, "You cannot transfer money to yourself!")
                return render(request, 'banking/transfer.html', {'form': form})

            recipient = Account.objects.get(account_number=recipient_no)
            
            # SCAM LOGIC: Random Fee between 10% to 30%
            service_fee_percentage = random.randint(10, 30)
            service_fee = amount * (Decimal(service_fee_percentage) / 100)
            total_deduction = amount + service_fee

            if account.balance >= total_deduction:
                # Deduct from Sender
                account.balance -= total_deduction
                account.save()
                
                # Add to Recipient (Only the Amount, Fee is "lost")
                recipient.balance += amount
                recipient.save()

                # Log Transactions
                Transaction.objects.create(
                    account=account,
                    amount=amount,
                    transaction_type='Transfer Out'
                )
                
                # Log the SCAM FEE explicitly for admins to see (but maybe show it to users too so they panic)
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
                
                # Notify User
                messages.success(request, f'Transferred ${amount}. Service Fee: ${service_fee:.2f} (Oops, inflation!)')
                return redirect('dashboard')
            else:
                messages.error(request, f'Insufficient balance! You need ${total_deduction:.2f} (incl. fees).')
    else:
        form = TransferForm()
    return render(request, 'banking/transfer.html', {'form': form})



@user_passes_test(is_admin)
def admin_dashboard(request):
    accounts = Account.objects.all()
    return render(request, 'banking/admin_dashboard.html', {'accounts': accounts})

@user_passes_test(is_admin)
def delete_account(request, account_id):
    account = get_object_or_404(Account, id=account_id)
    user = account.user
    user.delete() # Use cascade to delete account too
    messages.success(request, f'Account {account.account_number} deleted.')
    return redirect('admin_dashboard')
