from rest_framework import serializers

from core.models import TransferToClientData, TransferToCompanyData


class TransferToClientTableData(serializers.ModelSerializer):

    class Meta:
        model = TransferToClientData
        fields = (
            'user',
            'to_user',
            'money',
            'created_at',
        )

class TransferToCompanyTableData(serializers.ModelSerializer):

    class Meta:
        model = TransferToCompanyData
        fields = (
            'user',
            'to_company',
            'money',
            'created_at',
        )