from django.contrib import admin
from core import models


@admin.register(models.Account)
class AccountAdmin(admin.ModelAdmin):
    """User's account admin model"""

    ist_display = ('user', 'account',)
    list_filter = ('user', 'account',)
    search_fields = ('account',)


@admin.register(models.Bank)
class AccountAdmin(admin.ModelAdmin):
    """User's account admin model"""

    ist_display = ('bank', 'bik', 'inn',)
    list_filter = ('bank',)
    search_fields = ('bank',)


@admin.register(models.MoneyTransfer)
class AccountAdmin(admin.ModelAdmin):
    """User's account admin model"""

    ist_display = ('from_user', 'from_account', 'to_user', 'to_account', )
    list_filter = ('from_user', 'from_account', 'to_user', 'to_account', )