#!/bin/bash

echo "🚀 Verificando ambiente para deploy..."

# Verifica Procfile
if [ -f "Procfile" ]; then
  echo "✅ Procfile encontrado"
else
  echo "❌ Procfile ausente!"
fi

# Verifica gunicorn
if grep -q gunicorn requirements.txt; then
  echo "✅ gunicorn está no requirements.txt"
else
  echo "❌ gunicorn ausente do requirements.txt!"
fi

# Verifica migrações
echo "📦 Verificando migrações..."
python manage.py makemigrations --check

# Verifica collectstatic
echo "🎯 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

echo "✅ Verificações concluídas. Pronto para deploy."

