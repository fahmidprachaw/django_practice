from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import CreateView, ListView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Transaction
from .forms import DepositForm, WithdrawForm, LoanRequestForm, TransferAnotherAcc
from .constants import *
from django.contrib import messages
from datetime import datetime
from django.db.models import Sum
from django.urls import reverse_lazy
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.models import User

# Create your views here.

def send_transaction_email(user, amount, subject, template):
    message = render_to_string(template, {
        'user' : user,
        'amount' : amount
    })
    send_email = EmailMultiAlternatives(subject, '', to=[user.email])
    send_email.attach_alternative(message, 'text/html')
    send_email.send()

class TransactionCreateMixin(LoginRequiredMixin, CreateView):
    template_name = 'transactions/transaction_form.html'
    model = Transaction
    title = ''
    success_url = reverse_lazy('transaction_report')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'account' : self.request.user.account,
        })
        return kwargs
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context.update({
            'title': self.title
        })
        return context


class DepositMoneyView(TransactionCreateMixin):
    form_class = DepositForm
    title = 'Deposit'

    def get_initial(self):
        initial = {'transaction_type': DEPOSIT}
        return initial
    
    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        account = self.request.user.account
        account.balance += amount
        account.save(
            update_fields = ['balance']
        )

        messages.success(self.request, f'TK. {amount} deposited to your account successfully')
        # mail_subject = 'Deposite message'
        # message = render_to_string('transactions/deposite_mail.html', {
        #     'user' : self.request.user,
        #     'amount' : amount
        # })
        # to_email = self.request.user.email
        # send_email = EmailMultiAlternatives(mail_subject, '', to=[to_email])
        # send_email.attach_alternative(message, 'text/html')
        # send_email.send()
        send_transaction_email(self.request.user, amount, 'Deposite Message', 'transactions/deposite_mail.html')
        return super().form_valid(form)
    

class WithdrawMoneyView(TransactionCreateMixin):
    form_class = WithdrawForm
    title = 'Withdraw'

    def get_initial(self):
        initial = {'transaction_type': WITHDRAWAL}
        return initial
    
    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        account = self.request.user.account
        account.balance -= amount
        account.save(
            update_fields = ['balance']
        )

        messages.success(self.request, f'TK. {amount} Withdraw from your account successfully')
        send_transaction_email(self.request.user, amount, 'withdrawal Message', 'transactions/withdraw_email.html')
        return super().form_valid(form)
    

class LoanRequestView(TransactionCreateMixin):
    form_class = LoanRequestForm
    title = 'Request for Loan'

    def get_initial(self):
        initial = {'transaction_type': LOAN}
        return initial
    
    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        current_loan_count = Transaction.objects.filter(account=self.request.user.account, transaction_type = LOAN, loan_approve = True).count()

        if current_loan_count >= 3:
            return HttpResponse("You cross the loan limits")
        
        messages.success(self.request, f'Loan Request for amount TK.{amount} has been successfully sent to Bank.')
        send_transaction_email(self.request.user, amount, 'Loan Request Message', 'transactions/loan_request_email.html')
        return super().form_valid(form)



class TransactionReportView(LoginRequiredMixin, ListView):
    template_name = 'transactions/transaction_report.html'
    model = Transaction
    balance = 0

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            account = self.request.user.account
        )

        start_date_str = self.request.GET.get('start_date')
        end_date_str = self.request.GET.get('end_date')

        if start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

            queryset = queryset.filter(timestamp__date__gte = start_date, timestamp__date__lte = end_date)
            self.balance = Transaction.objects.filter(
                timestamp__date__gte=start_date, timestamp__date__lte=end_date
            ).aggregate(Sum('amount'))['amount__sum']

        else:
            self.balance = self.request.user.account.balance

        return queryset.distinct()
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'account': self.request.user.account
        })
        return context
    


class PayLoanView(TransactionCreateMixin, View):
    def get(self, request, loan_id):
        loan = get_object_or_404(Transaction, id = loan_id)

        if loan.loan_approve:
            user_account = loan.account
            if loan.amount < user_account.balance:
                user_account.balance -= loan.amount
                loan.balance_after_transaction = user_account.balance
                user_account.save()
                loan.transaction_type = LOAN_PAID
                loan.save()
                send_transaction_email(self.request.user, '1000', 'Loan Paid Message', 'transactions/loan_paid_email.html')
                return redirect('loan_list')
            else:
                messages.error(self.request, f'Loan amount is grater than available balance')
                return redirect('loan_list')



class LoanListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'transactions/loan_request.html'
    context_object_name = 'loans'


    def get_queryset(self):
        user_account = self.request.user.account
        queryset = Transaction.objects.filter(account = user_account, transaction_type=LOAN)
        return queryset



class TransferView(TransactionCreateMixin):
    form_class = TransferAnotherAcc
    title = 'Transfer Money'

    def get_initial(self):
        initial = {'transaction_type': TRANSFER}
        return initial
    
    def form_valid(self, form):
        sender_account = self.request.user.account
        receiver_account_name = form.cleaned_data.get('receiver_account')
        print("ereceiver_account_name")
        receiver_amount = form.cleaned_data.get('amount')

        try:
            receiver_user = User.objects.get(username=receiver_account_name)
        except User.DoesNotExist:
            messages.error(self.request, "Receiver account not found.")
            return super().form_invalid(form)

        if sender_account.balance < receiver_amount:
            messages.error(self.request, "Insufficient balance for the transfer.")
            return super().form_invalid(form)

        sender_account.balance -= receiver_amount
        sender_account.save(
            update_fields = ['balance']
        )

        receiver_account = receiver_user.account
        receiver_account.balance += receiver_amount
        receiver_account.save(
            update_fields = ['balance']
        )


        messages.success(self.request, f'Transferred TK. {receiver_amount} to {receiver_account} successfully')
        send_transaction_email(self.request.user, receiver_amount, 'Transfer Message', 'transactions/transfer_email.html')
        return super().form_valid(form)



        
        
    
        




    




