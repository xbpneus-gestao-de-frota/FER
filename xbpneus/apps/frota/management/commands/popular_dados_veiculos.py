from django.core.management.base import BaseCommand
from django.db import transaction
from xbpneus.apps.frota.models_auxiliares import (
    MarcaVeiculo, TipoVeiculo, ModeloVeiculo, CorVeiculo, 
    ConfiguracaoEixo, EspecificacaoTecnica
)

class Command(BaseCommand):
    help = 'Popula o banco de dados com marcas, modelos e cores de veículos brasileiros'

    def add_arguments(self, parser):
        parser.add_argument(
            '--limpar',
            action='store_true',
            help='Limpa os dados existentes antes de popular',
        )

    def handle(self, *args, **options):
        if options['limpar']:
            self.stdout.write('Limpando dados existentes...')
            self.limpar_dados()

        self.stdout.write('Iniciando população dos dados...')
        
        with transaction.atomic():
            self.criar_tipos_veiculo()
            self.criar_configuracoes_eixo()
            self.criar_cores()
            self.criar_marcas_e_modelos()
        
        self.stdout.write(
            self.style.SUCCESS('Dados populados com sucesso!')
        )

    def limpar_dados(self):
        """Limpa todos os dados auxiliares"""
        EspecificacaoTecnica.objects.all().delete()
        ModeloVeiculo.objects.all().delete()
        MarcaVeiculo.objects.all().delete()
        TipoVeiculo.objects.all().delete()
        CorVeiculo.objects.all().delete()
        ConfiguracaoEixo.objects.all().delete()

    def criar_tipos_veiculo(self):
        """Cria os tipos de veículos"""
        tipos = [
            ('caminhao', 'Caminhão'),
            ('carreta', 'Carreta'),
            ('semi_reboque', 'Semi-reboque'),
            ('reboque', 'Reboque'),
            ('bitrem', 'Bitrem'),
            ('rodotrem', 'Rodotrem'),
        ]
        
        for nome, descricao in tipos:
            TipoVeiculo.objects.get_or_create(
                nome=nome,
                defaults={'descricao': descricao}
            )
        
        self.stdout.write('✓ Tipos de veículos criados')

    def criar_configuracoes_eixo(self):
        """Cria as configurações de eixos"""
        configuracoes = [
            (2, '2 eixos - 4x2', '4x2', 16000),
            (3, '3 eixos - 6x2', '6x2', 23000),
            (4, '4 eixos - 8x4', '8x4', 33000),
            (5, '5 eixos - 10x4', '10x4', 43000),
            (6, '6 eixos - 12x4', '12x4', 53000),
            (7, '7 eixos - 14x4', '14x4', 63000),
            (9, '9 eixos - 18x4', '18x4', 74000),
        ]
        
        for qtd, desc, config, peso in configuracoes:
            ConfiguracaoEixo.objects.get_or_create(
                quantidade_eixos=qtd,
                defaults={
                    'descricao': desc,
                    'configuracao': config,
                    'peso_maximo': peso
                }
            )
        
        self.stdout.write('✓ Configurações de eixos criadas')

    def criar_cores(self):
        """Cria as cores padrão de veículos"""
        cores = [
            # Cores populares
            ('Branco', '#FFFFFF', True),
            ('Prata', '#C0C0C0', True),
            ('Azul', '#0066CC', True),
            ('Vermelho', '#CC0000', True),
            ('Preto', '#000000', True),
            
            # Cores comuns
            ('Cinza', '#808080', False),
            ('Verde', '#008000', False),
            ('Amarelo', '#FFFF00', False),
            ('Laranja', '#FF8000', False),
            ('Marrom', '#8B4513', False),
            ('Bege', '#F5F5DC', False),
            ('Dourado', '#FFD700', False),
            ('Roxo', '#800080', False),
            ('Rosa', '#FFC0CB', False),
            ('Vinho', '#722F37', False),
        ]
        
        for nome, hex_code, popular in cores:
            CorVeiculo.objects.get_or_create(
                nome=nome,
                defaults={
                    'codigo_hex': hex_code,
                    'popular': popular
                }
            )
        
        self.stdout.write('✓ Cores criadas')

    def criar_marcas_e_modelos(self):
        """Cria marcas e modelos de veículos brasileiros"""
        
        # Obter tipos de veículos
        tipo_caminhao = TipoVeiculo.objects.get(nome='caminhao')
        tipo_carreta = TipoVeiculo.objects.get(nome='carreta')
        tipo_semi_reboque = TipoVeiculo.objects.get(nome='semi_reboque')
        
        # Dados das marcas e modelos
        dados_marcas = {
            'Scania': {
                'pais': 'Suécia',
                'modelos': [
                    # Série R
                    ('R 440', tipo_caminhao, 2012, None, 3, 23000, 'DC13 440cv', 'Diesel'),
                    ('R 450', tipo_caminhao, 2012, None, 3, 23000, 'DC13 450cv', 'Diesel'),
                    ('R 480', tipo_caminhao, 2012, None, 3, 23000, 'DC13 480cv', 'Diesel'),
                    ('R 500', tipo_caminhao, 2012, None, 3, 23000, 'DC13 500cv', 'Diesel'),
                    ('R 520', tipo_caminhao, 2012, None, 3, 23000, 'DC13 520cv', 'Diesel'),
                    ('R 560', tipo_caminhao, 2012, None, 3, 23000, 'DC16 560cv', 'Diesel'),
                    ('R 620', tipo_caminhao, 2012, None, 3, 23000, 'DC16 620cv', 'Diesel'),
                    
                    # Série P
                    ('P 250', tipo_caminhao, 2012, None, 2, 16000, 'DC09 250cv', 'Diesel'),
                    ('P 280', tipo_caminhao, 2012, None, 2, 16000, 'DC09 280cv', 'Diesel'),
                    ('P 310', tipo_caminhao, 2012, None, 2, 16000, 'DC09 310cv', 'Diesel'),
                    ('P 360', tipo_caminhao, 2012, None, 3, 23000, 'DC09 360cv', 'Diesel'),
                    ('P 400', tipo_caminhao, 2012, None, 3, 23000, 'DC13 400cv', 'Diesel'),
                    
                    # Série G
                    ('G 380', tipo_caminhao, 2012, None, 2, 16000, 'DC09 380cv', 'Diesel'),
                    ('G 420', tipo_caminhao, 2012, None, 3, 23000, 'DC13 420cv', 'Diesel'),
                    ('G 440', tipo_caminhao, 2012, None, 3, 23000, 'DC13 440cv', 'Diesel'),
                ]
            },
            
            'Volvo': {
                'pais': 'Suécia',
                'modelos': [
                    # Série FH
                    ('FH 400', tipo_caminhao, 2012, None, 3, 23000, 'D11K 400cv', 'Diesel'),
                    ('FH 440', tipo_caminhao, 2012, None, 3, 23000, 'D11K 440cv', 'Diesel'),
                    ('FH 460', tipo_caminhao, 2012, None, 3, 23000, 'D13K 460cv', 'Diesel'),
                    ('FH 500', tipo_caminhao, 2012, None, 3, 23000, 'D13K 500cv', 'Diesel'),
                    ('FH 540', tipo_caminhao, 2012, None, 3, 23000, 'D13K 540cv', 'Diesel'),
                    
                    # Série FM
                    ('FM 350', tipo_caminhao, 2012, None, 2, 16000, 'D11K 350cv', 'Diesel'),
                    ('FM 370', tipo_caminhao, 2012, None, 2, 16000, 'D11K 370cv', 'Diesel'),
                    ('FM 400', tipo_caminhao, 2012, None, 3, 23000, 'D11K 400cv', 'Diesel'),
                    ('FM 440', tipo_caminhao, 2012, None, 3, 23000, 'D11K 440cv', 'Diesel'),
                    
                    # Série VM
                    ('VM 220', tipo_caminhao, 2012, None, 2, 16000, 'D5K 220cv', 'Diesel'),
                    ('VM 260', tipo_caminhao, 2012, None, 2, 16000, 'D5K 260cv', 'Diesel'),
                    ('VM 270', tipo_caminhao, 2012, None, 2, 16000, 'D5K 270cv', 'Diesel'),
                    ('VM 330', tipo_caminhao, 2012, None, 3, 23000, 'D8K 330cv', 'Diesel'),
                ]
            },
            
            'Mercedes-Benz': {
                'pais': 'Alemanha',
                'modelos': [
                    # Série Actros
                    ('Actros 2041', tipo_caminhao, 2012, None, 2, 16000, 'OM 470 410cv', 'Diesel'),
                    ('Actros 2546', tipo_caminhao, 2012, None, 3, 23000, 'OM 470 460cv', 'Diesel'),
                    ('Actros 2651', tipo_caminhao, 2012, None, 3, 23000, 'OM 473 510cv', 'Diesel'),
                    
                    # Série Atego
                    ('Atego 1719', tipo_caminhao, 2012, None, 2, 16000, 'OM 924 190cv', 'Diesel'),
                    ('Atego 1729', tipo_caminhao, 2012, None, 2, 16000, 'OM 924 290cv', 'Diesel'),
                    ('Atego 2426', tipo_caminhao, 2012, None, 3, 23000, 'OM 926 260cv', 'Diesel'),
                    
                    # Série Accelo
                    ('Accelo 815', tipo_caminhao, 2012, None, 2, 8000, 'OM 904 150cv', 'Diesel'),
                    ('Accelo 915', tipo_caminhao, 2012, None, 2, 8000, 'OM 904 150cv', 'Diesel'),
                    ('Accelo 1016', tipo_caminhao, 2012, None, 2, 10000, 'OM 904 160cv', 'Diesel'),
                ]
            },
            
            'DAF': {
                'pais': 'Holanda',
                'modelos': [
                    # Série XF
                    ('XF 440', tipo_caminhao, 2012, None, 3, 23000, 'MX-11 440cv', 'Diesel'),
                    ('XF 480', tipo_caminhao, 2012, None, 3, 23000, 'MX-13 480cv', 'Diesel'),
                    ('XF 510', tipo_caminhao, 2012, None, 3, 23000, 'MX-13 510cv', 'Diesel'),
                    
                    # Série CF
                    ('CF 370', tipo_caminhao, 2012, None, 2, 16000, 'MX-11 370cv', 'Diesel'),
                    ('CF 410', tipo_caminhao, 2012, None, 3, 23000, 'MX-11 410cv', 'Diesel'),
                    ('CF 440', tipo_caminhao, 2012, None, 3, 23000, 'MX-11 440cv', 'Diesel'),
                ]
            },
            
            'Iveco': {
                'pais': 'Itália',
                'modelos': [
                    # Série Stralis
                    ('Stralis 380', tipo_caminhao, 2012, None, 2, 16000, 'Cursor 9 380cv', 'Diesel'),
                    ('Stralis 420', tipo_caminhao, 2012, None, 3, 23000, 'Cursor 9 420cv', 'Diesel'),
                    ('Stralis 460', tipo_caminhao, 2012, None, 3, 23000, 'Cursor 13 460cv', 'Diesel'),
                    ('Stralis 500', tipo_caminhao, 2012, None, 3, 23000, 'Cursor 13 500cv', 'Diesel'),
                    
                    # Série Tector
                    ('Tector 150E22', tipo_caminhao, 2012, None, 2, 8000, 'F4AE 220cv', 'Diesel'),
                    ('Tector 170E22', tipo_caminhao, 2012, None, 2, 10000, 'F4AE 220cv', 'Diesel'),
                    ('Tector 240E25', tipo_caminhao, 2012, None, 2, 16000, 'F4AE 250cv', 'Diesel'),
                ]
            },
            
            'MAN': {
                'pais': 'Alemanha',
                'modelos': [
                    # Série TGX
                    ('TGX 28.440', tipo_caminhao, 2012, None, 3, 23000, 'D2676 440cv', 'Diesel'),
                    ('TGX 29.480', tipo_caminhao, 2012, None, 3, 23000, 'D2676 480cv', 'Diesel'),
                    ('TGX 33.540', tipo_caminhao, 2012, None, 3, 23000, 'D2676 540cv', 'Diesel'),
                    
                    # Série TGS
                    ('TGS 24.280', tipo_caminhao, 2012, None, 2, 16000, 'D0836 280cv', 'Diesel'),
                    ('TGS 26.360', tipo_caminhao, 2012, None, 3, 23000, 'D0836 360cv', 'Diesel'),
                    ('TGS 28.440', tipo_caminhao, 2012, None, 3, 23000, 'D2676 440cv', 'Diesel'),
                ]
            },
            
            'Ford': {
                'pais': 'Estados Unidos',
                'modelos': [
                    # Série Cargo
                    ('Cargo 815', tipo_caminhao, 2012, None, 2, 8000, 'Ecotorq 2.2 150cv', 'Diesel'),
                    ('Cargo 1119', tipo_caminhao, 2012, None, 2, 10000, 'Ecotorq 2.2 190cv', 'Diesel'),
                    ('Cargo 1319', tipo_caminhao, 2012, None, 2, 13000, 'Ecotorq 2.2 190cv', 'Diesel'),
                    ('Cargo 1519', tipo_caminhao, 2012, None, 2, 15000, 'Ecotorq 2.2 190cv', 'Diesel'),
                    ('Cargo 1719', tipo_caminhao, 2012, None, 2, 17000, 'Ecotorq 2.2 190cv', 'Diesel'),
                    ('Cargo 2429', tipo_caminhao, 2012, None, 3, 23000, 'Ecotorq 4.4 290cv', 'Diesel'),
                    ('Cargo 2629', tipo_caminhao, 2012, None, 3, 26000, 'Ecotorq 4.4 290cv', 'Diesel'),
                ]
            },
            
            'Volkswagen': {
                'pais': 'Alemanha',
                'modelos': [
                    # Série Constellation
                    ('Constellation 13.180', tipo_caminhao, 2012, None, 2, 13000, 'MWM 4.08 180cv', 'Diesel'),
                    ('Constellation 15.180', tipo_caminhao, 2012, None, 2, 15000, 'MWM 4.08 180cv', 'Diesel'),
                    ('Constellation 17.280', tipo_caminhao, 2012, None, 2, 17000, 'MWM 6.10 280cv', 'Diesel'),
                    ('Constellation 19.330', tipo_caminhao, 2012, None, 2, 19000, 'MWM 6.10 330cv', 'Diesel'),
                    ('Constellation 24.280', tipo_caminhao, 2012, None, 3, 23000, 'MWM 6.10 280cv', 'Diesel'),
                    ('Constellation 26.280', tipo_caminhao, 2012, None, 3, 26000, 'MWM 6.10 280cv', 'Diesel'),
                    
                    # Série Delivery
                    ('Delivery 6.160', tipo_caminhao, 2012, None, 2, 6000, 'MWM 2.8 160cv', 'Diesel'),
                    ('Delivery 8.160', tipo_caminhao, 2012, None, 2, 8000, 'MWM 2.8 160cv', 'Diesel'),
                    ('Delivery 9.170', tipo_caminhao, 2012, None, 2, 9000, 'MWM 2.8 170cv', 'Diesel'),
                    ('Delivery 11.180', tipo_caminhao, 2012, None, 2, 11000, 'MWM 4.08 180cv', 'Diesel'),
                ]
            }
        }
        
        # Criar marcas e modelos
        for nome_marca, dados in dados_marcas.items():
            marca, created = MarcaVeiculo.objects.get_or_create(
                nome=nome_marca,
                defaults={'pais_origem': dados['pais']}
            )
            
            if created:
                self.stdout.write(f'✓ Marca criada: {nome_marca}')
            
            # Criar modelos
            for modelo_data in dados['modelos']:
                nome_modelo, tipo, ano_inicio, ano_fim, eixos, capacidade, motor, combustivel = modelo_data
                
                modelo, created = ModeloVeiculo.objects.get_or_create(
                    marca=marca,
                    nome=nome_modelo,
                    ano_inicio=ano_inicio,
                    defaults={
                        'tipo_veiculo': tipo,
                        'ano_fim': ano_fim,
                        'quantidade_eixos': eixos,
                        'capacidade_carga': capacidade,
                        'motor_padrao': motor,
                        'combustivel': combustivel
                    }
                )
                
                if created:
                    self.stdout.write(f'  ✓ Modelo criado: {nome_modelo}')
        
        self.stdout.write('✓ Marcas e modelos criados')

    def criar_especificacoes_tecnicas(self):
        """Cria especificações técnicas para alguns modelos"""
        # Implementar especificações detalhadas se necessário
        pass

