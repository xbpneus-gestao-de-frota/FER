from django.urls import path
from .views import ProdutoListView, ProdutoDetailView, produtos_por_categoria

app_name = 'produtos'

urlpatterns = [
    path('', ProdutoListView.as_view(), name='lista'),
    path('categoria/<slug:categoria_slug>/', produtos_por_categoria, name='categoria'),
    path('<slug:slug>/', ProdutoDetailView.as_view(), name='detalhe'),
]

