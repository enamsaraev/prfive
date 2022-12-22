from django.urls import path

from app.views import LoginView, MenuView, TransfersView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('menu/', MenuView.as_view(), name='menu'),
    path('transfers/', TransfersView.as_view(), name='transfers'),
]

app_name = 'app'