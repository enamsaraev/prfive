
from django.db import models
from django.contrib.auth.models import User


# class MoneyTransferToClientManager(models.Manager):
#     """Money transfer model manager"""

#     def create_transfer(
#         self, 
#         from_user: str,
#         from_account: str,
#         to_user: str,
#         to_account: str,
#         bank: str,
#         transfer_purpose: str,
#         money: str,
#     ):

#         transfer = self.model(
#             from_user=Account.objects.get(account=from_account),
#             from_account=from_account,
#             to_user=Account.objects.get(account=to_account),
#             to_account=to_account,
#             bank=Bank.objects.get(bank=bank),
#             money=money,
#             transfer_purpose=transfer_purpose
#         )
#         transfer.save()

#         return transfer


# class MoneyTransferToCompanyManager(models.Manager):
#     """Money transfer model manager"""

#     def create_transfer(
#         self, 
#         fio: str,
#         user_account: str,
#         user_bank: str,
#         company: str,
#         company_account: str,
#         company_bank: str,
#         transfer_purpose: str,
#         money: str,
#     ):

#         transfer = self.model(
#             user=Account.objects.get(account=user_account),
#             user_bank=Bank.objects.get(bank=user_bank),
#             company=Company.objects.get(account=company_account),
#             company_bank=Bank.objects.get(bank=company_bank),
#             money=money,
#             transfer_purpose=transfer_purpose
#         )
#         transfer.save()

#         return transfer


class TransferToClientDataManager(models.Manager):

    def create_data(
        self, from_account: str, to_account: str, money: str
    ):

        data = self.model(
            user=Account.objects.get(money_account__account=from_account),
            to_user=Account.objects.get(money_account__account=to_account),
            money=money,
        )
        data.save()

        return data


class TransferToCompanyDataManager(models.Manager):

    def create_data(
        self, from_account: str, to_company: str, money: str
    ) -> None:

        data = self.model(
            user=Account.objects.get(money_account__account=from_account),
            to_company=Company.objects.get(account=to_company),
            money=money,
        )
        data.save()

        return data


class Account(models.Model):
    """User's account"""

    user = models.ForeignKey(
        User,
        related_name='account',
        on_delete=models.SET_NULL,
        null=True,
    )
    fio = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        default='',
    )
    email = models.EmailField(default='')
    passport_number = models.CharField(
        max_length=9,
        blank=False,
        null=False,
    )
    passport_data = models.TextField()
    created_at = models.DateTimeField()


    def __str__(self) -> str:
        return self.user.username


class MoneyAccount(models.Model):
    """Account data for user money"""

    ACCOUNT_TYPE = [
        ('Расчетный', 'Расчетный'),
    ]
    ACCOUNT_STATUS = [
        ('Открыт', 'Открыт'),
        ('Закрыт', 'Закрыт'),
    ]
    CURRENCY = [
        ('RUR', 'RUR'),
        ('USD', 'USD'),
        ('EUR', 'EUR'),
    ]

    user_account = models.ForeignKey(
        'Account',
        related_name='money_account',
        on_delete=models.SET_NULL,
        null=True,
    )
    account = models.CharField(
        max_length=20,
        blank=False,
        null=False,
    )
    type = models.CharField(
        max_length=255,
        choices=ACCOUNT_TYPE,
    )
    status = models.CharField(
        max_length=255,
        choices=ACCOUNT_STATUS,
    )
    currency = models.CharField(
        max_length=255,
        choices=CURRENCY,
    )
    balance = models.CharField(
        max_length=20,
        blank=False,
        null=False,
    )

    def __str__(self) -> str:
        return self.account

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

        
class Company(models.Model):
    """Company model"""

    name = models.CharField(
        max_length=255
    )
    email = models.EmailField(
        default='',
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
    bank = models.ForeignKey(
        'Bank',
        related_name='company_bank',
        on_delete=models.SET_NULL,
        null=True,
    )
    bank_bik = models.CharField(
        max_length=9,
        blank=False,
        null=False,
    )
    transfer_purpose = models.TextField()
    money = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def set_plus_balance(self, money: int):
        """Minus money from users balance"""
        
        balance = int(self.money) + money
        self.money = str(balance)

        self.save(update_fields=['money'])


class MoneyTransferToClient(models.Model):
    """Money transfer model"""

    from_user = models.CharField(
        max_length=255,
        blank=False,
        null=False,
    )
    from_account = models.CharField(
        max_length=30,
        blank=False,
        null=False
    )
    to_user = models.CharField(
        max_length=255,
        blank=False,
        null=False,
    )
    to_account = models.CharField(
        max_length=30,
        blank=False,
        null=False
    )
    bank = models.CharField(
        max_length=255,
        blank=False,
        null=False
    )
    transfer_purpose = models.TextField()
    money = models.CharField(
        max_length=20,
        blank=False,
        null=False
    )
    created_at = models.DateTimeField(auto_now_add=True)

    # objects = MoneyTransferToClientManager()

    def __str__(self) -> str:
        return str(self.created_at)


class MoneyTransferToCompany(models.Model):
    """Money transfer model"""

    fio = models.CharField(
        max_length=255,
        blank=False,
        null=False,
    )
    user_account = models.CharField(
        max_length=30,
        blank=False,
        null=False
    )
    user_bank = models.CharField(
        max_length=255,
        blank=False,
        null=False
    )
    company = models.CharField(
        max_length=255,
        blank=False,
        null=False
    )
    company_account = models.CharField(
        max_length=30,
        blank=False,
        null=False
    )
    company_bank = models.CharField(
        max_length=255,
        blank=False,
        null=False
    )
    transfer_purpose = models.TextField()
    money = models.CharField(
        max_length=20,
        blank=False,
        null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # objects = MoneyTransferToCompanyManager()

    def __str__(self) -> str:
        return str(self.created_at)


class TransferToClientData(models.Model):
    """Save info about client-to-client data"""

    user = models.ForeignKey(
        'Account',
        related_name='to_client_transfers',
        on_delete=models.SET_NULL,
        null=True
    )
    to_user = models.ForeignKey(
        'Account',
        related_name='from_client_transfers',
        on_delete=models.SET_NULL,
        null=True
    )
    money = models.CharField(
        max_length=20,
        null=False,
        blank=False
    )
    created_at = models.DateTimeField(auto_now_add=True)

    objects = TransferToClientDataManager()


    def __str__(self) -> str:
        return self.user.fio


class TransferToCompanyData(models.Model):
    """Save info about client-to-client data"""

    user = models.ForeignKey(
        'Account',
        related_name='to_company_transfers',
        on_delete=models.SET_NULL,
        null=True
    )
    to_company = models.ForeignKey(
        'Company',
        related_name='from_client_to_company_transfers',
        on_delete=models.SET_NULL,
        null=True
    )
    money = models.CharField(
        max_length=20,
        null=False,
        blank=False
    )
    created_at = models.DateTimeField(auto_now_add=True)

    objects = TransferToCompanyDataManager()


    def __str__(self) -> str:   
        return self.user.fio