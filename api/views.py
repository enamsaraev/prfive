from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from mailing.tasks import send_mail

from core.models import (Account, MoneyTransferToClient, MoneyTransferToCompany, MoneyAccount, Company, Bank)

from api.serializers import TransferToClientTableData, TransferToCompanyTableData


class TransfeToClientrApiView(APIView):
    def post(self, request, *args, **kwargs):

        transfer = MoneyTransferToClient.objects.create_transfer(
            from_user=request.data['from_user'],
            from_account=request.data['from_account'],
            to_user=request.data['to_user'],
            to_account=request.data['to_account'],
            bank=request.data['bank'],
            transfer_purpose=request.data['transfer_purpose'],
            money=request.data['money']
        )

        from_user_account = MoneyAccount.objects.get(account=transfer.from_account)
        from_user_account.set_minus_balance(int(transfer.money))

        to_user_account = MoneyAccount.objects.get(account=transfer.to_account)
        to_user_account.set_plus_balance(int(transfer.money))
        
        send_mail.delay(
            to=from_user_account.email,
            message=f'С Вашего счета списали {transfer.money} и отправили {transfer.to_user}',
            subject='Списание средств',
            transfer_id=str(transfer.id)
        )
        send_mail.delay(
            to=to_user_account.email,
            message=f'На Ваш счет зачислили {transfer.money} от {transfer.from_user}',
            subject='Зачисление средств',
            transfer_id=str(transfer.id)
        )

        return Response(status=status.HTTP_201_CREATED)


class TransferToCompanyApiView(APIView):
    def post(self, request, *args, **kwargs):

        transfer = MoneyTransferToCompany.objects.create_transfer(
            fio=request.data['fio'],
            user_account=request.data['user_account'],
            user_bank=request.data['user_bank'],
            company=request.data['company'],
            company_account=request.data['company_account'],
            company_bank=request.data['company_bank'],
            transfer_purpose=request.data['transfer_purpose'],
            money=request.data['money'],
        )

        from_user_account = MoneyAccount.objects.get(account=request.data['user_account'])
        from_user_account.set_minus_balance(int(transfer.money))

        company = Company.objects.get(account=request.data['company_account'])
        company.set_plus_balance(int(transfer.money))

        send_mail.delay(
            to=from_user_account.email,
            message=f'С Вашего счета списали {transfer.money} и отправили {company.name}',
            subject='Списание средств',
            transfer_id=str(transfer.id)
        )

        return Response(status=status.HTTP_201_CREATED)


class TransfetTable(APIView):
    """Table Transfer"""

    def get(self, request, *args, **kwargs):
        """Returns a data for the analitic table"""

        data = MoneyTransferToClient.objects.all().order_by('-created_at')
        serializer = TransferToClientTableData(data, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class TransfetToCompanyTable(APIView):
    """Table Transfer"""

    def get(self, request, *args, **kwargs):
        """Returns a data for the analitic table"""

        data = MoneyTransferToCompany.objects.all().order_by('-created_at')
        serializer = TransferToCompanyTableData(data, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class GuideApi(APIView):
    """Guide api"""

    def get(self, request, *args, **kwargs):
        account = Account.objects.all()
        bank = Bank.objects.all()
        company = Company.objects.all()

        

        