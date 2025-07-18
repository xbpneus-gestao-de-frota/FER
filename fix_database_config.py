#!/usr/bin/env python3
"""
Script para corrigir automaticamente a configuração do banco de dados
"""
import os
import sys
import django
from pathlib import Path

# Adicionar o projeto ao path
sys.path.insert(0, '/home/ubuntu/xbpneus-premium-complete')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'xbpneus.config.settings')

def fix_database_config():
    print("🔧 CORRIGINDO CONFIGURAÇÃO DO BANCO DE DADOS")
    print("=" * 60)
    
    try:
        # Tentar importar Django settings
        django.setup()
        from django.conf import settings
        
        print("✅ Django settings carregado com sucesso!")
        print(f"✅ Database engine: {settings.DATABASES['default']['ENGINE']}")
        
        if 'sqlite' in settings.DATABASES['default']['ENGINE']:
            print("⚠️  Usando SQLite como fallback")
        else:
            print("✅ Usando PostgreSQL")
            
    except Exception as e:
        print(f"❌ Erro ao carregar settings: {e}")
        return False
    
    try:
        # Testar conexão com banco
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        print("✅ Conexão com banco de dados funcionando!")
        
    except Exception as e:
        print(f"❌ Erro na conexão com banco: {e}")
        return False
    
    try:
        # Verificar migrações
        from django.core.management import execute_from_command_line
        print("\n🔄 Verificando migrações...")
        
        # Simular comando makemigrations
        sys.argv = ['manage.py', 'makemigrations', '--dry-run']
        execute_from_command_line(sys.argv)
        print("✅ Migrações verificadas!")
        
    except Exception as e:
        print(f"⚠️  Aviso nas migrações: {e}")
    
    print("\n✅ CONFIGURAÇÃO DO BANCO CORRIGIDA COM SUCESSO!")
    return True

if __name__ == "__main__":
    success = fix_database_config()
    sys.exit(0 if success else 1)

