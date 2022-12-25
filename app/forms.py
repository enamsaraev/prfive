from django.forms import (
    Form, ModelForm, CharField, EmailField, HiddenInput, 
    PasswordInput, TextInput, ChoiceField, Select
)

from core.models import Company, Bank

BANKS = [(bank.bank, bank.bank)  for bank in Bank.objects.all()]
COMPANIES = [(comapny.name, comapny.name) for comapny in Company.objects.all()]
# BANKS = ''
# COMPANIES = ''


class LoginForm(Form):
    username = CharField(
        max_length=150, 
        min_length=4,
        widget=TextInput(attrs={
            'id': 'user',
            'placeholder': 'user'}
        )
    )
    password = CharField(
        max_length=128, 
        min_length=4,
        widget=TextInput(attrs={
            'id': 'pass',
            'placeholder': 'password'}
        )
    )
    

class TransferToClientForm(Form):

    GEEKS_CHOICES =(
        BANKS
    )

    from_user = CharField(
        max_length=150, 
        min_length=4,
        widget=TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Отправитель'}
        )
    )
    from_account = CharField(
        max_length=30,
        widget=TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Счет отправителя'}
        )
    )
    to_user = CharField(
        max_length=150, 
        min_length=4,
        widget=TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Получатель'}
        )
    )
    to_account = CharField(
        max_length=30, 
        min_length=4,
        widget=TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Счет получателя'}
        )
    )
    bank = ChoiceField(
        choices = GEEKS_CHOICES,
        widget=Select(attrs={
            'class': 'form-select mt-3',
            'placeholder': 'Банк получателя'}
        )
    )
    transfer_purpose = CharField(
        max_length=1000, 
        min_length=4,
        widget=TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Назначение перевода'}
        )
    )
    money = CharField(
        max_length=20, 
        min_length=4,
        widget=TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Сумма'}
        )
    )

class TransferToCompanyForm(Form):

    GEEKS_CHOICES_BANKS =(
        BANKS
    )
    GEEKS_CHOICES_COMPANIES =(
        COMPANIES
    )

    fio = CharField(
        max_length=150, 
        min_length=4,
        widget=TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Отправитель'}
        )
    )
    user_account = CharField(
        max_length=30,
        widget=TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Счет отправителя'}
        )
    )
    user_bank = ChoiceField(
        choices = GEEKS_CHOICES_BANKS,
        widget=Select(attrs={
            'class': 'form-select mt-3',
            'placeholder': 'Банк получателя'}
        )
    )
    company = ChoiceField(
        choices = GEEKS_CHOICES_COMPANIES,
        widget=Select(attrs={
            'class': 'form-select mt-3',
            'placeholder': 'Наименование организации'}
        )
    )
    company_account = CharField(
        max_length=30,
        widget=TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Счет организации'}
        )
    )
    company_bank = ChoiceField(
        choices = GEEKS_CHOICES_BANKS,
        widget=Select(attrs={
            'class': 'form-select mt-3',
            'placeholder': 'Банк получателя'}
        )
    )
    transfer_purpose = CharField(
        max_length=1000, 
        min_length=4,
        widget=TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Назначение перевода'}
        )
    )
    money = CharField(
        max_length=20, 
        min_length=4,
        widget=TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Сумма'}
        )
    )