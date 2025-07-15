from django.db import models
from django.contrib.auth.models import User


class ModuloAcesso(models.Model):
    """Módulos de acesso do sistema (pilares)"""
    nome = models.CharField(max_length=50, unique=True, verbose_name='Nome do Módulo')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='Slug')
    descricao = models.TextField(blank=True, verbose_name='Descrição')
    icone = models.CharField(max_length=50, default='bi-circle', verbose_name='Ícone Bootstrap')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    ordem = models.PositiveIntegerField(default=0, verbose_name='Ordem de Exibição')
    
    class Meta:
        verbose_name = 'Módulo de Acesso'
        verbose_name_plural = 'Módulos de Acesso'
        ordering = ['ordem', 'nome']
    
    def __str__(self):
        return self.nome


class SubUsuario(models.Model):
    FUNCAO_CHOICES = [
        ('diretoria', 'Diretoria'),
        ('financeiro', 'Financeiro'),
        ('gestor_frota', 'Gestor de Frota'),
        ('operacional', 'Operacional'),
        ('compras', 'Compras'),
        ('manutencao', 'Manutenção'),
        ('administrativo', 'Administrativo'),
    ]
    
    nome = models.CharField(max_length=100, verbose_name='Nome Completo')
    email = models.EmailField(verbose_name='E-mail')
    funcao = models.CharField(
        max_length=20, 
        choices=FUNCAO_CHOICES, 
        verbose_name='Função'
    )
    usuario_principal = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='subusuarios',
        verbose_name='Usuário Principal'
    )
    modulos = models.ManyToManyField(
        ModuloAcesso, 
        blank=True, 
        related_name='subusuarios',
        verbose_name='Módulos de Acesso'
    )
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name='Última Atualização')
    
    class Meta:
        verbose_name = 'Subusuário'
        verbose_name_plural = 'Subusuários'
        ordering = ['nome']
        unique_together = ['email', 'usuario_principal']  # Email único por usuário principal
    
    def __str__(self):
        return f"{self.nome} ({self.get_funcao_display()})"
    
    def get_funcao_display_badge(self):
        """Retorna a função com classe CSS para badge"""
        badge_classes = {
            'diretoria': 'bg-primary',
            'financeiro': 'bg-success',
            'gestor_frota': 'bg-warning',
            'operacional': 'bg-info',
            'compras': 'bg-secondary',
            'manutencao': 'bg-danger',
            'administrativo': 'bg-dark',
        }
        return {
            'texto': self.get_funcao_display(),
            'classe': badge_classes.get(self.funcao, 'bg-secondary')
        }
    
    def tem_acesso_modulo(self, slug_modulo):
        """Verifica se o subusuário tem acesso a um módulo específico"""
        return self.modulos.filter(slug=slug_modulo, ativo=True).exists()
    
    def get_modulos_ativos(self):
        """Retorna módulos ativos do subusuário"""
        return self.modulos.filter(ativo=True).order_by('ordem', 'nome')


class PerfilAcesso(models.Model):
    """Perfis pré-definidos de acesso para facilitar a configuração"""
    nome = models.CharField(max_length=50, unique=True, verbose_name='Nome do Perfil')
    descricao = models.TextField(verbose_name='Descrição')
    modulos = models.ManyToManyField(ModuloAcesso, verbose_name='Módulos Incluídos')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    
    class Meta:
        verbose_name = 'Perfil de Acesso'
        verbose_name_plural = 'Perfis de Acesso'
        ordering = ['nome']
    
    def __str__(self):
        return self.nome
