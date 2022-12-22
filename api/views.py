from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from mailing.tasks import send_mail

from core.models import (Account, MoneyTransfer, Bank)


class TransferApiView(APIView):
    def post(self, request, *args, **kwargs):

        transfer = MoneyTransfer.objects.create_transfer(
            from_user=request.data['from_user'],
            from_account=request.data['from_account'],
            to_user=request.data['to_user'],
            to_account=request.data['to_account'],
            bank=request.data['bank'],
            transfer_purpose=request.data['transfer_purpose'],
            money=request.data['money']
        )

        from_user_account = Account.objects.get(account=transfer.from_account)
        from_user_account.set_minus_balance(int(transfer.money))

        to_user_account = Account.objects.get(account=transfer.to_account)
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