from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def central_estoque(request):
    """Tela central do Pilar Estoque"""
    context = {
        'titulo_pilar': 'Estoque',
        'mascote': 'mascotes/estoque.jpg',
        'descricao': 'Controle completo do estoque de pneus e peças',
        'cor_pilar': 'success',
        'icone_pilar': 'bi bi-boxes',
        'cards_acoes': [
            {
                'titulo': 'Entrada de Pneus',
                'descricao': 'Registre a entrada de novos pneus no estoque.',
                'cor': 'success',
                'icone': 'bi bi-plus-circle-fill',
                'icone_info': 'bi bi-arrow-down-circle',
                'info_adicional': 'Controle de entrada',
                'icone_botao': 'bi bi-plus-lg',
                'texto_botao': 'Registrar Entrada',
                'url': '#',
                'disponivel': False
            },
            {
                'titulo': 'Saída de Pneus',
                'descricao': 'Registre a saída de pneus do estoque.',
                'cor': 'warning',
                'icone': 'bi bi-dash-circle-fill',
                'icone_info': 'bi bi-arrow-up-circle',
                'info_adicional': 'Controle de saída',
                'icone_botao': 'bi bi-dash-lg',
                'texto_botao': 'Registrar Saída',
                'url': '#',
                'disponivel': False
            },
            {
                'titulo': 'Consultar Estoque',
                'descricao': 'Visualize o estoque atual de pneus e peças.',
                'cor': 'info',
                'icone': 'bi bi-search',
                'icone_info': 'bi bi-eye',
                'info_adicional': 'Visualização completa',
                'icone_botao': 'bi bi-list-ul',
                'texto_botao': 'Ver Estoque',
                'url': '#',
                'disponivel': False
            }
        ],
        'estatisticas': [
            {'valor': '0', 'label': 'Pneus em Estoque', 'cor': 'success'},
            {'valor': '0', 'label': 'Entradas Hoje', 'cor': 'info'},
            {'valor': '0', 'label': 'Saídas Hoje', 'cor': 'warning'},
            {'valor': '100%', 'label': 'Controle', 'cor': 'primary'}
        ]
    }
    return render(request, 'pilares/central_base.html', context)

@login_required
def central_manutencao(request):
    """Tela central do Pilar Manutenção"""
    context = {
        'titulo_pilar': 'Manutenção',
        'mascote': 'mascotes/manutencao.webp',
        'descricao': 'Gerencie a manutenção preventiva e corretiva da frota',
        'cor_pilar': 'warning',
        'icone_pilar': 'bi bi-tools',
        'cards_acoes': [
            {
                'titulo': 'Agendar Manutenção',
                'descricao': 'Programe manutenções preventivas para seus veículos.',
                'cor': 'warning',
                'icone': 'bi bi-calendar-plus',
                'icone_info': 'bi bi-clock',
                'info_adicional': 'Preventiva',
                'icone_botao': 'bi bi-calendar-check',
                'texto_botao': 'Agendar',
                'url': '#',
                'disponivel': False
            },
            {
                'titulo': 'Registrar Manutenção',
                'descricao': 'Registre manutenções realizadas nos veículos.',
                'cor': 'success',
                'icone': 'bi bi-wrench',
                'icone_info': 'bi bi-check-circle',
                'info_adicional': 'Corretiva',
                'icone_botao': 'bi bi-plus-lg',
                'texto_botao': 'Registrar',
                'url': '#',
                'disponivel': False
            },
            {
                'titulo': 'Histórico',
                'descricao': 'Consulte o histórico de manutenções realizadas.',
                'cor': 'info',
                'icone': 'bi bi-clock-history',
                'icone_info': 'bi bi-list-ul',
                'info_adicional': 'Completo',
                'icone_botao': 'bi bi-search',
                'texto_botao': 'Ver Histórico',
                'url': '#',
                'disponivel': False
            }
        ],
        'estatisticas': [
            {'valor': '0', 'label': 'Manutenções Agendadas', 'cor': 'warning'},
            {'valor': '0', 'label': 'Realizadas Este Mês', 'cor': 'success'},
            {'valor': '0', 'label': 'Pendentes', 'cor': 'danger'},
            {'valor': '24/7', 'label': 'Suporte', 'cor': 'info'}
        ]
    }
    return render(request, 'pilares/central_base.html', context)

@login_required
def central_eventos(request):
    """Tela central do Pilar Eventos"""
    context = {
        'titulo_pilar': 'Eventos',
        'mascote': 'mascotes/eventos.webp',
        'descricao': 'Acompanhe eventos, ocorrências e alertas da frota',
        'cor_pilar': 'info',
        'icone_pilar': 'bi bi-calendar-event',
        'cards_acoes': [
            {
                'titulo': 'Registrar Evento',
                'descricao': 'Registre eventos e ocorrências da frota.',
                'cor': 'info',
                'icone': 'bi bi-plus-circle',
                'icone_info': 'bi bi-pencil',
                'info_adicional': 'Novo registro',
                'icone_botao': 'bi bi-plus-lg',
                'texto_botao': 'Registrar',
                'url': '#',
                'disponivel': False
            },
            {
                'titulo': 'Alertas',
                'descricao': 'Configure e gerencie alertas automáticos.',
                'cor': 'warning',
                'icone': 'bi bi-bell',
                'icone_info': 'bi bi-exclamation-triangle',
                'info_adicional': 'Automático',
                'icone_botao': 'bi bi-gear',
                'texto_botao': 'Configurar',
                'url': '#',
                'disponivel': False
            },
            {
                'titulo': 'Relatórios',
                'descricao': 'Visualize relatórios de eventos e ocorrências.',
                'cor': 'success',
                'icone': 'bi bi-graph-up',
                'icone_info': 'bi bi-file-text',
                'info_adicional': 'Detalhado',
                'icone_botao': 'bi bi-file-earmark-text',
                'texto_botao': 'Ver Relatórios',
                'url': '#',
                'disponivel': False
            }
        ],
        'estatisticas': [
            {'valor': '0', 'label': 'Eventos Hoje', 'cor': 'info'},
            {'valor': '0', 'label': 'Alertas Ativos', 'cor': 'warning'},
            {'valor': '0', 'label': 'Resolvidos', 'cor': 'success'},
            {'valor': '100%', 'label': 'Monitoramento', 'cor': 'primary'}
        ]
    }
    return render(request, 'pilares/central_base.html', context)

@login_required
def central_noticias(request):
    """Tela central do Pilar Notícias"""
    context = {
        'titulo_pilar': 'Notícias',
        'mascote': 'mascotes/noticias.jpg',
        'descricao': 'Fique por dentro das últimas notícias do setor',
        'cor_pilar': 'primary',
        'icone_pilar': 'bi bi-newspaper',
        'cards_acoes': [
            {
                'titulo': 'Últimas Notícias',
                'descricao': 'Veja as notícias mais recentes do setor.',
                'cor': 'primary',
                'icone': 'bi bi-newspaper',
                'icone_info': 'bi bi-clock',
                'info_adicional': 'Atualizadas',
                'icone_botao': 'bi bi-eye',
                'texto_botao': 'Ver Notícias',
                'url': '#',
                'disponivel': False
            },
            {
                'titulo': 'Favoritas',
                'descricao': 'Acesse suas notícias marcadas como favoritas.',
                'cor': 'warning',
                'icone': 'bi bi-star-fill',
                'icone_info': 'bi bi-heart',
                'info_adicional': 'Personalizadas',
                'icone_botao': 'bi bi-star',
                'texto_botao': 'Ver Favoritas',
                'url': '#',
                'disponivel': False
            },
            {
                'titulo': 'Categorias',
                'descricao': 'Explore notícias por categoria de interesse.',
                'cor': 'success',
                'icone': 'bi bi-tags',
                'icone_info': 'bi bi-filter',
                'info_adicional': 'Organizadas',
                'icone_botao': 'bi bi-list-ul',
                'texto_botao': 'Ver Categorias',
                'url': '#',
                'disponivel': False
            }
        ],
        'estatisticas': [
            {'valor': '0', 'label': 'Notícias Hoje', 'cor': 'primary'},
            {'valor': '0', 'label': 'Favoritas', 'cor': 'warning'},
            {'valor': '5', 'label': 'Categorias', 'cor': 'success'},
            {'valor': '24h', 'label': 'Atualização', 'cor': 'info'}
        ]
    }
    return render(request, 'pilares/central_base.html', context)

@login_required
def central_relatorios(request):
    """Tela central do Pilar Relatórios"""
    context = {
        'titulo_pilar': 'Relatórios',
        'mascote': 'mascotes/relatorios.webp',
        'descricao': 'Gere relatórios detalhados e análises da frota',
        'cor_pilar': 'success',
        'icone_pilar': 'bi bi-file-earmark-text',
        'cards_acoes': [
            {
                'titulo': 'Relatório de Frota',
                'descricao': 'Gere relatórios completos da sua frota.',
                'cor': 'success',
                'icone': 'bi bi-truck',
                'icone_info': 'bi bi-file-text',
                'info_adicional': 'Completo',
                'icone_botao': 'bi bi-download',
                'texto_botao': 'Gerar',
                'url': '#',
                'disponivel': False
            },
            {
                'titulo': 'Relatório de Custos',
                'descricao': 'Analise os custos operacionais da frota.',
                'cor': 'warning',
                'icone': 'bi bi-currency-dollar',
                'icone_info': 'bi bi-graph-up',
                'info_adicional': 'Financeiro',
                'icone_botao': 'bi bi-calculator',
                'texto_botao': 'Calcular',
                'url': '#',
                'disponivel': False
            },
            {
                'titulo': 'Dashboard Executivo',
                'descricao': 'Visualize indicadores executivos em tempo real.',
                'cor': 'info',
                'icone': 'bi bi-speedometer2',
                'icone_info': 'bi bi-lightning',
                'info_adicional': 'Tempo real',
                'icone_botao': 'bi bi-eye',
                'texto_botao': 'Visualizar',
                'url': '#',
                'disponivel': False
            }
        ],
        'estatisticas': [
            {'valor': '0', 'label': 'Relatórios Gerados', 'cor': 'success'},
            {'valor': '5', 'label': 'Tipos Disponíveis', 'cor': 'info'},
            {'valor': '0', 'label': 'Agendados', 'cor': 'warning'},
            {'valor': 'PDF', 'label': 'Formato', 'cor': 'primary'}
        ]
    }
    return render(request, 'pilares/central_base.html', context)

@login_required
def central_compras(request):
    """Tela central do Pilar Compras"""
    context = {
        'titulo_pilar': 'Compras',
        'mascote': 'mascotes/compras.webp',
        'descricao': 'Gerencie compras, fornecedores e orçamentos',
        'cor_pilar': 'info',
        'icone_pilar': 'bi bi-cart',
        'cards_acoes': [
            {
                'titulo': 'Nova Compra',
                'descricao': 'Registre uma nova compra de pneus ou peças.',
                'cor': 'info',
                'icone': 'bi bi-cart-plus',
                'icone_info': 'bi bi-plus-circle',
                'info_adicional': 'Novo pedido',
                'icone_botao': 'bi bi-plus-lg',
                'texto_botao': 'Registrar',
                'url': '#',
                'disponivel': False
            },
            {
                'titulo': 'Fornecedores',
                'descricao': 'Gerencie seus fornecedores e contatos.',
                'cor': 'success',
                'icone': 'bi bi-people',
                'icone_info': 'bi bi-building',
                'info_adicional': 'Cadastro',
                'icone_botao': 'bi bi-list-ul',
                'texto_botao': 'Ver Fornecedores',
                'url': '#',
                'disponivel': False
            },
            {
                'titulo': 'Orçamentos',
                'descricao': 'Compare orçamentos e tome decisões.',
                'cor': 'warning',
                'icone': 'bi bi-calculator',
                'icone_info': 'bi bi-graph-up',
                'info_adicional': 'Comparativo',
                'icone_botao': 'bi bi-search',
                'texto_botao': 'Comparar',
                'url': '#',
                'disponivel': False
            }
        ],
        'estatisticas': [
            {'valor': '0', 'label': 'Compras Este Mês', 'cor': 'info'},
            {'valor': '0', 'label': 'Fornecedores', 'cor': 'success'},
            {'valor': 'R$ 0', 'label': 'Valor Total', 'cor': 'warning'},
            {'valor': '0', 'label': 'Pendentes', 'cor': 'danger'}
        ]
    }
    return render(request, 'pilares/central_base.html', context)

@login_required
def central_financeiro(request):
    """Tela central do Pilar Financeiro"""
    context = {
        'titulo_pilar': 'Financeiro',
        'mascote': 'mascotes/financeiro.webp',
        'descricao': 'Controle financeiro completo da operação',
        'cor_pilar': 'success',
        'icone_pilar': 'bi bi-currency-dollar',
        'cards_acoes': [
            {
                'titulo': 'Contas a Pagar',
                'descricao': 'Gerencie contas a pagar e vencimentos.',
                'cor': 'danger',
                'icone': 'bi bi-credit-card',
                'icone_info': 'bi bi-calendar-x',
                'info_adicional': 'Vencimentos',
                'icone_botao': 'bi bi-list-ul',
                'texto_botao': 'Ver Contas',
                'url': '#',
                'disponivel': False
            },
            {
                'titulo': 'Contas a Receber',
                'descricao': 'Acompanhe recebimentos e faturamento.',
                'cor': 'success',
                'icone': 'bi bi-cash-coin',
                'icone_info': 'bi bi-arrow-down-circle',
                'info_adicional': 'Recebimentos',
                'icone_botao': 'bi bi-graph-up',
                'texto_botao': 'Ver Recebimentos',
                'url': '#',
                'disponivel': False
            },
            {
                'titulo': 'Fluxo de Caixa',
                'descricao': 'Visualize o fluxo de caixa em tempo real.',
                'cor': 'info',
                'icone': 'bi bi-graph-up-arrow',
                'icone_info': 'bi bi-lightning',
                'info_adicional': 'Tempo real',
                'icone_botao': 'bi bi-speedometer2',
                'texto_botao': 'Ver Fluxo',
                'url': '#',
                'disponivel': False
            }
        ],
        'estatisticas': [
            {'valor': 'R$ 0', 'label': 'Saldo Atual', 'cor': 'success'},
            {'valor': 'R$ 0', 'label': 'A Receber', 'cor': 'info'},
            {'valor': 'R$ 0', 'label': 'A Pagar', 'cor': 'warning'},
            {'valor': '0', 'label': 'Vencimentos Hoje', 'cor': 'danger'}
        ]
    }
    return render(request, 'pilares/central_base.html', context)

