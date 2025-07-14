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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('painel/', painel_cliente, name='painel_cliente'),
    path('frota/', include('xbpneus.apps.frota.urls')),
    path('painel/subusuarios/', include('xbpneus.apps.subusuarios.urls')),
    
    # Rotas de redirecionamento para integração com site principal
    path('transportador/', transportador_redirect, name='transportador_redirect'),
    path('area-cliente/', area_cliente_redirect, name='area_cliente_redirect'),
    path('area-do-cliente/', area_cliente_redirect, name='area_do_cliente_redirect'),
    path('health/', health_check, name='health_check'),
    
    # Apps do sistema
    path('produtos/', include('xbpneus.apps.produtos.urls')),
    path('servicos/', include('xbpneus.apps.servicos.urls')),
    path('contato/', include('xbpneus.apps.contato.urls')),
    
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

