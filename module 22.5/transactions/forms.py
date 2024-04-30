from typing import Any
from django import forms
from .models import Transaction


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'transaction_type']

    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop('account')
        super().__init__(*args, **kwargs)
        self.fields['transaction_type'].disabled = True
        self.fields['transaction_type'].widget = forms.HiddenInput()

    def save(self, commit=True):
        self.instance.account = self.account
        self.instance.balance_after_transaction = self.account.balance
        return super().save()
    

class DepositForm(TransactionForm):
    def clean_amount(self):
        min_deposit_amount= 100
        amount = self.cleaned_data.get('amount')
        if amount < min_deposit_amount:
            raise forms.ValidationError(
                f'You need to deposit at least TK. {min_deposit_amount}'
            )
        return amount


class WithdrawForm(TransactionForm):
    def clean_amount(self):
        account = self.account
        min_withdraw_amount = 500
        max_withdraw_amount = 2000000
        balance = account.balance
        amount = self.cleaned_data.get('amount')
        if amount < min_withdraw_amount:
            raise forms.ValidationError(
                f'You can withdraw at least TK. {min_withdraw_amount}'
            )
        
        if amount > max_withdraw_amount:
            raise forms.ValidationError(
                f'You can withdraw maximum Tk. {max_withdraw_amount} at a time'
            )
        
        if amount > balance :
            raise forms.ValidationError(
                f'You have TK. {balance} in your account. '
                'You can not withdraw more then your account balance'
            )
        return amount
    


class LoanRequestForm(TransactionForm):
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')

        return amount
    
class TransferAnotherAcc(TransactionForm):
    receiver_account = forms.CharField(required=True)
    class Meta:
        model = Transaction
        fields = ['amount', 'receiver_account', 'transaction_type']


    def clean_amount(self):
        amount = self.cleaned_data.get("amount")
        min_transfer_amount = 100
        if amount < min_transfer_amount :
            raise forms.ValidationError(f'The minimum transfer amount is TK. {min_transfer_amount}')
        
        return amount
    
    