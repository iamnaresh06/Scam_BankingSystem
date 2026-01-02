from django.db import models
from django.contrib.auth.models import User
import random
from datetime import datetime

# Welcome to the models file!
# Here we define the structure of our database tables.
# It's like defining the columns in an Excel sheet.

class Account(models.Model):
    """
    Represents a bank account. 
    Each user has one account.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=10, unique=True)
    mobile_number = models.CharField(max_length=15)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    account_type = models.CharField(max_length=20, choices=[('Savings', 'Savings'), ('Fixed', 'Fixed Deposit')])
    
    def __str__(self):
        return f"{self.user.username} - {self.account_number}"

    def save(self, *args, **kwargs):
        # Generate a random account number if it doesn't exist
        if not self.account_number:
            self.account_number = str(random.randint(1000000000, 9999999999))
        super().save(*args, **kwargs)

class Transaction(models.Model):
    """
    Records every deposit and withdrawal.
    """
    TRANSACTION_TYPES = [
        ('Deposit', 'Deposit'),
        ('Withdrawal', 'Withdrawal'),
        ('Transfer Out', 'Transfer Out'),
        ('Transfer In', 'Transfer In'),
        ('Service Fee', 'Service Fee'),
    ]

    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} - {self.timestamp}"
