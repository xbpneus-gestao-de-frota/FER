from django.contrib import admin
from .models import Servico, Agendamento


@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'preco_base', 'ordem', 'active', 'created_at']
    list_filter = ['active', 'created_at']
    search_fields = ['nome', 'descricao']
    prepopulated_fields = {'slug': ('nome',)}
    list_editable = ['ordem', 'active']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ['nome_cliente', 'servico', 'data_agendamento', 'status', 'created_at']
    list_filter = ['status', 'servico', 'data_agendamento', 'created_at']
    search_fields = ['nome_cliente', 'email_cliente', 'telefone_cliente']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'data_agendamento'

