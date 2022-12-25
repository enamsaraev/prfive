from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from mailing.tasks import send_mail

from core.models import (
    Account, MoneyTransferToClient, MoneyTransferToCompany, 
    TransferToClientData, TransferToCompanyData,
    MoneyAccount, Company, Bank)

from api.serializers import TransferToClientTableData, TransferToCompanyTableData


class TransfeToClientrApiView(APIView):
    def post(self, request, *args, **kwargs):

        transfer = self.create_transfer(request)
        from_user_account, to_user_account = self.solve_money(transfer)

        
        send_mail.delay(
            to=from_user_account.user_account.email,
            message=f'С Вашего счета списали {transfer.money} и отправили {transfer.to_user}',
            subject='Списание средств',
            transfer_id=str(transfer.id)
        )
        send_mail.delay(
            to=to_user_account.user_account.email,
            message=f'На Ваш счет зачислили {transfer.money} от {transfer.from_user}',
            subject='Зачисление средств',
            transfer_id=str(transfer.id)
        )

        return Response(status=status.HTTP_201_CREATED)

    @classmethod
    def create_transfer(self, request) -> object:
        
        transfer = MoneyTransferToClient.objects.create(
            from_user=request.data['from_user'],
            from_account=request.data['from_account'],
            to_user=request.data['to_user'],
            to_account=request.data['to_account'],
            bank=request.data['bank'],
            transfer_purpose=request.data['transfer_purpose'],
            money=request.data['money']
        )

        return transfer

    @classmethod
    def solve_money(self, transfer: MoneyTransferToClient):

        from_user_account = MoneyAccount.objects.get(account=transfer.from_account)
        from_user_account.set_minus_balance(int(transfer.money))

        to_user_account = MoneyAccount.objects.get(account=transfer.to_account)
        to_user_account.set_plus_balance(int(transfer.money))

        return from_user_account, to_user_account


class TransferToCompanyApiView(APIView):
    def post(self, request, *args, **kwargs):

        transfer = self.create_transfer(request)
        from_user_account, company = self.solve_money(transfer)

        send_mail.delay(
            to=from_user_account.user_account.email,
            message=f'С Вашего счета списали {transfer.money} и отправили {company.name}',
            subject='Списание средств',
            transfer_id=str(transfer.id)
        )

        return Response(status=status.HTTP_201_CREATED)

    @classmethod
    def create_transfer(self, request) -> object:

        transfer = MoneyTransferToCompany.objects.create(
            fio=request.data['fio'],
            user_account=request.data['user_account'],
            user_bank=request.data['user_bank'],
            company=request.data['company'],
            company_account=request.data['company_account'],
            company_bank=request.data['company_bank'],
            transfer_purpose=request.data['transfer_purpose'],
            money=request.data['money'],
        )

        return transfer

    @classmethod
    def solve_money(self, transfer: MoneyTransferToCompany):

        from_user_account = MoneyAccount.objects.get(account=transfer.user_account)
        from_user_account.set_minus_balance(int(transfer.money))

        company = Company.objects.get(account=transfer.company_account)
        company.set_plus_balance(int(transfer.money))

        return from_user_account, company



class TransfetTable(APIView):
    """Table Transfer"""

    def get(self, request, *args, **kwargs):
        """Returns a data for the analitic table"""

        data = TransferToClientData.objects.all().order_by('-created_at')
        serializer = TransferToClientTableData(data, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class TransfetToCompanyTable(APIView):
    """Table Transfer"""

    def get(self, request, *args, **kwargs):
        """Returns a data for the analitic table"""

        data = TransferToCompanyData.objects.all().order_by('-created_at')
        serializer = TransferToCompanyTableData(data, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

        

        