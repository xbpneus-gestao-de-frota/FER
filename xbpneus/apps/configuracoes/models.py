from django.db import models
from django.contrib.auth.models import User


class ConfiguracaoEmpresa(models.Model):
    """Configurações da empresa/transportador"""
    usuario = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='configuracao_empresa',
        verbose_name='Usuário'
    )
    
    # Dados da empresa
    razao_social = models.CharField(max_length=200, verbose_name='Razão Social')
    nome_fantasia = models.CharField(max_length=200, blank=True, verbose_name='Nome Fantasia')
    cnpj = models.CharField(max_length=18, verbose_name='CNPJ')
    inscricao_estadual = models.CharField(max_length=20, blank=True, verbose_name='Inscrição Estadual')
    
    # Contato
    telefone = models.CharField(max_length=20, verbose_name='Telefone')
    email_comercial = models.EmailField(verbose_name='E-mail Comercial')
    site = models.URLField(blank=True, verbose_name='Site')
    
    # Endereço
    cep = models.CharField(max_length=9, verbose_name='CEP')
    endereco = models.CharField(max_length=200, verbose_name='Endereço')
    numero = models.CharField(max_length=10, verbose_name='Número')
    complemento = models.CharField(max_length=100, blank=True, verbose_name='Complemento')
    bairro = models.CharField(max_length=100, verbose_name='Bairro')
    cidade = models.CharField(max_length=100, verbose_name='Cidade')
    estado = models.CharField(max_length=2, verbose_name='Estado')
    
    # Configurações do sistema
    fuso_horario = models.CharField(
        max_length=50, 
        default='America/Sao_Paulo',
        verbose_name='Fuso Horário'
    )
    moeda = models.CharField(
        max_length=3, 
        default='BRL',
        verbose_name='Moeda'
    )
    
    # Metadados
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name='Última Atualização')
    
    class Meta:
        verbose_name = 'Configuração da Empresa'
        verbose_name_plural = 'Configurações da Empresa'
    
    def __str__(self):
        return f"Configurações - {self.razao_social}"


class PreferenciaSistema(models.Model):
    """Preferências individuais do usuário"""
    usuario = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='preferencias',
        verbose_name='Usuário'
    )
    
    # Preferências de interface
    tema = models.CharField(
        max_length=20,
        choices=[
            ('claro', 'Claro'),
            ('escuro', 'Escuro'),
            ('automatico', 'Automático'),
        ],
        default='automatico',
        verbose_name='Tema'
    )
    
    idioma = models.CharField(
        max_length=10,
        choices=[
            ('pt-br', 'Português (Brasil)'),
            ('en', 'English'),
            ('es', 'Español'),
        ],
        default='pt-br',
        verbose_name='Idioma'
    )
    
    # Notificações
    notificacoes_email = models.BooleanField(default=True, verbose_name='Notificações por E-mail')
    notificacoes_sistema = models.BooleanField(default=True, verbose_name='Notificações do Sistema')
    
    # Dashboard
    itens_por_pagina = models.PositiveIntegerField(default=20, verbose_name='Itens por Página')
    dashboard_compacto = models.BooleanField(default=False, verbose_name='Dashboard Compacto')
    
    # Metadados
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name='Última Atualização')
    
    class Meta:
        verbose_name = 'Preferência do Sistema'
        verbose_name_plural = 'Preferências do Sistema'
    
    def __str__(self):
        return f"Preferências - {self.usuario.username}"

