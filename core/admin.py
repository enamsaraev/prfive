from django.contrib import admin
from core import models


@admin.register(models.Account)
class AccountAdmin(admin.ModelAdmin):
    """User's account admin model"""

    list_display = ('user', 'account',)
    list_filter = ('user', 'account',)
    search_fields = ('account',)


@admin.register(models.Company)
class CompantAdmin(admin.ModelAdmin):
    """User's account admin model"""

    list_display = ('name', 'account',)
    list_filter = ('name', 'account',)
    search_fields = ('name', 'account',)


@admin.register(models.Bank)
class Bankdmin(admin.ModelAdmin):
    """User's account admin model"""

    list_display = ('bank', 'bik', 'inn',)
    list_filter = ('bank',)
    search_fields = ('bank',)


@admin.register(models.MoneyTransferToClient)
class MoneyTransferToClientAdmin(admin.ModelAdmin):
    """User's account admin model"""

    list_display = ('from_user', 'from_account', 'to_user', 'to_account', )
    list_filter = ('from_user', 'from_account', 'to_user', 'to_account', )


@admin.register(models.MoneyTransferToCompany)
class MoneyTransferToCompantAdmin(admin.ModelAdmin):
    """User's account admin model"""

    list_display = ('user', 'company', )
    list_filter = ('user', 'company', )