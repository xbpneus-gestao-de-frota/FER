from django.core.management.base import BaseCommand
from xbpneus.apps.subusuarios.models import ModuloAcesso, PerfilAcesso


class Command(BaseCommand):
    help = 'Popula os módulos de acesso (pilares) do sistema'

    def handle(self, *args, **options):
        # Definir os pilares do sistema
        pilares = [
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
                'descricao': 'Gestão completa da frota de veículos',
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
                'descricao': 'Controle financeiro e custos operacionais',
                'icone': 'bi-currency-dollar',
                'ordem': 6
            },
            {
                'nome': 'Compras',
                'slug': 'compras',
                'descricao': 'Gestão de compras e fornecedores',
                'icone': 'bi-cart',
                'ordem': 7
            },
            {
                'nome': 'Eventos',
                'slug': 'eventos',
                'descricao': 'Gestão de eventos e ocorrências',
                'icone': 'bi-calendar-event',
                'ordem': 8
            },
            {
                'nome': 'Notícias',
                'slug': 'noticias',
                'descricao': 'Central de notícias e comunicados',
                'icone': 'bi-newspaper',
                'ordem': 9
            },
            {
                'nome': 'Configurações',
                'slug': 'configuracoes',
                'descricao': 'Configurações do sistema e usuários',
                'icone': 'bi-gear',
                'ordem': 10
            }
        ]

        # Criar ou atualizar módulos
        for pilar_data in pilares:
            modulo, created = ModuloAcesso.objects.get_or_create(
                slug=pilar_data['slug'],
                defaults=pilar_data
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Módulo "{modulo.nome}" criado com sucesso')
                )
            else:
                # Atualizar dados se já existe
                for key, value in pilar_data.items():
                    setattr(modulo, key, value)
                modulo.save()
                self.stdout.write(
                    self.style.WARNING(f'↻ Módulo "{modulo.nome}" atualizado')
                )

        # Criar perfis de acesso padrão
        perfis = [
            {
                'nome': 'Administrador Completo',
                'descricao': 'Acesso total a todos os módulos do sistema',
                'modulos': ['dashboard', 'frota', 'estoque', 'manutencao', 'relatorios', 
                           'financeiro', 'compras', 'eventos', 'noticias', 'configuracoes']
            },
            {
                'nome': 'Gestor de Frota',
                'descricao': 'Acesso focado na gestão de frota e manutenção',
                'modulos': ['dashboard', 'frota', 'manutencao', 'relatorios']
            },
            {
                'nome': 'Financeiro',
                'descricao': 'Acesso aos módulos financeiros e relatórios',
                'modulos': ['dashboard', 'financeiro', 'compras', 'relatorios']
            },
            {
                'nome': 'Operacional',
                'descricao': 'Acesso básico para operações do dia a dia',
                'modulos': ['dashboard', 'frota', 'estoque', 'eventos']
            },
            {
                'nome': 'Compras',
                'descricao': 'Acesso focado em compras e estoque',
                'modulos': ['dashboard', 'estoque', 'compras', 'relatorios']
            },
            {
                'nome': 'Manutenção',
                'descricao': 'Acesso focado em manutenção e frota',
                'modulos': ['dashboard', 'frota', 'manutencao', 'estoque']
            }
        ]

        for perfil_data in perfis:
            perfil, created = PerfilAcesso.objects.get_or_create(
                nome=perfil_data['nome'],
                defaults={
                    'descricao': perfil_data['descricao']
                }
            )
            
            # Adicionar módulos ao perfil
            modulos_slugs = perfil_data['modulos']
            modulos = ModuloAcesso.objects.filter(slug__in=modulos_slugs)
            perfil.modulos.set(modulos)
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Perfil "{perfil.nome}" criado com sucesso')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'↻ Perfil "{perfil.nome}" atualizado')
                )

        self.stdout.write(
            self.style.SUCCESS('\n🎉 Setup dos pilares concluído com sucesso!')
        )
        self.stdout.write(
            self.style.SUCCESS(f'📊 Total de módulos: {ModuloAcesso.objects.count()}')
        )
        self.stdout.write(
            self.style.SUCCESS(f'👥 Total de perfis: {PerfilAcesso.objects.count()}')
        )

