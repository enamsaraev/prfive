from django.db import models

from core.models import Account, Bank, MoneyTransferToClient


class EmailEntry(models.Model):
    msg_number = models.CharField(
        max_length=30,
        blank=False,
        null=False
    )
    user = models.ForeignKey(
        Account,
        related_name='msgs',
        on_delete=models.SET_NULL,
        null=True,
    )
    theme = models.CharField(
        max_length=255,
        blank=False,
        null=False
    )
    text = models.TextField()
