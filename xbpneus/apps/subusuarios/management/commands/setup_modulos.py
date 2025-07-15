from django.core.management.base import BaseCommand
from xbpneus.apps.subusuarios.models import ModuloAcesso, PerfilAcesso


class Command(BaseCommand):
    help = 'Popula os módulos de acesso iniciais do sistema'

    def handle(self, *args, **options):
        self.stdout.write('Criando módulos de acesso...')
        
        # Módulos principais (9 pilares)
        modulos_data = [
            {
                'nome': 'Dashboard',
                'slug': 'dashboard',
                'descricao': 'Painel principal com visão geral do sistema',
                'icone': 'bi-speedometer2',
                'ordem': 1
            },
            {
                'nome': 'Frota',
                'slug': 'frota',
                'descricao': 'Gestão de veículos e controle da frota',
                'icone': 'bi-truck',
                'ordem': 2
            },
            {
                'nome': 'Estoque',
                'slug': 'estoque',
                'descricao': 'Controle de estoque de pneus e peças',
                'icone': 'bi-boxes',
                'ordem': 3
            },
            {
                'nome': 'Manutenção',
                'slug': 'manutencao',
                'descricao': 'Gestão de manutenções preventivas e corretivas',
                'icone': 'bi-tools',
                'ordem': 4
            },
            {
                'nome': 'Relatórios',
                'slug': 'relatorios',
                'descricao': 'Relatórios gerenciais e operacionais',
                'icone': 'bi-graph-up',
                'ordem': 5
            },
            {
                'nome': 'Financeiro',
                'slug': 'financeiro',
                'descricao': 'Controle financeiro e custos',
                'icone': 'bi-currency-dollar',
                'ordem': 6
            },
            {
                'nome': 'Compras',
                'slug': 'compras',
                'descricao': 'Gestão de compras e fornecedores',
                'icone': 'bi-cart3',
                'ordem': 7
            },
            {
                'nome': 'Eventos',
                'slug': 'eventos',
                'descricao': 'Registro e acompanhamento de eventos',
                'icone': 'bi-calendar-event',
                'ordem': 8
            },
            {
                'nome': 'Notícias',
                'slug': 'noticias',
                'descricao': 'Comunicados e notícias internas',
                'icone': 'bi-newspaper',
                'ordem': 9
            },
        ]
        
        modulos_criados = 0
        for modulo_data in modulos_data:
            modulo, created = ModuloAcesso.objects.get_or_create(
                slug=modulo_data['slug'],
                defaults=modulo_data
            )
            if created:
                modulos_criados += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Módulo "{modulo.nome}" criado')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'- Módulo "{modulo.nome}" já existe')
                )
        
        self.stdout.write('\nCriando perfis de acesso padrão...')
        
        # Perfis de acesso padrão
        perfis_data = [
            {
                'nome': 'Administrador Completo',
                'descricao': 'Acesso total a todos os módulos do sistema',
                'modulos': ['dashboard', 'frota', 'estoque', 'manutencao', 'relatorios', 'financeiro', 'compras', 'eventos', 'noticias']
            },
            {
                'nome': 'Gestor de Frota',
                'descricao': 'Acesso aos módulos de gestão de frota e manutenção',
                'modulos': ['dashboard', 'frota', 'estoque', 'manutencao', 'relatorios']
            },
            {
                'nome': 'Financeiro',
                'descricao': 'Acesso aos módulos financeiros e de compras',
                'modulos': ['dashboard', 'financeiro', 'compras', 'relatorios']
            },
            {
                'nome': 'Operacional',
                'descricao': 'Acesso básico para operações do dia a dia',
                'modulos': ['dashboard', 'frota', 'eventos']
            },
            {
                'nome': 'Manutenção',
                'descricao': 'Acesso específico para equipe de manutenção',
                'modulos': ['dashboard', 'frota', 'estoque', 'manutencao']
            },
        ]
        
        perfis_criados = 0
        for perfil_data in perfis_data:
            perfil, created = PerfilAcesso.objects.get_or_create(
                nome=perfil_data['nome'],
                defaults={
                    'descricao': perfil_data['descricao']
                }
            )
            
            if created:
                # Adicionar módulos ao perfil
                modulos = ModuloAcesso.objects.filter(slug__in=perfil_data['modulos'])
                perfil.modulos.set(modulos)
                perfis_criados += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Perfil "{perfil.nome}" criado com {modulos.count()} módulos')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'- Perfil "{perfil.nome}" já existe')
                )
        
        # Resumo
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS(f'✓ {modulos_criados} módulos criados'))
        self.stdout.write(self.style.SUCCESS(f'✓ {perfis_criados} perfis criados'))
        self.stdout.write(self.style.SUCCESS('✓ Setup de módulos concluído com sucesso!'))
        self.stdout.write('='*50)

