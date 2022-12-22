from django.urls import path

from api.views import TransferApiView

urlpatterns = [
    path('transfer-create/', TransferApiView.as_view(), name='set_transfer'),
]

app_name = 'api'