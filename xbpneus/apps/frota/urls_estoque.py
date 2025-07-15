from django.urls import path
from . import views_estoque

app_name = 'estoque'

urlpatterns = [
    # Dashboard do estoque
    path('', views_estoque.dashboard_estoque, name='dashboard'),
    
    # Gestão do estoque
    path('lista/', views_estoque.listar_estoque, name='listar'),
    path('cadastrar/', views_estoque.cadastrar_pneu_estoque, name='cadastrar'),
    path('detalhes/<int:pneu_id>/', views_estoque.detalhes_pneu_estoque, name='detalhes'),
    
    # Vinculação de pneus
    path('vincular/', views_estoque.vincular_pneu, name='vincular'),
    path('remover/<int:vinculacao_id>/', views_estoque.remover_pneu, name='remover'),
    path('atualizar-sulco/<int:vinculacao_id>/', views_estoque.atualizar_sulco, name='atualizar_sulco'),
    
    # Relatórios
    path('relatorio/', views_estoque.relatorio_estoque, name='relatorio'),
    
    # APIs
    path('api/pneus-disponiveis/', views_estoque.api_pneus_disponiveis, name='api_pneus_disponiveis'),
]

