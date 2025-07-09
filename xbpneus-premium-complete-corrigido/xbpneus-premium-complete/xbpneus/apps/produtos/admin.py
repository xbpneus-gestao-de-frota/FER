from django.contrib import admin
from .models import Categoria, Marca, Produto


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'active', 'created_at']
    list_filter = ['active', 'created_at']
    search_fields = ['nome', 'descricao']
    prepopulated_fields = {'slug': ('nome',)}


@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'site', 'active', 'created_at']
    list_filter = ['active', 'created_at']
    search_fields = ['nome']


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'marca', 'categoria', 'preco', 'estoque', 'especificacao_completa', 'active']
    list_filter = ['marca', 'categoria', 'active', 'created_at']
    search_fields = ['nome', 'codigo', 'descricao']
    prepopulated_fields = {'slug': ('nome',)}
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'categoria', 'marca', 'codigo', 'descricao', 'preco', 'estoque', 'imagem', 'active')
        }),
        ('Especificações Técnicas', {
            'fields': ('aro', 'largura', 'perfil', 'indice_carga', 'indice_velocidade')
        }),
        ('SEO', {
            'fields': ('slug', 'meta_description')
        }),
        ('Datas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

