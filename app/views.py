import requests, json

from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

from core.models import Account, Company

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
                    account=form.cleaned_data['from_account']
                ).exists()
                recipient = Account.objects.filter(
                    fio=form.cleaned_data['to_user'],
                    account=form.cleaned_data['to_account']
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

                    if response.status_code == 201:
                        return render(request, self.template_name, {"form": self.form_class})

        return redirect(reverse("app:login"))


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
                    account=form.cleaned_data['user_account']
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

                    if response.status_code == 201:
                        return render(request, self.template_name, {"form": self.form_class})

        return redirect(reverse("app:login"))


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

        else:
            return redirect(reverse("app:login"))


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