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
    
    # Exclusão
    path('<int:subusuario_id>/excluir/', views.excluir_subusuario, name='excluir_subusuario'),
    
    # Alternar status (AJAX)
    path('<int:subusuario_id>/toggle-ativo/', views.toggle_ativo_subusuario, name='toggle_ativo_subusuario'),
    
    # === FLUXO DE CONVITE ===
    # Enviar convite por e-mail
    path('<int:subusuario_id>/enviar-convite/', views.enviar_convite, name='enviar_convite'),
    
    # Reenviar convite
    path('<int:subusuario_id>/reenviar-convite/', views.reenviar_convite, name='reenviar_convite'),
    
    # Definir senha (acesso público via token)
    path('definir-senha/<uuid:token>/', views.definir_senha, name='definir_senha'),
    
    # === AJAX ENDPOINTS ===
    # Módulos de perfil
    path('ajax/perfil/<int:perfil_id>/modulos/', views.ajax_modulos_perfil, name='ajax_modulos_perfil'),
    
    # Validações
    path('ajax/validar-login/', views.ajax_validar_login, name='ajax_validar_login'),
    path('ajax/validar-email/', views.ajax_validar_email, name='ajax_validar_email'),
]

