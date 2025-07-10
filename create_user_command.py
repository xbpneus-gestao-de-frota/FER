#!/usr/bin/env python
"""
Comando Django para criar usuário de teste
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'xbpneus.config.settings')
django.setup()

from django.contrib.auth.models import User

def create_test_user():
    username = 'cliente_teste'
    password = 'senha123'
    email = 'cliente@teste.com'
    
    try:
        # Deletar usuário existente se houver
        if User.objects.filter(username=username).exists():
            User.objects.filter(username=username).delete()
            print(f"🗑️ Usuário existente '{username}' removido")
        
        # Criar novo usuário
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.is_active = True
        user.save()
        
        print(f"✅ Usuário '{username}' criado com sucesso!")
        print(f"📧 Email: {email}")
        print(f"🔑 Senha: {password}")
        
        # Testar autenticação
        from django.contrib.auth import authenticate
        auth_user = authenticate(username=username, password=password)
        if auth_user:
            print(f"✅ Teste de autenticação: SUCESSO")
        else:
            print(f"❌ Teste de autenticação: FALHOU")
            
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar usuário: {e}")
        return False

if __name__ == '__main__':
    create_test_user()

