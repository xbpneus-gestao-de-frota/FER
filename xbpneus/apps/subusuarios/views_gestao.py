from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.hashers import make_password
import json
import secrets
import string

from .models import SubUsuario, ModuloAcesso
from .forms import SubUsuarioForm


@login_required
def gestao_subusuarios(request):
    """
    View principal para gestão de subusuários
    Exibe lista de todos os subusuários com filtros e estatísticas
    """
    
    # Busca e filtros
    busca = request.GET.get('busca', '')
    status_filtro = request.GET.get('status', '')
    pilar_filtro = request.GET.get('pilar', '')
    
    # Query base
    subusuarios = SubUsuario.objects.all().prefetch_related('modulos')
    
    # Aplicar filtros
    if busca:
        subusuarios = subusuarios.filter(
            Q(nome__icontains=busca) |
            Q(email__icontains=busca) |
            Q(funcao__icontains=busca) |
            Q(login__icontains=busca)
        )
    
    if status_filtro == 'ativo':
        subusuarios = subusuarios.filter(ativo=True)
    elif status_filtro == 'inativo':
        subusuarios = subusuarios.filter(ativo=False)
    
    if pilar_filtro:
        subusuarios = subusuarios.filter(modulos__slug=pilar_filtro).distinct()
    
    # Estatísticas
    total_usuarios = SubUsuario.objects.count()
    usuarios_ativos = SubUsuario.objects.filter(ativo=True).count()
    usuarios_inativos = total_usuarios - usuarios_ativos
    
    # Módulos para filtro
    modulos = ModuloAcesso.objects.filter(ativo=True).order_by('ordem', 'nome')
    
    context = {
        'subusuarios': subusuarios.order_by('-data_criacao'),
        'modulos': modulos,
        'total_usuarios': total_usuarios,
        'usuarios_ativos': usuarios_ativos,
        'usuarios_inativos': usuarios_inativos,
        'total_modulos': modulos.count(),
        'busca': busca,
        'status_filtro': status_filtro,
        'pilar_filtro': pilar_filtro,
    }
    
    return render(request, 'subusuarios/gestao_subusuarios.html', context)


@login_required
def cadastrar_subusuario_completo(request):
    """
    View para cadastrar novo subusuário com interface completa
    """
    
    if request.method == 'POST':
        form = SubUsuarioForm(request.POST)
        
        if form.is_valid():
            try:
                subusuario = form.save(commit=False)
                
                # Define o usuário principal (quem está criando)
                subusuario.usuario_principal = request.user
                
                # Criptografa a senha
                if form.cleaned_data.get('senha'):
                    subusuario.senha = make_password(form.cleaned_data['senha'])
                
                subusuario.save()
                
                # Salva os módulos (many-to-many)
                form.save_m2m()
                
                messages.success(
                    request, 
                    f'Subusuário "{subusuario.nome}" criado com sucesso!'
                )
                
                return redirect('subusuarios:gestao_subusuarios')
                
            except Exception as e:
                messages.error(
                    request, 
                    f'Erro ao criar subusuário: {str(e)}'
                )
        else:
            messages.error(
                request, 
                'Corrija os erros abaixo e tente novamente.'
            )
    else:
        form = SubUsuarioForm()
    
    context = {
        'form': form,
        'title': 'Novo Subusuário',
        'action': 'create'
    }
    
    return render(request, 'subusuarios/subusuario_form_completo.html', context)


@login_required
def editar_subusuario(request, subusuario_id):
    """
    View para editar subusuário existente
    """
    
    subusuario = get_object_or_404(SubUsuario, id=subusuario_id)
    
    if request.method == 'POST':
        form = SubUsuarioForm(request.POST, instance=subusuario)
        
        if form.is_valid():
            try:
                subusuario = form.save()
                
                messages.success(
                    request, 
                    f'Subusuário "{subusuario.nome}" atualizado com sucesso!'
                )
                
                return redirect('subusuarios:gestao_subusuarios')
                
            except Exception as e:
                messages.error(
                    request, 
                    f'Erro ao atualizar subusuário: {str(e)}'
                )
        else:
            messages.error(
                request, 
                'Corrija os erros abaixo e tente novamente.'
            )
    else:
        form = SubUsuarioForm(instance=subusuario)
    
    context = {
        'form': form,
        'title': f'Editar {subusuario.nome}',
        'action': 'edit',
        'subusuario': subusuario
    }
    
    return render(request, 'subusuarios/subusuario_form_completo.html', context)


@login_required
@require_http_methods(["POST"])
def toggle_status_subusuario(request, subusuario_id):
    """
    API para ativar/desativar subusuário via AJAX
    """
    
    try:
        subusuario = get_object_or_404(SubUsuario, id=subusuario_id)
        
        # Lê o novo status do corpo da requisição
        data = json.loads(request.body)
        novo_status = data.get('status', not subusuario.ativo)
        
        subusuario.ativo = novo_status
        subusuario.save()
        
        action = 'ativado' if novo_status else 'desativado'
        
        return JsonResponse({
            'success': True,
            'message': f'Usuário {action} com sucesso',
            'new_status': novo_status
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Erro ao alterar status: {str(e)}'
        }, status=400)


@login_required
@require_http_methods(["POST"])
def reset_password_subusuario(request, subusuario_id):
    """
    API para resetar senha do subusuário
    """
    
    try:
        subusuario = get_object_or_404(SubUsuario, id=subusuario_id)
        
        # Gera nova senha aleatória
        nova_senha = gerar_senha_aleatoria()
        
        # Atualiza a senha
        subusuario.senha = make_password(nova_senha)
        subusuario.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Senha resetada com sucesso',
            'new_password': nova_senha
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Erro ao resetar senha: {str(e)}'
        }, status=400)


@login_required
@require_http_methods(["DELETE"])
def delete_subusuario(request, subusuario_id):
    """
    API para excluir subusuário
    """
    
    try:
        subusuario = get_object_or_404(SubUsuario, id=subusuario_id)
        nome_usuario = subusuario.nome
        
        subusuario.delete()
        
        return JsonResponse({
            'success': True,
            'message': f'Usuário "{nome_usuario}" excluído com sucesso'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Erro ao excluir usuário: {str(e)}'
        }, status=400)


@login_required
def view_permissions_subusuario(request, subusuario_id):
    """
    View para visualizar permissões detalhadas do subusuário
    """
    
    subusuario = get_object_or_404(SubUsuario, id=subusuario_id)
    
    # Módulos do usuário
    modulos_usuario = subusuario.modulos.all().order_by('ordem', 'nome')
    
    # Todos os módulos disponíveis
    todos_modulos = ModuloAcesso.objects.filter(ativo=True).order_by('ordem', 'nome')
    
    context = {
        'subusuario': subusuario,
        'modulos_usuario': modulos_usuario,
        'todos_modulos': todos_modulos,
    }
    
    return render(request, 'subusuarios/permissions_detail.html', context)


def gerar_senha_aleatoria(tamanho=12):
    """
    Gera uma senha aleatória segura
    """
    
    caracteres = string.ascii_letters + string.digits + "!@#$%&*"
    
    # Garante pelo menos um de cada tipo
    senha = [
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.digits),
        secrets.choice("!@#$%&*")
    ]
    
    # Completa o restante aleatoriamente
    for _ in range(tamanho - 4):
        senha.append(secrets.choice(caracteres))
    
    # Embaralha a senha
    secrets.SystemRandom().shuffle(senha)
    
    return ''.join(senha)


@login_required
def dashboard_subusuarios(request):
    """
    Dashboard com estatísticas e métricas dos subusuários
    """
    
    # Estatísticas gerais
    stats = {
        'total_usuarios': SubUsuario.objects.count(),
        'usuarios_ativos': SubUsuario.objects.filter(ativo=True).count(),
        'usuarios_inativos': SubUsuario.objects.filter(ativo=False).count(),
        'total_modulos': ModuloAcesso.objects.filter(ativo=True).count(),
    }
    
    # Usuários criados recentemente (últimos 7 dias)
    from datetime import datetime, timedelta
    data_limite = datetime.now() - timedelta(days=7)
    usuarios_recentes = SubUsuario.objects.filter(
        data_criacao__gte=data_limite
    ).order_by('-data_criacao')[:5]
    
    # Módulos mais utilizados
    from django.db.models import Count
    modulos_populares = ModuloAcesso.objects.annotate(
        total_usuarios=Count('subusuarios')
    ).filter(ativo=True).order_by('-total_usuarios')[:5]
    
    context = {
        'stats': stats,
        'usuarios_recentes': usuarios_recentes,
        'modulos_populares': modulos_populares,
    }
    
    return render(request, 'subusuarios/dashboard.html', context)

