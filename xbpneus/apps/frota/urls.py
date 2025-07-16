from django.urls import path, include
from . import views
from django.shortcuts import redirect

app_name = 'frota'

# Views de redirecionamento para compatibilidade
def redirect_veiculos_lista(request):
    return redirect('frota:listar_frota')

def redirect_veiculos_cadastrar(request):
    return redirect('frota:cadastrar_frota')

def redirect_veiculos_detalhes(request, veiculo_id):
    return redirect('frota:detalhes_frota', veiculo_id=veiculo_id)

def redirect_veiculos_editar(request, veiculo_id):
    return redirect('frota:editar_frota', veiculo_id=veiculo_id)

def redirect_pneus_para_estoque(request):
    return redirect('estoque:dashboard')

urlpatterns = [
    # Dashboard da Frota (rota raiz)
    path('', views.listar_veiculos, name='dashboard'),
    
    # Rotas principais da Frota (nova nomenclatura)
    path('lista/', views.listar_veiculos, name='listar_frota'),
    path('cadastrar/', views.cadastrar_veiculo, name='cadastrar_frota'),
    path('detalhes/<int:veiculo_id>/', views.detalhes_veiculo, name='detalhes_frota'),
    path('editar/<int:veiculo_id>/', views.editar_veiculo, name='editar_frota'),
    
    # Estoque de Pneus (sistema principal)
    path('estoque/', include('xbpneus.apps.frota.urls_estoque')),
    
    # Relatórios
    path('relatorios/', views.relatorios, name='relatorios'),
    
    # === ROTAS DE COMPATIBILIDADE (redirecionamentos) ===
    # Frota (antigo: veículos)
    path('veiculos/', redirect_veiculos_lista, name='listar_veiculos'),
    path('veiculos/cadastrar/', redirect_veiculos_cadastrar, name='cadastrar_veiculo'),
    path('veiculos/<int:veiculo_id>/', redirect_veiculos_detalhes, name='detalhes_veiculo'),
    path('veiculos/<int:veiculo_id>/editar/', redirect_veiculos_editar, name='editar_veiculo'),
    
    # Pneus (redirecionamento para estoque)
    path('pneus/', redirect_pneus_para_estoque, name='listar_pneus'),
    path('pneus/cadastrar/', redirect_pneus_para_estoque, name='cadastrar_pneu'),
    path('pneus/cadastrar/<int:veiculo_id>/', redirect_pneus_para_estoque, name='cadastrar_pneu_veiculo'),
    path('pneus/<int:pneu_id>/editar/', redirect_pneus_para_estoque, name='editar_pneu'),
]

