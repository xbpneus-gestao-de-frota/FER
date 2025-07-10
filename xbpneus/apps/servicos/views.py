from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Servico


class ServicoListView(ListView):
    """Lista de serviços"""
    model = Servico
    template_name = 'servicos/lista.html'
    context_object_name = 'servicos'
    
    def get_queryset(self):
        return Servico.objects.filter(active=True).order_by('ordem', 'nome')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Serviços - XBPNEUS Premium',
            'meta_description': 'Conheça todos os serviços especializados da XBPNEUS Premium'
        })
        return context


class ServicoDetailView(DetailView):
    """Detalhes do serviço"""
    model = Servico
    template_name = 'servicos/detalhe.html'
    context_object_name = 'servico'
    slug_field = 'slug'
    
    def get_queryset(self):
        return Servico.objects.filter(active=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        servico = self.get_object()
        context.update({
            'page_title': f'{servico.nome} - XBPNEUS Premium',
            'meta_description': servico.meta_description or servico.descricao_curta,
            'outros_servicos': Servico.objects.filter(active=True).exclude(id=servico.id)[:3]
        })
        return context

