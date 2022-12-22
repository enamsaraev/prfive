from rest_framework import serializers

from core.models import MoneyTransferToClient, Bank


class TransferToClientTableData(serializers.ModelSerializer):

    bank = serializers.StringRelatedField(source='bank.bank', read_only=True)

    class Meta:
        model = MoneyTransferToClient
        fields = (
            'from_account',
            'to_account',
            'bank',
            'money',
        )

class TransferToCompanyTableData(serializers.ModelSerializer):

    user = serializers.StringRelatedField(source='user.account', read_only=True)
    user_bank = serializers.StringRelatedField(source='user_bank.bank')
    company = serializers.StringRelatedField(source='company.name')
    company_bank = serializers.StringRelatedField(source='company_bank.bank')

    class Meta:
        model = MoneyTransferToClient
        fields = (
            'user',
            'user_bank',
            'company',
            'company_bank',
            'money',
        )