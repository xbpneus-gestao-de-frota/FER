#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'xbpneus.config.settings')
django.setup()

from xbpneus.apps.subusuarios.models import ModuloAcesso

# Lista de módulos/pilares
MODULOS = [
    {"nome": "Dashboard", "slug": "dashboard", "descricao": "Painel principal do sistema", "icone": "bi-speedometer2", "ordem": 1},
    {"nome": "Frota", "slug": "frota", "descricao": "Gestão da frota de veículos", "icone": "bi-truck", "ordem": 2},
    {"nome": "Estoque", "slug": "estoque", "descricao": "Controle de estoque de pneus", "icone": "bi-box-seam", "ordem": 3},
    {"nome": "Manutenção", "slug": "manutencao", "descricao": "Gestão de manutenções", "icone": "bi-tools", "ordem": 4},
    {"nome": "Relatórios", "slug": "relatorios", "descricao": "Relatórios e análises", "icone": "bi-graph-up", "ordem": 5},
    {"nome": "Financeiro", "slug": "financeiro", "descricao": "Gestão financeira", "icone": "bi-currency-dollar", "ordem": 6},
    {"nome": "Compras", "slug": "compras", "descricao": "Gestão de compras", "icone": "bi-cart", "ordem": 7},
    {"nome": "Eventos", "slug": "eventos", "descricao": "Gestão de eventos", "icone": "bi-calendar-event", "ordem": 8},
    {"nome": "Notícias", "slug": "noticias", "descricao": "Gestão de notícias", "icone": "bi-newspaper", "ordem": 9},
    {"nome": "Configurações", "slug": "configuracoes", "descricao": "Configurações do sistema", "icone": "bi-gear", "ordem": 10},
]

print("Criando módulos no banco PostgreSQL...")

for modulo_data in MODULOS:
    modulo, created = ModuloAcesso.objects.get_or_create(
        nome=modulo_data["nome"],
        defaults={
            'slug': modulo_data["slug"],
            'descricao': modulo_data["descricao"],
            'icone': modulo_data["icone"],
            'ativo': True,
            'ordem': modulo_data["ordem"]
        }
    )
    
    if created:
        print(f"✅ Módulo '{modulo.nome}' criado com sucesso!")
    else:
        print(f"ℹ️  Módulo '{modulo.nome}' já existe.")

print(f"\n🎉 Total de módulos ativos: {ModuloAcesso.objects.filter(ativo=True).count()}")
print("Módulos criados/validados com sucesso!")
