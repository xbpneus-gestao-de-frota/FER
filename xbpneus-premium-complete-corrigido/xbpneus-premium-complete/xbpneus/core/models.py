from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    """Modelo base para todos os modelos do XBPNEUS"""
    created_at = models.DateTimeField('Criado em', default=timezone.now)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    active = models.BooleanField('Ativo', default=True)

    class Meta:
        abstract = True


class Configuracao(BaseModel):
    """Configurações gerais do sistema"""
    chave = models.CharField('Chave', max_length=100, unique=True)
    valor = models.TextField('Valor')
    descricao = models.CharField('Descrição', max_length=255, blank=True)

    class Meta:
        verbose_name = 'Configuração'
        verbose_name_plural = 'Configurações'
        ordering = ['chave']

    def __str__(self):
        return f'{self.chave}: {self.valor[:50]}'

