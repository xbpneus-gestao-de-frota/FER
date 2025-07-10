from django.urls import path
from .views import ServicoListView, ServicoDetailView

app_name = 'servicos'

urlpatterns = [
    path('', ServicoListView.as_view(), name='lista'),
    path('<slug:slug>/', ServicoDetailView.as_view(), name='detalhe'),
]

