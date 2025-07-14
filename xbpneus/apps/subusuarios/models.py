from django.db import models
from django.contrib.auth.models import User

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

