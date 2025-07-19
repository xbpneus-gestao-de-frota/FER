#!/usr/bin/env python3
"""
Script de diagnóstico completo para testar o boot da aplicação Django XBPNEUS
Identifica a causa raiz exata dos crashes persistentes no Railway
"""

import os
import sys
import traceback
from pathlib import Path

print("🔍 INICIANDO DIAGNÓSTICO COMPLETO DO BOOT DJANGO XBPNEUS")
print("=" * 60)

def test_django_boot():
    """Testa o boot do Django linha a linha"""
    try:
        print("⚙️  1. Configurando DJANGO_SETTINGS_MODULE...")
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'xbpneus.config.settings')
        print("✅ Settings module configurado")

        print("\n⚙️  2. Importando Django...")
        import django
        print("✅ Django importado com sucesso")

        print("\n⚙️  3. Inicializando Django (django.setup())...")
        django.setup()
        print("✅ Django inicializado com sucesso!")

        print("\n⚙️  4. Testando importação de settings...")
        from django.conf import settings
        print(f"✅ Settings carregado - DEBUG: {settings.DEBUG}")
        print(f"✅ Database engine: {settings.DATABASES['default']['ENGINE']}")

        print("\n⚙️  5. Testando conexão com banco de dados...")
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
        print("✅ Conexão com banco de dados funcionando")

        print("\n⚙️  6. Verificando apps instalados...")
        for app in settings.INSTALLED_APPS:
            print(f"   - {app}")
        print("✅ Apps instalados verificados")

        print("\n⚙️  7. Testando importação de URLs...")
        from django.urls import get_resolver
        resolver = get_resolver()
        print("✅ URLs carregadas com sucesso")

        print("\n⚙️  8. Executando django check...")
        from django.core.management import call_command
        call_command('check', verbosity=0)
        print("✅ Django check passou sem erros")

        print("\n⚙️  9. Testando migrações...")
        call_command('makemigrations', check=True, dry_run=True, verbosity=0)
        print("✅ Migrações verificadas")

        print("\n⚙️  10. Testando collectstatic...")
        call_command('collectstatic', dry_run=True, verbosity=0, interactive=False)
        print("✅ Collectstatic testado")

        print("\n🎉 SUCESSO TOTAL! Django inicializado sem erros!")
        print("✅ O problema NÃO está no código Django")
        print("✅ O problema deve estar no ambiente Railway")
        
        return True

    except Exception as e:
        print(f"\n❌ ERRO DETECTADO DURANTE O BOOT:")
        print(f"Tipo do erro: {type(e).__name__}")
        print(f"Mensagem: {str(e)}")
        print("\n📋 TRACEBACK COMPLETO:")
        traceback.print_exc()
        
        print("\n🎯 ANÁLISE DO ERRO:")
        error_str = str(e).lower()
        if 'module' in error_str and 'not found' in error_str:
            print("🔍 Erro de módulo não encontrado - verifique INSTALLED_APPS")
        elif 'database' in error_str or 'connection' in error_str:
            print("🔍 Erro de conexão com banco - verifique DATABASE_URL")
        elif 'import' in error_str:
            print("🔍 Erro de importação - verifique dependências")
        elif 'settings' in error_str:
            print("🔍 Erro de configuração - verifique settings.py")
        else:
            print("🔍 Erro desconhecido - análise manual necessária")
        
        return False

def test_environment():
    """Testa o ambiente e variáveis"""
    print("\n🌍 TESTANDO AMBIENTE:")
    print(f"Python version: {sys.version}")
    print(f"Working directory: {os.getcwd()}")
    
    # Verifica variáveis de ambiente importantes
    env_vars = ['DATABASE_URL', 'SECRET_KEY', 'DEBUG', 'DJANGO_SETTINGS_MODULE']
    for var in env_vars:
        value = os.environ.get(var, 'NÃO DEFINIDA')
        if var == 'SECRET_KEY' and value != 'NÃO DEFINIDA':
            value = f"{value[:10]}..." if len(value) > 10 else value
        print(f"{var}: {value}")

def test_file_structure():
    """Verifica estrutura de arquivos"""
    print("\n📁 VERIFICANDO ESTRUTURA DE ARQUIVOS:")
    
    required_files = [
        'manage.py',
        'Procfile',
        'requirements.txt',
        'xbpneus/config/settings.py',
        'xbpneus/config/urls.py',
        'xbpneus/config/wsgi.py',
    ]
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - AUSENTE!")

def main():
    """Função principal do diagnóstico"""
    try:
        # Testa ambiente
        test_environment()
        
        # Testa estrutura de arquivos
        test_file_structure()
        
        # Testa boot do Django
        success = test_django_boot()
        
        print("\n" + "=" * 60)
        if success:
            print("🎉 DIAGNÓSTICO CONCLUÍDO - DJANGO FUNCIONANDO LOCALMENTE!")
            print("🎯 O problema está no ambiente Railway, não no código")
            print("🔧 Recomendação: Verificar logs específicos do Railway")
        else:
            print("❌ DIAGNÓSTICO CONCLUÍDO - ERRO IDENTIFICADO!")
            print("🎯 Corrija o erro acima e execute novamente")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\n⚠️  Diagnóstico interrompido pelo usuário")
    except Exception as e:
        print(f"\n💥 ERRO CRÍTICO NO SCRIPT DE DIAGNÓSTICO:")
        traceback.print_exc()

if __name__ == "__main__":
    main()

