from django.db import models
from xbpneus.core.models import BaseModel


class Servico(BaseModel):
    """Serviços oferecidos pela XBPNEUS"""
    nome = models.CharField('Nome', max_length=200)
    descricao_curta = models.CharField('Descrição Curta', max_length=255)
    descricao = models.TextField('Descrição Completa')
    preco_base = models.DecimalField('Preço Base', max_digits=10, decimal_places=2, null=True, blank=True)
    icone = models.CharField('Ícone (FontAwesome)', max_length=50, default='fas fa-cog')
    imagem = models.ImageField('Imagem', upload_to='servicos/', blank=True)
    ordem = models.PositiveIntegerField('Ordem', default=0)
    
    # SEO
    slug = models.SlugField('Slug', unique=True)
    meta_description = models.CharField('Meta Description', max_length=160, blank=True)

    class Meta:
        verbose_name = 'Serviço'
        verbose_name_plural = 'Serviços'
        ordering = ['ordem', 'nome']

    def __str__(self):
        return self.nome


class Agendamento(BaseModel):
    """Agendamentos de serviços"""
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('confirmado', 'Confirmado'),
        ('em_andamento', 'Em Andamento'),
        ('concluido', 'Concluído'),
        ('cancelado', 'Cancelado'),
    ]
    
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE, verbose_name='Serviço')
    nome_cliente = models.CharField('Nome do Cliente', max_length=200)
    email_cliente = models.EmailField('Email do Cliente')
    telefone_cliente = models.CharField('Telefone do Cliente', max_length=20)
    data_agendamento = models.DateTimeField('Data do Agendamento')
    observacoes = models.TextField('Observações', blank=True)
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='pendente')

    class Meta:
        verbose_name = 'Agendamento'
        verbose_name_plural = 'Agendamentos'
        ordering = ['-data_agendamento']

    def __str__(self):
        return f'{self.servico.nome} - {self.nome_cliente} - {self.data_agendamento.strftime("%d/%m/%Y %H:%M")}'

