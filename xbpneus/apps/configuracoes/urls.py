from django.urls import path, include
from . import views

app_name = 'configuracoes'

urlpatterns = [
    # Dashboard principal das configurações
    path('', views.dashboard_configuracoes, name='dashboard'),
    
    # Configurações da empresa
    path('empresa/', views.configuracao_empresa, name='empresa'),
    
    # Preferências do usuário
    path('preferencias/', views.preferencias_usuario, name='preferencias'),
    
    # Subusuários (incluído como submenu)
    path('subusuarios/', include('xbpneus.apps.subusuarios.urls')),
]

