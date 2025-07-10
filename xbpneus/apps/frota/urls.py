from django.urls import path
from . import views

app_name = 'frota'

urlpatterns = [
    # Dashboard
    path('', views.dashboard_frota, name='dashboard'),
    
    # Veículos
    path('veiculos/', views.listar_veiculos, name='listar_veiculos'),
    path('veiculos/cadastrar/', views.cadastrar_veiculo, name='cadastrar_veiculo'),
    path('veiculos/<int:veiculo_id>/', views.detalhes_veiculo, name='detalhes_veiculo'),
    path('veiculos/<int:veiculo_id>/editar/', views.editar_veiculo, name='editar_veiculo'),
    
    # Pneus
    path('pneus/', views.listar_pneus, name='listar_pneus'),
    path('pneus/cadastrar/', views.cadastrar_pneu, name='cadastrar_pneu'),
    path('pneus/cadastrar/<int:veiculo_id>/', views.cadastrar_pneu, name='cadastrar_pneu_veiculo'),
    path('pneus/<int:pneu_id>/editar/', views.editar_pneu, name='editar_pneu'),
    
    # Relatórios
    path('relatorios/', views.relatorios, name='relatorios'),
]

