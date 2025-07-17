from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q, Count
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from .models import SubUsuario, ModuloAcesso
from .forms import SubUsuarioForm
from .utils import enviar_convite_subusuario, reenviar_convite_subusuario, validar_token_convite, definir_senha_subusuario


@login_required
def listar_subusuarios(request):
    """Lista todos os subusuários do usuário principal"""
    subusuarios = SubUsuario.objects.filter(usuario_principal=request.user)
    
    # Estatísticas
    stats = {
        'total': subusuarios.count(),
        'ativos': subusuarios.filter(ativo=True).count(),
        'inativos': subusuarios.filter(ativo=False).count(),
    }
    
    context = {
        'subusuarios': subusuarios,
        'stats': stats,
    }
    return render(request, 'subusuarios/subusuarios_list.html', context)


@login_required
def cadastrar_subusuario(request):
    """Cadastra um novo subusuário"""
    if request.method == 'POST':
        form = SubUsuarioForm(request.POST, usuario_principal=request.user)
        if form.is_valid():
            subusuario = form.save()
            
            # Verificar se deve enviar convite
            if form.cleaned_data.get('enviar_convite'):
                if enviar_convite_subusuario(subusuario, request):
                    messages.success(
                        request, 
                        f'Subusuário "{subusuario.nome}" cadastrado com sucesso! '
                        f'Convite enviado para {subusuario.email}.'
                    )
                else:
                    messages.warning(
                        request, 
                        f'Subusuário "{subusuario.nome}" cadastrado, mas houve erro ao enviar o convite. '
                        f'Você pode reenviar o convite na listagem.'
                    )
            else:
                messages.success(
                    request, 
                    f'Subusuário "{subusuario.nome}" cadastrado com sucesso!'
                )
            
            return redirect('configuracoes:subusuarios:listar_subusuarios')
    else:
        form = SubUsuarioForm(usuario_principal=request.user)
    
    context = {
        'form': form,
        'titulo': 'Cadastrar Subusuário',
        'botao_texto': 'Cadastrar',
    }
    return render(request, 'subusuarios/subusuarios_form_novo.html', context)


@login_required
def editar_subusuario(request, subusuario_id):
    """Edita um subusuário existente"""
    subusuario = get_object_or_404(
        SubUsuario, 
        id=subusuario_id, 
        usuario_principal=request.user
    )
    
    if request.method == 'POST':
        form = SubUsuarioForm(
            request.POST, 
            instance=subusuario, 
            usuario_principal=request.user
        )
        if form.is_valid():
            form.save()
            messages.success(request, f'Subusuário "{subusuario.nome}" atualizado com sucesso!')
            return redirect('configuracoes:subusuarios:listar_subusuarios')
    else:
        form = SubUsuarioForm(instance=subusuario, usuario_principal=request.user)
    
    context = {
        'form': form,
        'subusuario': subusuario,
        'titulo': 'Editar Subusuário',
        'botao_texto': 'Atualizar',
    }
    return render(request, 'subusuarios/subusuarios_form_novo.html', context)


@login_required
def detalhes_subusuario(request, subusuario_id):
    """Exibe detalhes de um subusuário"""
    subusuario = get_object_or_404(
        SubUsuario, 
        id=subusuario_id, 
        usuario_principal=request.user
    )
    
    context = {
        'subusuario': subusuario,
    }
    return render(request, 'subusuarios/subusuarios_detail.html', context)


@login_required
def excluir_subusuario(request, subusuario_id):
    """Exclui um subusuário"""
    subusuario = get_object_or_404(
        SubUsuario, 
        id=subusuario_id, 
        usuario_principal=request.user
    )
    
    if request.method == 'POST':
        nome = subusuario.nome
        subusuario.delete()
        messages.success(request, f'Subusuário "{nome}" excluído com sucesso!')
        return redirect('configuracoes:subusuarios:listar_subusuarios')
    
    context = {
        'subusuario': subusuario,
    }
    return render(request, 'subusuarios/subusuarios_confirm_delete.html', context)


@login_required
def alternar_status_subusuario(request, subusuario_id):
    """Alterna status ativo/inativo de um subusuário"""
    subusuario = get_object_or_404(
        SubUsuario, 
        id=subusuario_id, 
        usuario_principal=request.user
    )
    
    subusuario.ativo = not subusuario.ativo
    subusuario.save()
    
    status = "ativado" if subusuario.ativo else "desativado"
    messages.success(request, f'Subusuário "{subusuario.nome}" {status} com sucesso!')
    
    return redirect('configuracoes:subusuarios:listar_subusuarios')


# ===== VIEWS PARA GESTÃO DE MÓDULOS =====

@login_required
def listar_modulos(request):
    """Lista módulos de acesso"""
    modulos = ModuloAcesso.objects.all()
    
    context = {
        'modulos': modulos,
    }
    return render(request, 'subusuarios/modulos_list.html', context)


# ===== CONVITES E DEFINIÇÃO DE SENHA =====

def definir_senha(request, token):
    """Permite que subusuário defina sua senha via token"""
    subusuario = validar_token_convite(token)
    
    if not subusuario:
        messages.error(request, 'Token inválido ou expirado.')
        return redirect('login')
    
    if request.method == 'POST':
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')
        
        if senha != confirmar_senha:
            messages.error(request, 'As senhas não coincidem.')
        else:
            try:
                validate_password(senha)
                definir_senha_subusuario(subusuario, senha, token)
                messages.success(request, 'Senha definida com sucesso! Você já pode fazer login.')
                return redirect('login')
            except ValidationError as e:
                messages.error(request, ' '.join(e.messages))
    
    context = {
        'subusuario': subusuario,
        'token': token,
    }
    return render(request, 'subusuarios/definir_senha.html', context)


@login_required
def enviar_convite(request, subusuario_id):
    """Envia convite para subusuário"""
    subusuario = get_object_or_404(
        SubUsuario, 
        id=subusuario_id, 
        usuario_principal=request.user
    )
    
    if enviar_convite_subusuario(subusuario, request):
        messages.success(
            request, 
            f'Convite enviado para {subusuario.email} com sucesso!'
        )
    else:
        messages.error(
            request, 
            f'Erro ao enviar convite para {subusuario.email}. Tente novamente.'
        )
    
    return redirect('configuracoes:subusuarios:listar_subusuarios')


@login_required
def reenviar_convite(request, subusuario_id):
    """Reenvia convite para subusuário"""
    return enviar_convite(request, subusuario_id)


# ===== AJAX ENDPOINTS =====

@login_required
def ajax_validar_login(request):
    """Valida se login já existe via AJAX"""
    login = request.GET.get('login', '').strip()
    subusuario_id = request.GET.get('subusuario_id')
    
    if not login:
        return JsonResponse({'disponivel': True})
    
    queryset = SubUsuario.objects.filter(
        login=login, 
        usuario_principal=request.user
    )
    
    # Se estamos editando, excluir o próprio registro
    if subusuario_id:
        queryset = queryset.exclude(id=subusuario_id)
    
    disponivel = not queryset.exists()
    
    return JsonResponse({'disponivel': disponivel})


@login_required
def ajax_validar_email(request):
    """Valida se email já existe via AJAX"""
    email = request.GET.get('email', '').strip()
    subusuario_id = request.GET.get('subusuario_id')
    
    if not email:
        return JsonResponse({'disponivel': True})
    
    queryset = SubUsuario.objects.filter(
        email=email, 
        usuario_principal=request.user
    )
    
    # Se estamos editando, excluir o próprio registro
    if subusuario_id:
        queryset = queryset.exclude(id=subusuario_id)
    
    disponivel = not queryset.exists()
    
    return JsonResponse({'disponivel': disponivel})


# ===== DECORATORS E UTILITÁRIOS =====

def require_module_access(module_slug):
    """Decorator para verificar acesso a módulo específico"""
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            # Verificar se o usuário tem acesso ao módulo
            # Implementar lógica de verificação aqui
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def get_user_modules(user):
    """Retorna módulos acessíveis pelo usuário"""
    if hasattr(user, 'subusuario'):
        return user.subusuario.get_modulos_ativos()
    else:
        # Usuário principal tem acesso a todos os módulos
        return ModuloAcesso.objects.filter(ativo=True)

