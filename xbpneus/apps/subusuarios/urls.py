from django.urls import path
from . import views

app_name = 'subusuarios'

urlpatterns = [
    # === SUBUSUÁRIOS ===
    # Listagem
    path('', views.listar_subusuarios, name='listar_subusuarios'),
    
    # Cadastro
    path('novo/', views.cadastrar_subusuario, name='cadastrar_subusuario'),
    
    # Edição
    path('<int:subusuario_id>/editar/', views.editar_subusuario, name='editar_subusuario'),
    
    # Detalhes
    path('<int:subusuario_id>/', views.detalhes_subusuario, name='detalhes_subusuario'),
    
    # Exclusão
    path('<int:subusuario_id>/excluir/', views.excluir_subusuario, name='excluir_subusuario'),
    
    # Alternar status (AJAX)
    path('<int:subusuario_id>/toggle-ativo/', views.toggle_ativo_subusuario, name='toggle_ativo_subusuario'),
    
    # === MÓDULOS DE ACESSO ===
    path('modulos/', views.listar_modulos, name='listar_modulos'),
    path('modulos/novo/', views.cadastrar_modulo, name='cadastrar_modulo'),
    
    # === PERFIS DE ACESSO ===
    path('perfis/', views.listar_perfis, name='listar_perfis'),
    path('perfis/novo/', views.cadastrar_perfil, name='cadastrar_perfil'),
    path('perfis/<int:perfil_id>/editar/', views.editar_perfil, name='editar_perfil'),
    
    # === APIs AJAX ===
    path('api/perfil/<int:perfil_id>/modulos/', views.api_perfil_modulos, name='api_perfil_modulos'),
]

