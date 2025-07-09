from django.db import models
from xbpneus.core.models import BaseModel


class Contato(BaseModel):
    """Mensagens de contato"""
    ASSUNTO_CHOICES = [
        ('duvida', 'Dúvida'),
        ('orcamento', 'Orçamento'),
        ('suporte', 'Suporte'),
        ('reclamacao', 'Reclamação'),
        ('sugestao', 'Sugestão'),
        ('outro', 'Outro'),
    ]
    
    nome = models.CharField('Nome', max_length=200)
    email = models.EmailField('Email')
    telefone = models.CharField('Telefone', max_length=20, blank=True)
    assunto = models.CharField('Assunto', max_length=20, choices=ASSUNTO_CHOICES)
    mensagem = models.TextField('Mensagem')
    respondido = models.BooleanField('Respondido', default=False)
    resposta = models.TextField('Resposta', blank=True)
    data_resposta = models.DateTimeField('Data da Resposta', null=True, blank=True)

    class Meta:
        verbose_name = 'Contato'
        verbose_name_plural = 'Contatos'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.nome} - {self.get_assunto_display()} - {self.created_at.strftime("%d/%m/%Y")}'

