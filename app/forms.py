from django.forms import (
    Form, ModelForm, CharField, EmailField, HiddenInput, 
    PasswordInput, TextInput, ChoiceField, Select
)

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
    

class TransferForm(Form):

    GEEKS_CHOICES =(
    ("ВТБ", "ВТБ"),
    ("Сбербанк", "Сбербанк"),
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
        max_length=150, 
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