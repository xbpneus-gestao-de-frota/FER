from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction
from xbpneus.apps.subusuarios.models import ModuloAcesso, SubUsuario


class Command(BaseCommand):
    help = 'Aplica as configurações dos pilares baseado no script SQL recebido'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('Iniciando aplicação das configurações dos pilares...')
        )

        try:
            with transaction.atomic():
                # 1. Popular pilares básicos (equivalente aos pilares do SQL)
                pilares_basicos = [
                    {
                        'nome': 'Frota',
                        'slug': 'frota',
                        'descricao': 'Gestão completa da frota de veículos',
                        'icone': 'bi-truck',
                        'ordem': 1
                    },
                    {
                        'nome': 'Manutenção',
                        'slug': 'manutencao',
                        'descricao': 'Controle de manutenções preventivas e corretivas',
                        'icone': 'bi-tools',
                        'ordem': 2
                    },
                    {
                        'nome': 'Pneus',
                        'slug': 'pneus',
                        'descricao': 'Gestão e controle de pneus da frota',
                        'icone': 'bi-circle',
                        'ordem': 3
                    },
                    {
                        'nome': 'Estoque',
                        'slug': 'estoque',
                        'descricao': 'Controle de estoque de peças e materiais',
                        'icone': 'bi-box-seam',
                        'ordem': 4
                    },
                    {
                        'nome': 'Financeiro',
                        'slug': 'financeiro',
                        'descricao': 'Gestão financeira e controle de custos',
                        'icone': 'bi-currency-dollar',
                        'ordem': 5
                    },
                    {
                        'nome': 'Relatórios',
                        'slug': 'relatorios',
                        'descricao': 'Relatórios gerenciais e operacionais',
                        'icone': 'bi-graph-up',
                        'ordem': 6
                    },
                    {
                        'nome': 'Configurações',
                        'slug': 'configuracoes',
                        'descricao': 'Configurações do sistema e empresa',
                        'icone': 'bi-gear',
                        'ordem': 7
                    },
                    {
                        'nome': 'Dashboard',
                        'slug': 'dashboard',
                        'descricao': 'Painel principal com visão geral',
                        'icone': 'bi-speedometer2',
                        'ordem': 0
                    }
                ]

                # Criar ou atualizar módulos
                for pilar_data in pilares_basicos:
                    modulo, created = ModuloAcesso.objects.get_or_create(
                        nome=pilar_data['nome'],
                        defaults={
                            'slug': pilar_data['slug'],
                            'descricao': pilar_data['descricao'],
                            'icone': pilar_data['icone'],
                            'ordem': pilar_data['ordem'],
                            'ativo': True
                        }
                    )
                    
                    if created:
                        self.stdout.write(
                            self.style.SUCCESS(f'✓ Módulo "{modulo.nome}" criado com sucesso')
                        )
                    else:
                        # Atualizar dados se já existe
                        modulo.slug = pilar_data['slug']
                        modulo.descricao = pilar_data['descricao']
                        modulo.icone = pilar_data['icone']
                        modulo.ordem = pilar_data['ordem']
                        modulo.ativo = True
                        modulo.save()
                        self.stdout.write(
                            self.style.WARNING(f'⚠ Módulo "{modulo.nome}" já existia - dados atualizados')
                        )

                # 2. Verificar se existe usuário administrador principal
                admin_users = User.objects.filter(is_superuser=True)
                if not admin_users.exists():
                    self.stdout.write(
                        self.style.WARNING('⚠ Nenhum usuário administrador encontrado')
                    )
                    self.stdout.write(
                        'Para criar um usuário administrador, execute:'
                    )
                    self.stdout.write(
                        'python manage.py createsuperuser'
                    )
                else:
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ {admin_users.count()} usuário(s) administrador(es) encontrado(s)')
                    )

                # 3. Estatísticas finais
                total_modulos = ModuloAcesso.objects.filter(ativo=True).count()
                total_subusuarios = SubUsuario.objects.filter(ativo=True).count()
                
                self.stdout.write('\n' + '='*50)
                self.stdout.write(
                    self.style.SUCCESS('CONFIGURAÇÕES APLICADAS COM SUCESSO!')
                )
                self.stdout.write('='*50)
                self.stdout.write(f'📊 Total de módulos ativos: {total_modulos}')
                self.stdout.write(f'👥 Total de subusuários ativos: {total_subusuarios}')
                self.stdout.write(f'🔧 Total de usuários admin: {admin_users.count()}')
                
                # 4. Listar módulos criados
                self.stdout.write('\n📋 MÓDULOS DISPONÍVEIS:')
                for modulo in ModuloAcesso.objects.filter(ativo=True).order_by('ordem'):
                    self.stdout.write(f'  {modulo.ordem}. {modulo.nome} ({modulo.slug})')
                
                self.stdout.write('\n✅ Configurações dos pilares aplicadas com sucesso!')
                self.stdout.write('🚀 Sistema pronto para uso!')

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Erro ao aplicar configurações: {str(e)}')
            )
            raise e

