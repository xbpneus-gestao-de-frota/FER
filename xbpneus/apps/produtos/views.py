from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Produto, Categoria, Marca


class ProdutoListView(ListView):
    """Lista de produtos"""
    model = Produto
    template_name = 'produtos/lista.html'
    context_object_name = 'produtos'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Produto.objects.filter(active=True).select_related('marca', 'categoria')
        
        # Filtros
        categoria = self.request.GET.get('categoria')
        marca = self.request.GET.get('marca')
        busca = self.request.GET.get('q')
        
        if categoria:
            queryset = queryset.filter(categoria__slug=categoria)
        if marca:
            queryset = queryset.filter(marca__id=marca)
        if busca:
            queryset = queryset.filter(nome__icontains=busca)
            
        return queryset.order_by('nome')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'categorias': Categoria.objects.filter(active=True),
            'marcas': Marca.objects.filter(active=True),
            'page_title': 'Produtos - XBPNEUS Premium'
        })
        return context


class ProdutoDetailView(DetailView):
    """Detalhes do produto"""
    model = Produto
    template_name = 'produtos/detalhe.html'
    context_object_name = 'produto'
    slug_field = 'slug'
    
    def get_queryset(self):
        return Produto.objects.filter(active=True).select_related('marca', 'categoria')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        produto = self.get_object()
        context.update({
            'page_title': f'{produto.nome} - XBPNEUS Premium',
            'meta_description': produto.meta_description or produto.descricao[:160],
            'produtos_relacionados': Produto.objects.filter(
                categoria=produto.categoria,
                active=True
            ).exclude(id=produto.id)[:4]
        })
        return context


def produtos_por_categoria(request, categoria_slug):
    """Produtos filtrados por categoria"""
    categoria = get_object_or_404(Categoria, slug=categoria_slug, active=True)
    produtos = Produto.objects.filter(categoria=categoria, active=True)
    
    return render(request, 'produtos/categoria.html', {
        'categoria': categoria,
        'produtos': produtos,
        'page_title': f'{categoria.nome} - XBPNEUS Premium'
    })

