import requests
import pandas as pd

from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

from core.models import Account, MoneyAccount, Company, Bank, MoneyTransferToClient, MoneyTransferToCompany

from app.forms import LoginForm, TransferToClientForm, TransferToCompanyForm

class LoginView(TemplateView):
    template_name = 'login.html'
    form_class = LoginForm

    def get(self, request, *args, **kwarg):
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request, *args, **kwarg):
        form = self.form_class(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                """Auth user"""

                login(request, user)
                userdata = {'username': username, 'password': password}

                response = requests.post("http://localhost:8000/api-token-auth/", data=userdata)
                
                obj = response.json()
                request.session['token'] = obj['token']
                request.session.modified = True

            else:
                messages.error(request, "Your login data is not valid")
                return render(request, self.template_name, {"form": form})

        return redirect(reverse("app:menu"))


class MenuView(TemplateView):
    template_name = 'menu.html'

    def get(self, request, *args, **kwarg):
        if request.user.is_authenticated:
            return render(request, self.template_name)
        else:
            return redirect(reverse("app:login"))


class TransfersToClientView(TemplateView):
    template_name = 'transfers/transfers_to_client.html'
    form_class = TransferToClientForm

    def get(self, request, *args, **kwarg):
        if request.user.is_authenticated:
            return render(request, self.template_name, {'form': self.form_class})
        else:
            return redirect(reverse("app:login"))

    def post(self, request, *args, **kwarg):
        if request.user.is_authenticated:
            form = self.form_class(request.POST)

            if form.is_valid():
                sender = Account.objects.filter(
                    fio=form.cleaned_data['from_user'],
                    money_account=MoneyAccount.objects.get(account=form.cleaned_data['from_account'])
                ).exists()
                recipient = Account.objects.filter(
                    fio=form.cleaned_data['to_user'],
                    money_account=MoneyAccount.objects.get(account=form.cleaned_data['to_account'])
                ).exists()

                if sender and recipient:

                    data = dict(
                        from_user=form.cleaned_data['from_user'],
                        from_account=form.cleaned_data['from_account'],
                        to_user=form.cleaned_data['to_user'],
                        to_account=form.cleaned_data['to_account'],
                        bank=form.cleaned_data['bank'],
                        transfer_purpose=form.cleaned_data['transfer_purpose'],
                        money=form.cleaned_data['money'],
                    )

                    headers = {'Authorization': 'JWT ' + request.session["token"]}
                    
                    response = requests.post(
                        "http://localhost:8000" + reverse("api:transfers-to-client"),
                        data=data,
                        headers=headers,
                    )

                    if response.status_code != 200:
                        error_message = "Update have not been succeeded"
                        messages.error(request, error_message)

            return render(request, self.template_name, {"form": self.form_class})
                        


class TransferToCompanyView(TemplateView):
    template_name = 'transfers/transfers_to_company.html'
    form_class = TransferToCompanyForm

    def get(self, request, *args, **kwarg):
        if request.user.is_authenticated:
            return render(request, self.template_name, {'form': self.form_class})
        else:
            return redirect(reverse("app:login"))

    def post(self, request, *args, **kwarg):
        if request.user.is_authenticated:
            form = self.form_class(request.POST)

            if form.is_valid():

                sender = Account.objects.filter(
                    fio=form.cleaned_data['fio'],
                    money_account=MoneyAccount.objects.get(account=form.cleaned_data['user_account'])
                ).exists()
                recipient = Company.objects.filter(
                    account=form.cleaned_data['company_account']
                ).exists()

                if sender and recipient:

                    data = dict(
                        fio=form.cleaned_data['fio'],
                        user_account=form.cleaned_data['user_account'],
                        user_bank=form.cleaned_data['user_bank'],
                        company=form.cleaned_data['company'],
                        company_account=form.cleaned_data['company_account'],
                        company_bank=form.cleaned_data['company_bank'],
                        transfer_purpose=form.cleaned_data['transfer_purpose'],
                        money=form.cleaned_data['money'],
                    )

                    headers = {'Authorization': 'JWT ' + request.session["token"]}
                    
                    response = requests.post(
                        "http://localhost:8000" + reverse("api:transfers-to-company"),
                        data=data,
                        headers=headers,
                    )
                    
                    if response.status_code != 200:
                        error_message = "Update have not been succeeded"
                        messages.error(request, error_message)

            return render(request, self.template_name, {"form": self.form_class})



class TransferAnalytics(TemplateView):
    template_name = 'transfers/transfers-analitics.html'

    def get(self, request, *args, **kwarg):
        if request.user.is_authenticated:

            headers = {'Authorization': 'JWT ' + request.session["token"]}
                
            response = requests.get(
                "http://localhost:8000" + reverse("api:transfer-analitics"),
                headers=headers,
            )
            data = response.json()
            
            return render(request, self.template_name, {'data': data})


class TransferAnalyticsToCompany(TemplateView):
    template_name = 'transfers/transfer-analitics-to-company.html'

    def get(self, request, *args, **kwarg):
        if request.user.is_authenticated:

            headers = {'Authorization': 'JWT ' + request.session["token"]}
                
            response = requests.get(
                "http://localhost:8000" + reverse("api:transfer-analitics-to-company"),
                headers=headers,
            )
            data = response.json()
            
            return render(request, self.template_name, {'data': data})

        else:
            return redirect(reverse("app:login"))


class GuideView(TemplateView):
    template_name = 'guides/guide.html'

    def get(self, request, *args, **kwarg):
        """Prepares data for the guide book"""
        if request.user.is_authenticated:

            context = {
                'account': MoneyAccount.objects.all(),
                'bank': Bank.objects.all(),
                'company': Company.objects.all(),
            }

            return render(request, self.template_name, context)
        
        else:
            return redirect(reverse("app:login"))


class ClientOrderView(TemplateView):
    """"""
    
    template_name = 'pay-order.html'

    def get(self, request, *args, **kwarg):
        if request.user.is_authenticated:
            mtc = MoneyTransferToClient.objects.last()
            context = {
                'from_user': MoneyAccount.objects.get(account=mtc.from_account),
                'to_user': MoneyAccount.objects.get(account=mtc.to_account),
                'ctx': mtc,
            }
            ctx = MoneyTransferToClient.objects.last()
            return render(request, self.template_name, context)
        else:
            return redirect(reverse("app:login"))


class CompanyOrderView(TemplateView):
    """"""
    template_name = 'payment-order.html'

    def get(self, request, *args, **kwarg):
        if request.user.is_authenticated:
            mtcomp = MoneyTransferToCompany.objects.last()
            context = {
                'ctx': mtcomp,
                'acc': MoneyAccount.objects.get(account=mtcomp.user_account),
                'bank': Bank.objects.get(bank=mtcomp.company_bank),
                'company': Company.objects.get(account=mtcomp.company_account),
            }
            return render(request, self.template_name, context)
        else:
            return redirect(reverse("app:login"))


class CreateFile(TemplateView):
    def get(self, request, *args, **kwargs):
        headers = {'Authorization': 'JWT ' + request.session["token"]}
        company_response = requests.get(
                "http://localhost:8000" + reverse("api:transfer-analitics-to-company"),
                headers=headers,
            )
        company_data = company_response.json()

        company_df = pd.DataFrame({
            'Отправитель': [company_data[item]['user'] for item in range(len(company_data))],
            'Банк отправителя': [company_data[item]['user_bank'] for item in range(len(company_data))],
            'Наименование организации': [company_data[item]['company'] for item in range(len(company_data))],
            'Банк организации': [company_data[item]['company_bank'] for item in range(len(company_data))],
            'Сумма перевода': [company_data[item]['money'] for item in range(len(company_data))],
        })

        company_df.to_excel('static/xl/payments-to-company.xlsx')


        client_response = requests.get(
                "http://localhost:8000" + reverse("api:transfer-analitics"),
                headers=headers,
            )
        client_data = client_response.json()

        client_df = pd.DataFrame({
            'Счет отправителя': [client_data[item]['from_account'] for item in range(len(client_data))],
            'Счет получателя': [client_data[item]['to_account'] for item in range(len(client_data))],
            'Банк': [client_data[item]['bank'] for item in range(len(client_data))],
            'Сумма перевода': [client_data[item]['money'] for item in range(len(client_data))],
        })

        client_df.to_excel('static/xl/payments-to-client.xlsx')


        return redirect(reverse("app:menu"))
