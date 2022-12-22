import requests, json

from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

from app.forms import LoginForm, TransferForm

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


class TransfersView(TemplateView):
    template_name = 'transfers.html'
    form_class = TransferForm

    def get(self, request, *args, **kwarg):
        if request.user.is_authenticated:
            return render(request, self.template_name, {'form': self.form_class})
        else:
            return redirect(reverse("app:login"))

    def post(self, request, *args, **kwarg):
        if request.user.is_authenticated:
            form = self.form_class(request.POST)

            if form.is_valid():
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
                    "http://localhost:8000" + reverse("api:set_transfer"),
                    data=data,
                    headers=headers,
                )

                return render(request, self.template_name, {"form": self.form_class})

        return redirect(reverse("app:login"))