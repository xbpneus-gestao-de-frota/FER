#!/bin/bash

echo "🚀 SCRIPT DE DEPLOY OTIMIZADO PARA RAILWAY"
echo "=========================================="

# Coleta arquivos estáticos
echo "📦 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

# Aplica migrações
echo "🗄️ Aplicando migrações..."
python manage.py migrate --noinput

# Verifica se tudo está OK
echo "🔍 Verificando sistema..."
python manage.py check

echo "✅ Deploy preparado com sucesso!"
echo "🎯 Sistema pronto para inicialização no Railway"

