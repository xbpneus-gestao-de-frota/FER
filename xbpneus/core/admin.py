from django.contrib import admin
from .models import Configuracao


@admin.register(Configuracao)
class ConfiguracaoAdmin(admin.ModelAdmin):
    list_display = ['chave', 'valor', 'descricao', 'active', 'updated_at']
    list_filter = ['active', 'created_at']
    search_fields = ['chave', 'valor', 'descricao']
    readonly_fields = ['created_at', 'updated_at']

