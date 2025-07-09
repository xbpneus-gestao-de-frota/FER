# XBPNEUS Premium - Sistema de Gestão de Pneus

Sistema Django completo para gestão de pneus com interface moderna e funcionalidades avançadas.

## 🚀 Funcionalidades

- **Gestão de Produtos**: Catálogo completo de pneus com especificações técnicas
- **Sistema de Categorias**: Organização por categorias e marcas
- **Página de Serviços**: Apresentação dos serviços oferecidos
- **Formulário de Contato**: Sistema de mensagens integrado
- **Interface Responsiva**: Design moderno e adaptável
- **Painel Administrativo**: Django Admin customizado
- **SEO Otimizado**: URLs amigáveis e meta tags

## 🛠️ Tecnologias

- **Backend**: Django 4.2+
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Banco de Dados**: SQLite (desenvolvimento) / PostgreSQL (produção)
- **Deploy**: Docker, Railway
- **Outros**: Font Awesome, Gunicorn, WhiteNoise

## 📦 Instalação Local

### Pré-requisitos
- Python 3.11+
- pip
- Git

### Passo a Passo

1. **Clone o repositório**
```bash
git clone https://github.com/seu-usuario/xbpneus-premium.git
cd xbpneus-premium
```

2. **Crie um ambiente virtual**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Execute as migrações**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Crie um superusuário**
```bash
python manage.py createsuperuser
```

6. **Colete arquivos estáticos**
```bash
python manage.py collectstatic
```

7. **Execute o servidor**
```bash
python manage.py runserver
```

8. **Acesse o sistema**
- Site: http://localhost:8000
- Admin: http://localhost:8000/admin

## 🚀 Deploy

### Railway (Recomendado)

1. **Conecte seu repositório GitHub ao Railway**
2. **Configure as variáveis de ambiente**:
   - `DJANGO_SETTINGS_MODULE=xbpneus.config.settings`
   - `DEBUG=False`
   - `SECRET_KEY=sua-chave-secreta`

3. **O deploy será automático** usando o `railway.json` e `Dockerfile`

### Docker

```bash
# Build da imagem
docker build -t xbpneus-premium .

# Execute o container
docker run -p 8000:8000 xbpneus-premium
```

## 📁 Estrutura do Projeto

```
xbpneus-premium-complete/
├── manage.py
├── requirements.txt
├── Dockerfile
├── railway.json
├── .gitignore
├── README.md
└── xbpneus/
    ├── __init__.py
    ├── config/
    │   ├── __init__.py
    │   ├── settings.py
    │   ├── urls.py
    │   ├── wsgi.py
    │   └── asgi.py
    ├── core/
    │   ├── __init__.py
    │   ├── apps.py
    │   ├── models.py
    │   └── admin.py
    ├── apps/
    │   ├── home/
    │   ├── produtos/
    │   ├── servicos/
    │   └── contato/
    ├── static/
    │   ├── css/
    │   ├── js/
    │   └── images/
    ├── templates/
    │   ├── base/
    │   ├── home/
    │   ├── produtos/
    │   ├── servicos/
    │   └── contato/
    └── media/
```

## 🎨 Customização

### Cores e Estilos
Edite o arquivo `xbpneus/static/css/style.css` para personalizar:
- Cores primárias e secundárias
- Fontes e tipografia
- Espaçamentos e layouts

### Conteúdo
- **Textos**: Edite os templates em `xbpneus/templates/`
- **Imagens**: Adicione em `xbpneus/static/images/`
- **Configurações**: Modifique `xbpneus/config/settings.py`

## 📊 Funcionalidades do Admin

Acesse `/admin` para gerenciar:
- **Produtos**: Cadastro completo com especificações
- **Categorias**: Organização dos produtos
- **Marcas**: Fabricantes de pneus
- **Serviços**: Serviços oferecidos
- **Contatos**: Mensagens recebidas
- **Configurações**: Parâmetros do sistema

## 🔧 Comandos Úteis

```bash
# Criar migrações
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Coletar arquivos estáticos
python manage.py collectstatic

# Executar testes
python manage.py test

# Shell Django
python manage.py shell
```

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📞 Suporte

Para suporte e dúvidas:
- Email: contato@xbpneus.com
- Issues: [GitHub Issues](https://github.com/seu-usuario/xbpneus-premium/issues)

---

**XBPNEUS Premium** - Tecnologia avançada em gestão de pneus 🚗

