from django.db import models
from datetime import datetime

class MarcaVeiculo(models.Model):
    """Modelo para marcas de veículos"""
    nome = models.CharField(max_length=50, unique=True, verbose_name='Nome da Marca')
    pais_origem = models.CharField(max_length=50, default='Brasil', verbose_name='País de Origem')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    data_cadastro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Marca de Veículo'
        verbose_name_plural = 'Marcas de Veículos'
        ordering = ['nome']
    
    def __str__(self):
        return self.nome

class TipoVeiculo(models.Model):
    """Modelo para tipos de veículos"""
    TIPOS_CHOICES = [
        ('caminhao', 'Caminhão'),
        ('carreta', 'Carreta'),
        ('semi_reboque', 'Semi-reboque'),
        ('reboque', 'Reboque'),
        ('bitrem', 'Bitrem'),
        ('rodotrem', 'Rodotrem'),
    ]
    
    nome = models.CharField(max_length=20, choices=TIPOS_CHOICES, unique=True, verbose_name='Tipo')
    descricao = models.CharField(max_length=100, verbose_name='Descrição')
    
    class Meta:
        verbose_name = 'Tipo de Veículo'
        verbose_name_plural = 'Tipos de Veículos'
        ordering = ['nome']
    
    def __str__(self):
        return self.get_nome_display()

class ModeloVeiculo(models.Model):
    """Modelo para modelos de veículos"""
    marca = models.ForeignKey(MarcaVeiculo, on_delete=models.CASCADE, related_name='modelos')
    tipo_veiculo = models.ForeignKey(TipoVeiculo, on_delete=models.CASCADE, related_name='modelos')
    nome = models.CharField(max_length=100, verbose_name='Nome do Modelo')
    ano_inicio = models.PositiveSmallIntegerField(verbose_name='Ano de Início')
    ano_fim = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Ano de Fim')
    quantidade_eixos = models.PositiveSmallIntegerField(verbose_name='Quantidade de Eixos')
    capacidade_carga = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, verbose_name='Capacidade de Carga (kg)')
    motor_padrao = models.CharField(max_length=100, blank=True, verbose_name='Motor Padrão')
    combustivel = models.CharField(max_length=20, default='Diesel', verbose_name='Combustível')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    data_cadastro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Modelo de Veículo'
        verbose_name_plural = 'Modelos de Veículos'
        ordering = ['marca__nome', 'nome']
        unique_together = ['marca', 'nome', 'ano_inicio']
    
    def __str__(self):
        return f"{self.marca.nome} {self.nome}"
    
    @property
    def anos_disponiveis(self):
        """Retorna lista de anos disponíveis para este modelo"""
        ano_atual = datetime.now().year
        ano_fim = self.ano_fim if self.ano_fim else ano_atual
        return list(range(self.ano_inicio, min(ano_fim + 1, ano_atual + 1)))
    
    @property
    def nome_completo(self):
        """Retorna nome completo do modelo com especificações"""
        specs = []
        if self.quantidade_eixos:
            specs.append(f"{self.quantidade_eixos} eixos")
        if self.capacidade_carga:
            specs.append(f"{self.capacidade_carga}kg")
        
        if specs:
            return f"{self.nome} ({', '.join(specs)})"
        return self.nome

class CorVeiculo(models.Model):
    """Modelo para cores de veículos"""
    nome = models.CharField(max_length=30, unique=True, verbose_name='Nome da Cor')
    codigo_hex = models.CharField(max_length=7, blank=True, verbose_name='Código Hex')
    popular = models.BooleanField(default=False, verbose_name='Cor Popular')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    
    class Meta:
        verbose_name = 'Cor de Veículo'
        verbose_name_plural = 'Cores de Veículos'
        ordering = ['-popular', 'nome']
    
    def __str__(self):
        return self.nome

class ConfiguracaoEixo(models.Model):
    """Modelo para configurações de eixos"""
    quantidade_eixos = models.PositiveSmallIntegerField(unique=True, verbose_name='Quantidade de Eixos')
    descricao = models.CharField(max_length=100, verbose_name='Descrição')
    configuracao = models.CharField(max_length=20, verbose_name='Configuração (ex: 4x2, 6x4)')
    peso_maximo = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, verbose_name='Peso Máximo (kg)')
    
    class Meta:
        verbose_name = 'Configuração de Eixo'
        verbose_name_plural = 'Configurações de Eixos'
        ordering = ['quantidade_eixos']
    
    def __str__(self):
        return f"{self.quantidade_eixos} eixos - {self.configuracao}"

class EspecificacaoTecnica(models.Model):
    """Modelo para especificações técnicas dos modelos"""
    modelo = models.OneToOneField(ModeloVeiculo, on_delete=models.CASCADE, related_name='especificacao')
    potencia_motor = models.CharField(max_length=20, blank=True, verbose_name='Potência do Motor')
    torque_motor = models.CharField(max_length=20, blank=True, verbose_name='Torque do Motor')
    transmissao = models.CharField(max_length=50, blank=True, verbose_name='Transmissão')
    freios = models.CharField(max_length=50, blank=True, verbose_name='Sistema de Freios')
    suspensao_dianteira = models.CharField(max_length=50, blank=True, verbose_name='Suspensão Dianteira')
    suspensao_traseira = models.CharField(max_length=50, blank=True, verbose_name='Suspensão Traseira')
    tanque_combustivel = models.CharField(max_length=20, blank=True, verbose_name='Capacidade do Tanque')
    pneus_dianteiros = models.CharField(max_length=20, blank=True, verbose_name='Medida Pneus Dianteiros')
    pneus_traseiros = models.CharField(max_length=20, blank=True, verbose_name='Medida Pneus Traseiros')
    
    class Meta:
        verbose_name = 'Especificação Técnica'
        verbose_name_plural = 'Especificações Técnicas'
    
    def __str__(self):
        return f"Especificações - {self.modelo}"

