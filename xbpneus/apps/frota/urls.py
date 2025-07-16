from django.urls import path, include
from . import views

app_name = 'frota'

urlpatterns = [
    # Dashboard da Frota
    path('', views.dashboard_frota, name='dashboard'),
    
    # Frota (antigo: veículos)
    path('veiculos/', views.listar_veiculos, name='listar_veiculos'),  # Manter para compatibilidade
    path('veiculos/cadastrar/', views.cadastrar_veiculo, name='cadastrar_veiculo'),  # Manter para compatibilidade
    path('veiculos/<int:veiculo_id>/', views.detalhes_veiculo, name='detalhes_veiculo'),  # Manter para compatibilidade
    path('veiculos/<int:veiculo_id>/editar/', views.editar_veiculo, name='editar_veiculo'),  # Manter para compatibilidade
    
    # Novas rotas da Frota
    path('lista/', views.listar_veiculos, name='listar_frota'),
    path('cadastrar/', views.cadastrar_veiculo, name='cadastrar_frota'),
    path('<int:veiculo_id>/', views.detalhes_veiculo, name='detalhes_frota'),
    path('<int:veiculo_id>/editar/', views.editar_veiculo, name='editar_frota'),
    
    # Estoque de Pneus (novo sistema principal)
    path('estoque/', include('xbpneus.apps.frota.urls_estoque')),
    
    # Pneus (sistema antigo - redirecionamento para estoque)
    path('pneus/', views.listar_pneus, name='listar_pneus'),  # Manter para compatibilidade
    path('pneus/cadastrar/', views.cadastrar_pneu, name='cadastrar_pneu'),  # Manter para compatibilidade
    path('pneus/cadastrar/<int:veiculo_id>/', views.cadastrar_pneu, name='cadastrar_pneu_veiculo'),  # Manter para compatibilidade
    path('pneus/<int:pneu_id>/editar/', views.editar_pneu, name='editar_pneu'),  # Manter para compatibilidade
    
    # Relatórios
    path('relatorios/', views.relatorios, name='relatorios'),
]

