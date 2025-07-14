from django.urls import path
from . import views

app_name = 'subusuarios'

urlpatterns = [
    # Listagem
    path('', views.listar_subusuarios, name='listar_subusuarios'),
    
    # Cadastro
    path('novo/', views.cadastrar_subusuario, name='cadastrar_subusuario'),
    
    # Edição
    path('<int:subusuario_id>/editar/', views.editar_subusuario, name='editar_subusuario'),
    
    # Exclusão
    path('<int:subusuario_id>/excluir/', views.excluir_subusuario, name='excluir_subusuario'),
    
    # Alternar status
    path('<int:subusuario_id>/alternar-status/', views.alternar_status_subusuario, name='alternar_status_subusuario'),
]

