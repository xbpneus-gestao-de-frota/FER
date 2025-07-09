from django.contrib import admin
from django.utils import timezone
from .models import Contato


@admin.register(Contato)
class ContatoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'email', 'assunto', 'respondido', 'created_at']
    list_filter = ['assunto', 'respondido', 'created_at']
    search_fields = ['nome', 'email', 'mensagem']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Informações do Contato', {
            'fields': ('nome', 'email', 'telefone', 'assunto', 'mensagem')
        }),
        ('Resposta', {
            'fields': ('respondido', 'resposta', 'data_resposta')
        }),
        ('Datas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def save_model(self, request, obj, form, change):
        if obj.respondido and not obj.data_resposta:
            obj.data_resposta = timezone.now()
        super().save_model(request, obj, form, change)

