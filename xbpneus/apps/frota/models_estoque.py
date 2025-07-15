from django.db import models
from django.contrib.auth.models import User
from .models import Veiculo


class PneuEstoque(models.Model):
    """Modelo para estoque de pneus"""
    
    STATUS_CHOICES = [
        ('disponivel', 'Disponível'),
        ('em_uso', 'Em uso'),
        ('reformado', 'Reformado'),
        ('descartado', 'Descartado'),
    ]
    
    TIPO_CHOICES = [
        ('novo', 'Novo'),
        ('usado', 'Usado'),
        ('reformado', 'Reformado'),
    ]
    
    MEDIDAS_CHOICES = [
        ('225/75/16', '225/75/16'),
        ('215/75/17.5', '215/75/17.5'),
        ('235/75/17.5', '235/75/17.5'),
        ('275/80/22.5', '275/80/22.5'),
        ('295/80/22.5', '295/80/22.5'),
        ('315/80/22.5', '315/80/22.5'),
    ]
    
    # Informações da Nota Fiscal
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pneus_estoque')
    numero_nf = models.CharField(max_length=50, verbose_name='Número da NF')
    fornecedor = models.CharField(max_length=100, verbose_name='Fornecedor')
    data_entrada = models.DateField(verbose_name='Data de Entrada')
    
    # Informações do Pneu
    marca = models.CharField(max_length=50, verbose_name='Marca')
    modelo = models.CharField(max_length=100, verbose_name='Modelo')
    medida = models.CharField(max_length=20, choices=MEDIDAS_CHOICES, verbose_name='Medida')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, verbose_name='Tipo')
    
    # Controle
    numero_serie = models.CharField(max_length=50, unique=True, verbose_name='Número de Série')
    dot = models.CharField(max_length=10, verbose_name='DOT (Data Fabricação)')
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor Unitário')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='disponivel', verbose_name='Status')
    
    # Observações
    observacoes = models.TextField(blank=True, verbose_name='Observações')
    data_cadastro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Pneu em Estoque'
        verbose_name_plural = 'Pneus em Estoque'
        ordering = ['-data_cadastro']
    
    def __str__(self):
        return f"{self.marca} {self.modelo} - {self.medida} - {self.numero_serie}"


class VinculacaoPneu(models.Model):
    """Modelo para vinculação de pneu do estoque ao veículo"""
    
    POSICOES_CHOICES = [
        ('dianteiro_esquerdo', 'Dianteiro Esquerdo'),
        ('dianteiro_direito', 'Dianteiro Direito'),
        ('intermediario_esquerdo_1', 'Intermediário Esquerdo 1'),
        ('intermediario_esquerdo_2', 'Intermediário Esquerdo 2'),
        ('intermediario_direito_1', 'Intermediário Direito 1'),
        ('intermediario_direito_2', 'Intermediário Direito 2'),
        ('traseiro_esquerdo_1', 'Traseiro Esquerdo 1'),
        ('traseiro_esquerdo_2', 'Traseiro Esquerdo 2'),
        ('traseiro_direito_1', 'Traseiro Direito 1'),
        ('traseiro_direito_2', 'Traseiro Direito 2'),
        ('estepe', 'Estepe'),
    ]
    
    # Relacionamentos
    pneu_estoque = models.ForeignKey(PneuEstoque, on_delete=models.CASCADE, related_name='vinculacoes')
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE, related_name='pneus_vinculados')
    
    # Dados da montagem
    posicao = models.CharField(max_length=30, choices=POSICOES_CHOICES, verbose_name='Posição no Veículo')
    data_montagem = models.DateField(verbose_name='Data de Montagem')
    km_montagem = models.IntegerField(verbose_name='KM na Montagem')
    
    # Dados atuais
    pressao_atual = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True, verbose_name='Pressão Atual (PSI)')
    sulco_externo = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, verbose_name='Sulco Externo (mm)')
    sulco_central = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, verbose_name='Sulco Central (mm)')
    sulco_interno = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, verbose_name='Sulco Interno (mm)')
    
    # Controle
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    data_remocao = models.DateField(null=True, blank=True, verbose_name='Data de Remoção')
    km_remocao = models.IntegerField(null=True, blank=True, verbose_name='KM na Remoção')
    motivo_remocao = models.TextField(blank=True, verbose_name='Motivo da Remoção')
    
    observacoes = models.TextField(blank=True, verbose_name='Observações')
    data_cadastro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Vinculação de Pneu'
        verbose_name_plural = 'Vinculações de Pneus'
        ordering = ['-data_cadastro']
        unique_together = ['veiculo', 'posicao', 'ativo']  # Apenas um pneu ativo por posição
    
    def __str__(self):
        return f"{self.veiculo.placa} - {self.get_posicao_display()} - {self.pneu_estoque.marca}"
    
    def save(self, *args, **kwargs):
        # Atualizar status do pneu no estoque
        if self.ativo:
            self.pneu_estoque.status = 'em_uso'
        else:
            self.pneu_estoque.status = 'disponivel'
        self.pneu_estoque.save()
        super().save(*args, **kwargs)


class HistoricoMovimentacao(models.Model):
    """Histórico de movimentação dos pneus"""
    
    TIPOS_MOVIMENTO = [
        ('entrada', 'Entrada no Estoque'),
        ('montagem', 'Montagem no Veículo'),
        ('remocao', 'Remoção do Veículo'),
        ('manutencao', 'Manutenção'),
        ('reforma', 'Reforma'),
        ('descarte', 'Descarte'),
    ]
    
    pneu_estoque = models.ForeignKey(PneuEstoque, on_delete=models.CASCADE, related_name='historico')
    tipo_movimento = models.CharField(max_length=20, choices=TIPOS_MOVIMENTO, verbose_name='Tipo de Movimento')
    data_movimento = models.DateTimeField(auto_now_add=True, verbose_name='Data do Movimento')
    
    # Dados opcionais dependendo do tipo de movimento
    veiculo = models.ForeignKey(Veiculo, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Veículo')
    km_veiculo = models.IntegerField(null=True, blank=True, verbose_name='KM do Veículo')
    custo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Custo')
    
    descricao = models.TextField(verbose_name='Descrição')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário')
    
    class Meta:
        verbose_name = 'Histórico de Movimentação'
        verbose_name_plural = 'Históricos de Movimentação'
        ordering = ['-data_movimento']
    
    def __str__(self):
        return f"{self.pneu_estoque} - {self.get_tipo_movimento_display()} - {self.data_movimento.strftime('%d/%m/%Y')}"

