from django import forms
from django.contrib.auth.models import User
from .models import Account

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    mobile_number = forms.CharField(max_length=15)
    initial_deposit = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0)
    account_type = forms.ChoiceField(choices=[('Savings', 'Savings'), ('Fixed', 'Fixed Deposit')])

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

class DepositForm(forms.Form):
    amount = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0.01)

class WithdrawForm(forms.Form):
    amount = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0.01)

class TransferForm(forms.Form):
    recipient_account = forms.CharField(max_length=20, label="Recipient Account Number")
    amount = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0.01)

    def clean_recipient_account(self):
        acc_no = self.cleaned_data['recipient_account']
        if not Account.objects.filter(account_number=acc_no).exists():
            raise forms.ValidationError("Account not found!")
        return acc_no
