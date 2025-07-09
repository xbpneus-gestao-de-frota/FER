"""
URL configuration for XBPNEUS Premium project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('xbpneus.apps.home.urls')),
    path('produtos/', include('xbpneus.apps.produtos.urls')),
    path('servicos/', include('xbpneus.apps.servicos.urls')),
    path('contato/', include('xbpneus.apps.contato.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Admin customization
admin.site.site_header = 'XBPNEUS Premium Admin'
admin.site.site_title = 'XBPNEUS Admin'
admin.site.index_title = 'Painel Administrativo'

