from django.urls import path

from api.views import TransfeToClientrApiView, TransferToCompanyApiView, TransfetTable, TransfetToCompanyTable

urlpatterns = [
    path('api/transfer-create-client/', TransfeToClientrApiView.as_view(), name='transfers-to-client'),
    path('api/transfer-create-company/', TransferToCompanyApiView.as_view(), name='transfers-to-company'),
    path('api/transfer-analics/', TransfetTable.as_view(), name='transfer-analitics'),
    path('api/transfer-analics-to-company/', TransfetToCompanyTable.as_view(), name='transfer-analitics-to-company'),
]

app_name = 'api'