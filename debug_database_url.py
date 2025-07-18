#!/usr/bin/env python3
"""
Script de debug para verificar a variável DATABASE_URL
"""
import os
import sys

def debug_database_url():
    print("🔍 DEBUG DATABASE_URL")
    print("=" * 50)
    
    # Verificar se DATABASE_URL existe
    database_url = os.environ.get('DATABASE_URL')
    
    print(f"DATABASE_URL existe: {database_url is not None}")
    
    if database_url:
        print(f"DATABASE_URL valor: '{database_url}'")
        print(f"DATABASE_URL length: {len(database_url)}")
        print(f"DATABASE_URL stripped: '{database_url.strip()}'")
        print(f"DATABASE_URL é vazia após strip: {not database_url.strip()}")
        
        # Verificar se começa com scheme válido
        valid_schemes = ['postgresql://', 'postgres://', 'sqlite://', 'mysql://']
        has_valid_scheme = any(database_url.startswith(scheme) for scheme in valid_schemes)
        print(f"Tem scheme válido: {has_valid_scheme}")
        
        if database_url.startswith('://'):
            print("❌ ERRO: DATABASE_URL começa com '://' - scheme inválido!")
        
    else:
        print("❌ DATABASE_URL não está definida!")
    
    print("\n🔧 VARIÁVEIS DE AMBIENTE RELACIONADAS:")
    for key, value in os.environ.items():
        if 'DATABASE' in key.upper() or 'DB' in key.upper() or 'POSTGRES' in key.upper():
            print(f"{key}: {value}")
    
    print("\n✅ TESTE CONCLUÍDO")

if __name__ == "__main__":
    debug_database_url()

