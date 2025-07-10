from django.shortcuts import render
from django.views.generic import TemplateView


class HomeView(TemplateView):
    """Página inicial do XBPNEUS"""
    template_name = 'home/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'XBPNEUS Premium - Gestão de Pneus',
            'meta_description': 'Sistema premium de gestão de pneus com tecnologia avançada',
            'hero_title': 'XBPNEUS Premium',
            'hero_subtitle': 'Tecnologia Avançada em Gestão de Pneus',
            'features': [
                {
                    'title': 'Gestão Inteligente',
                    'description': 'Sistema completo para controle de estoque e vendas',
                    'icon': 'fas fa-cogs'
                },
                {
                    'title': 'Relatórios Avançados',
                    'description': 'Análises detalhadas para tomada de decisão',
                    'icon': 'fas fa-chart-line'
                },
                {
                    'title': 'Suporte 24/7',
                    'description': 'Atendimento especializado quando você precisar',
                    'icon': 'fas fa-headset'
                }
            ]
        })
        return context


def home_view(request):
    """View alternativa para a página inicial"""
    return render(request, 'home/index.html', {
        'page_title': 'XBPNEUS Premium',
    })

