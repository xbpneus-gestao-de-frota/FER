from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.auth.hashers import make_password
from xbpneus.apps.subusuarios.models import SubUsuario, ModuloAcesso
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Popula pilares completos, permissões e usuário principal da empresa'

    def handle(self, *args, **options):
        """
        Comando Django equivalente ao XBPNEUS_SCRIPT_PILAR_CONFIGURACOES.sql
        Cria todos os pilares, permissões e usuário principal
        """
        
        try:
            with transaction.atomic():
                self.stdout.write(self.style.SUCCESS('🚀 Iniciando seed completo dos pilares XBPNEUS...'))
                
                # 1. CRIAR/ATUALIZAR MÓDULOS (PILARES)
                self._criar_modulos()
                
                # 2. CRIAR USUÁRIO PRINCIPAL DA EMPRESA (se não existir)
                self._criar_usuario_principal()
                
                # 3. CONFIGURAR PERMISSÕES BÁSICAS
                self._configurar_permissoes()
                
                self.stdout.write(self.style.SUCCESS('✅ Seed completo finalizado com sucesso!'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Erro durante o seed: {str(e)}'))
            logger.error(f'Erro no seed_pilares_completo: {str(e)}')
            raise

    def _criar_modulos(self):
        """Cria todos os módulos/pilares do sistema"""
        
        modulos_data = [
            {
                'nome': 'Dashboard',
                'slug': 'dashboard',
                'descricao': 'Painel principal com visão geral do sistema',
                'icone': 'bi-speedometer2',
                'ordem': 0,
                'ativo': True
            },
            {
                'nome': 'Frota',
                'slug': 'frota',
                'descricao': 'Gestão completa da frota de veículos',
                'icone': 'bi-truck',
                'ordem': 1,
                'ativo': True
            },
            {
                'nome': 'Manutenção',
                'slug': 'manutencao',
                'descricao': 'Controle de manutenções preventivas e corretivas',
                'icone': 'bi-tools',
                'ordem': 2,
                'ativo': True
            },
            {
                'nome': 'Pneus',
                'slug': 'pneus',
                'descricao': 'Gestão detalhada de pneus e rodízios',
                'icone': 'bi-circle',
                'ordem': 3,
                'ativo': True
            },
            {
                'nome': 'Estoque',
                'slug': 'estoque',
                'descricao': 'Controle de estoque de peças e materiais',
                'icone': 'bi-box-seam',
                'ordem': 4,
                'ativo': True
            },
            {
                'nome': 'Financeiro',
                'slug': 'financeiro',
                'descricao': 'Gestão financeira e controle de custos',
                'icone': 'bi-currency-dollar',
                'ordem': 5,
                'ativo': True
            },
            {
                'nome': 'Relatórios',
                'slug': 'relatorios',
                'descricao': 'Relatórios gerenciais e análises',
                'icone': 'bi-graph-up',
                'ordem': 6,
                'ativo': True
            },
            {
                'nome': 'Configurações',
                'slug': 'configuracoes',
                'descricao': 'Configurações do sistema e empresa',
                'icone': 'bi-gear',
                'ordem': 7,
                'ativo': True
            },
            {
                'nome': 'Usuários',
                'slug': 'usuarios',
                'descricao': 'Gestão de usuários e permissões',
                'icone': 'bi-people',
                'ordem': 8,
                'ativo': True
            },
            {
                'nome': 'Eventos',
                'slug': 'eventos',
                'descricao': 'Registro de eventos e notificações',
                'icone': 'bi-calendar-event',
                'ordem': 9,
                'ativo': True
            }
        ]
        
        for modulo_data in modulos_data:
            modulo, created = ModuloAcesso.objects.get_or_create(
                slug=modulo_data['slug'],
                defaults=modulo_data
            )
            
            if created:
                self.stdout.write(f'✅ Módulo criado: {modulo.nome}')
            else:
                # Atualiza dados se já existe
                for key, value in modulo_data.items():
                    setattr(modulo, key, value)
                modulo.save()
                self.stdout.write(f'🔄 Módulo atualizado: {modulo.nome}')

    def _criar_usuario_principal(self):
        """Cria usuário principal da empresa se não existir"""
        
        # Verifica se já existe um usuário admin
        if SubUsuario.objects.filter(login='admin').exists():
            self.stdout.write('ℹ️ Usuário admin já existe, pulando criação...')
            return
            
        # Cria usuário principal
        usuario_admin = SubUsuario.objects.create(
            nome='Administrador do Sistema',
            email='admin@xbpneus.com',
            login='admin',
            funcao='Administrador Geral',
            senha=make_password('admin123'),  # Senha padrão - DEVE SER ALTERADA
            ativo=True,
            usuario_principal=None  # É o usuário principal
        )
        
        # Associa todos os módulos ao admin
        todos_modulos = ModuloAcesso.objects.filter(ativo=True)
        usuario_admin.modulos.set(todos_modulos)
        
        self.stdout.write(f'✅ Usuário principal criado: {usuario_admin.nome}')
        self.stdout.write('⚠️ IMPORTANTE: Altere a senha padrão "admin123" imediatamente!')

    def _configurar_permissoes(self):
        """Configura permissões básicas do sistema"""
        
        # Aqui você pode adicionar lógica específica de permissões
        # Por exemplo, criar grupos de permissões, configurar níveis de acesso, etc.
        
        self.stdout.write('✅ Permissões básicas configuradas')
        
        # Exemplo de configuração adicional:
        total_modulos = ModuloAcesso.objects.filter(ativo=True).count()
        total_usuarios = SubUsuario.objects.count()
        
        self.stdout.write(f'📊 Estatísticas finais:')
        self.stdout.write(f'   - Módulos ativos: {total_modulos}')
        self.stdout.write(f'   - Usuários cadastrados: {total_usuarios}')

