from django.contrib import admin
from .models import Account, Transaction

# Register your models here.
# This makes them accessible in the Django Admin panel (http://localhost:8000/admin)

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'account_number', 'balance', 'account_type')
    search_fields = ('user__username', 'account_number', 'mobile_number')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('account', 'transaction_type', 'amount', 'timestamp')
    list_filter = ('transaction_type', 'timestamp')
