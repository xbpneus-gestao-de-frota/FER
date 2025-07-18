"""
URL configuration for XBPNEUS Premium project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from xbpneus.views import painel_cliente
from xbpneus.views_redirect import (
    transportador_redirect, 
    area_cliente_redirect, 
    health_check,
    root_redirect
)
from xbpneus.core.views_pilares import (
    central_estoque,
    central_manutencao,
    central_eventos,
    central_noticias,
    central_relatorios,
    central_compras,
    central_financeiro
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('painel/', painel_cliente, name='painel_cliente'),
    
    # Pilares do Sistema - Telas Centrais
    path('frota/', include('xbpneus.apps.frota.urls')),
    path('estoque/', central_estoque, name='central_estoque'),
    path('manutencao/', central_manutencao, name='central_manutencao'),
    path('eventos/', central_eventos, name='central_eventos'),
    path('noticias/', central_noticias, name='central_noticias'),
    path('relatorios/', central_relatorios, name='central_relatorios'),
    path('compras/', central_compras, name='central_compras'),
    path('financeiro/', central_financeiro, name='central_financeiro'),
    
    # Configurações
    path('painel/configuracoes/', include(('xbpneus.apps.configuracoes.urls', 'configuracoes'), namespace='configuracoes')),
    
    # Rotas de redirecionamento para integração com site principal
    path('transportador/', transportador_redirect, name='transportador_redirect'),
    path('area-cliente/', area_cliente_redirect, name='area_cliente_redirect'),
    path('area-do-cliente/', area_cliente_redirect, name='area_do_cliente_redirect'),
    path('health/', health_check, name='health_check'),
    
    # Apps do sistema - Comentados até serem implementados
    # path('produtos/', include('xbpneus.apps.produtos.urls')),
    # path('servicos/', include('xbpneus.apps.servicos.urls')),
    # path('contato/', include('xbpneus.apps.contato.urls')),
    
    # Página inicial - deve ser a última
    path('', root_redirect, name='root_redirect'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Admin customization
admin.site.site_header = 'XBPNEUS Premium Admin'
admin.site.site_title = 'XBPNEUS Admin'
admin.site.index_title = 'Painel Administrativo'

