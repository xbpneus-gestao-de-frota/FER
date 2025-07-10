from django.db import models
from xbpneus.core.models import BaseModel


class Categoria(BaseModel):
    """Categorias de produtos"""
    nome = models.CharField('Nome', max_length=100)
    descricao = models.TextField('Descrição', blank=True)
    slug = models.SlugField('Slug', unique=True)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Marca(BaseModel):
    """Marcas de pneus"""
    nome = models.CharField('Nome', max_length=100)
    logo = models.ImageField('Logo', upload_to='marcas/', blank=True)
    site = models.URLField('Site', blank=True)

    class Meta:
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Produto(BaseModel):
    """Produtos (Pneus)"""
    nome = models.CharField('Nome', max_length=200)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, verbose_name='Categoria')
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE, verbose_name='Marca')
    codigo = models.CharField('Código', max_length=50, unique=True)
    descricao = models.TextField('Descrição')
    preco = models.DecimalField('Preço', max_digits=10, decimal_places=2)
    estoque = models.PositiveIntegerField('Estoque', default=0)
    imagem = models.ImageField('Imagem', upload_to='produtos/', blank=True)
    
    # Especificações técnicas
    aro = models.CharField('Aro', max_length=10)
    largura = models.CharField('Largura', max_length=10)
    perfil = models.CharField('Perfil', max_length=10)
    indice_carga = models.CharField('Índice de Carga', max_length=10, blank=True)
    indice_velocidade = models.CharField('Índice de Velocidade', max_length=5, blank=True)
    
    # SEO
    slug = models.SlugField('Slug', unique=True)
    meta_description = models.CharField('Meta Description', max_length=160, blank=True)

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['nome']

    def __str__(self):
        return f'{self.marca.nome} {self.nome} - {self.largura}/{self.perfil}R{self.aro}'

    @property
    def especificacao_completa(self):
        return f'{self.largura}/{self.perfil}R{self.aro}'

