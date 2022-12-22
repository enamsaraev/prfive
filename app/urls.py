from django.urls import path

from app.views import (
    LoginView, MenuView, TransfersToClientView, TransferToCompanyView, TransferAnalytics, TransferAnalyticsToCompany
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('menu/', MenuView.as_view(), name='menu'),
    path('transfers-to-client/', TransfersToClientView.as_view(), name='transfers-to-client'),
    path('transfers-to-company/', TransferToCompanyView.as_view(), name='transfers-to-company'),
    path('transfer-analytics/', TransferAnalytics.as_view(), name='transfers-analitics'),
    path('transfer-analytics-to-company/', TransferAnalyticsToCompany.as_view(), name='transfers-analitics-to-company'),
]

app_name = 'app'