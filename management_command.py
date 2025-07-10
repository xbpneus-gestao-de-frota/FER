#!/usr/bin/env python
"""
Comando de gerenciamento Django para criar usuário em produção
"""
import os
import sys
import django
from django.core.management.base import BaseCommand

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'xbpneus.config.settings')
django.setup()

from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Criar usuário de teste'

    def handle(self, *args, **options):
        username = 'cliente_teste'
        password = 'senha123'
        email = 'cliente@teste.com'
        
        try:
            # Deletar usuário existente se houver
            User.objects.filter(username=username).delete()
            
            # Criar novo usuário
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            user.is_active = True
            user.save()
            
            self.stdout.write(
                self.style.SUCCESS(f'Usuário "{username}" criado com sucesso!')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Erro ao criar usuário: {e}')
            )

# Executar diretamente
if __name__ == '__main__':
    cmd = Command()
    cmd.handle()

