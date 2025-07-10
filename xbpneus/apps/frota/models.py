from django.db import models
from django.contrib.auth.models import User

class Veiculo(models.Model):
    """Modelo para cadastro de veículos"""
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='veiculos')
    placa = models.CharField(max_length=8, unique=True, verbose_name='Placa')
    modelo = models.CharField(max_length=100, verbose_name='Modelo')
    cor = models.CharField(max_length=50, verbose_name='Cor')
    km = models.IntegerField(verbose_name='Quilometragem')
    ano = models.IntegerField(verbose_name='Ano')
    data_cadastro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Veículo'
        verbose_name_plural = 'Veículos'
        ordering = ['-data_cadastro']
    
    def __str__(self):
        return f"{self.placa} - {self.modelo}"

class Pneu(models.Model):
    """Modelo para cadastro de pneus"""
    
    # Medidas de pneus pré-definidas
    MEDIDAS_CHOICES = [
        ('225/75/16', '225/75/16'),
        ('215/75/17.5', '215/75/17.5'),
        ('235/75/17.5', '235/75/17.5'),
        ('275/80/22.5', '275/80/22.5'),
        ('295/80/22.5', '295/80/22.5'),
    ]
    
    # Posições no veículo
    POSICOES_CHOICES = [
        ('dianteiro_esquerdo', 'Dianteiro Esquerdo'),
        ('dianteiro_direito', 'Dianteiro Direito'),
        ('traseiro_esquerdo_1', 'Traseiro Esquerdo 1'),
        ('traseiro_direito_1', 'Traseiro Direito 1'),
        ('traseiro_esquerdo_2', 'Traseiro Esquerdo 2'),
        ('traseiro_direito_2', 'Traseiro Direito 2'),
        ('estepe', 'Estepe'),
    ]
    
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE, related_name='pneus')
    posicao = models.CharField(max_length=30, choices=POSICOES_CHOICES, verbose_name='Posição no Veículo')
    marca = models.CharField(max_length=50, verbose_name='Marca')
    modelo = models.CharField(max_length=100, verbose_name='Modelo')
    medida = models.CharField(max_length=20, choices=MEDIDAS_CHOICES, verbose_name='Medida do Pneu')
    pressao = models.DecimalField(max_digits=5, decimal_places=1, verbose_name='Pressão (PSI)')
    profundidade_sulco = models.DecimalField(max_digits=4, decimal_places=1, verbose_name='Profundidade do Sulco (mm)')
    custo = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Custo')
    data_instalacao = models.DateField(verbose_name='Data de Instalação')
    km_instalacao = models.IntegerField(verbose_name='KM na Instalação')
    fornecedor = models.CharField(max_length=100, verbose_name='Fornecedor')
    lote_fabricacao = models.CharField(max_length=50, verbose_name='Lote de Fabricação')
    numero_serie = models.CharField(max_length=50, verbose_name='Número de Série')
    marca_fogo = models.CharField(max_length=50, verbose_name='Marca Fogo')
    observacoes = models.TextField(blank=True, verbose_name='Observações Técnicas')
    data_cadastro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Pneu'
        verbose_name_plural = 'Pneus'
        ordering = ['-data_cadastro']
        unique_together = ['veiculo', 'posicao']
    
    def __str__(self):
        return f"{self.veiculo.placa} - {self.get_posicao_display()} - {self.marca} {self.modelo}"

class HistoricoPneu(models.Model):
    """Modelo para histórico de manutenções e trocas de pneus"""
    
    TIPOS_EVENTO = [
        ('instalacao', 'Instalação'),
        ('manutencao', 'Manutenção'),
        ('troca', 'Troca'),
        ('remocao', 'Remoção'),
    ]
    
    pneu = models.ForeignKey(Pneu, on_delete=models.CASCADE, related_name='historico')
    tipo_evento = models.CharField(max_length=20, choices=TIPOS_EVENTO, verbose_name='Tipo de Evento')
    data_evento = models.DateField(verbose_name='Data do Evento')
    km_evento = models.IntegerField(verbose_name='KM no Evento')
    descricao = models.TextField(verbose_name='Descrição')
    custo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Custo')
    data_cadastro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Histórico de Pneu'
        verbose_name_plural = 'Históricos de Pneus'
        ordering = ['-data_evento']
    
    def __str__(self):
        return f"{self.pneu} - {self.get_tipo_evento_display()} - {self.data_evento}"

