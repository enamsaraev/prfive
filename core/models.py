from django.db import models
from django.contrib.auth.models import User


class MoneyTransferManager(models.Manager):
    """Money transfer model manager"""

    def create_transfer(
        self, 
        from_user: str,
        from_account: str,
        to_user: str,
        to_account: str,
        bank: str,
        transfer_purpose: str,
        money: str,
    ):

        transfer = self.model(
            from_user=Account.objects.get(account=from_account),
            from_account=from_account,
            to_user=Account.objects.get(account=to_account),
            to_account=to_account,
            bank=Bank.objects.get(bank=bank),
            money=money,
            transfer_purpose=transfer_purpose
        )
        transfer.save()

        return transfer


class Account(models.Model):
    """User's account"""

    user = models.ForeignKey(
        User,
        related_name='account',
        on_delete=models.SET_NULL,
        null=True,
    )
    email = models.EmailField(default='')
    created_at = models.DateTimeField()
    account = models.CharField(
        max_length=20,
        blank=False,
        null=False,
    )
    balance = models.CharField(
        max_length=20,
        blank=False,
        null=False,
    )

    def __str__(self) -> str:
        return self.user.username

    def set_minus_balance(self, money: int):
        """Minus money from users balance"""

        balance = int(self.balance) - money
        self.balance = str(balance)

        self.save(update_fields=['balance'])

    def set_plus_balance(self, money: int):
        """Minus money from users balance"""
        
        balance = int(self.balance) + money
        self.balance = str(balance)

        self.save(update_fields=['balance'])


class Bank(models.Model):
    """Bank model"""

    bank = models.CharField(max_length=150)
    bik = models.CharField(
        max_length=9,
        blank=False,
        null=False,
    )
    account = models.CharField(
        max_length=20,
        blank=False,
        null=False,
    )
    inn = models.CharField(
        max_length=10,
        blank=False,
        null=False,
    )
    kpp = models.CharField(
        max_length=9,
        blank=False,
        null=False,
    )
    money_transfer_comission = models.IntegerField()
    info = models.TextField()

    def __str__(self) -> str:
        return self.bank


class MoneyTransfer(models.Model):
    """Money transfer model"""

    from_user = models.ForeignKey(
        'Account',
        related_name='transfers_from',
        on_delete=models.SET_NULL,
        null=True,
    )
    from_account = models.CharField(
        max_length=30,
        blank=False,
        null=False
    )
    to_user = models.ForeignKey(
        'Account',
        related_name='transfers_to',
        on_delete=models.SET_NULL,
        null=True,
    )
    to_account = models.CharField(
        max_length=30,
        blank=False,
        null=False
    )
    bank = models.ForeignKey(
        'Bank',
        related_name='transfers_bank',
        on_delete=models.SET_NULL,
        null=True,
    )
    transfer_purpose = models.TextField()
    money = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = MoneyTransferManager()

    def __str__(self) -> str:
        return str(self.created_at)
