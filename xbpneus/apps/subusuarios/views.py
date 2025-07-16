from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q, Count
from .models import SubUsuario, ModuloAcesso, PerfilAcesso
from .forms import SubUsuarioForm, PerfilAcessoForm, ModuloAcessoForm, FiltroSubUsuarioForm


@login_required
def listar_subusuarios(request):
    """Lista todos os subusuários do usuário principal com filtros"""
    subusuarios = SubUsuario.objects.filter(usuario_principal=request.user)
    form = FiltroSubUsuarioForm(request.GET)
    
    # Aplicar filtros
    if form.is_valid():
        if form.cleaned_data['funcao']:
            subusuarios = subusuarios.filter(funcao=form.cleaned_data['funcao'])
        if form.cleaned_data['ativo']:
            ativo = form.cleaned_data['ativo'] == 'True'
            subusuarios = subusuarios.filter(ativo=ativo)
        if form.cleaned_data['modulo']:
            subusuarios = subusuarios.filter(modulos=form.cleaned_data['modulo'])
    
    # Estatísticas
    stats = {
        'total': subusuarios.count(),
        'ativos': subusuarios.filter(ativo=True).count(),
        'inativos': subusuarios.filter(ativo=False).count(),
    }
    
    context = {
        'subusuarios': subusuarios,
        'form': form,
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
        'perfis_acesso': PerfilAcesso.objects.filter(ativo=True),
    }
    return render(request, 'subusuarios/subusuarios_form.html', context)


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
            messages.success(
                request, 
                f'Subusuário "{subusuario.nome}" atualizado com sucesso!'
            )
            return redirect('configuracoes:subusuarios:listar_subusuarios')
    else:
        form = SubUsuarioForm(instance=subusuario, usuario_principal=request.user)
    
    context = {
        'form': form,
        'subusuario': subusuario,
        'titulo': 'Editar Subusuário',
        'botao_texto': 'Atualizar',
        'perfis_acesso': PerfilAcesso.objects.filter(ativo=True),
    }
    return render(request, 'subusuarios/subusuarios_form.html', context)


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
        'modulos_acesso': subusuario.get_modulos_ativos(),
    }
    return render(request, 'subusuarios/subusuarios_detalhes.html', context)


@login_required
@require_POST
def excluir_subusuario(request, subusuario_id):
    """Exclui um subusuário"""
    subusuario = get_object_or_404(
        SubUsuario, 
        id=subusuario_id, 
        usuario_principal=request.user
    )
    
    nome = subusuario.nome
    subusuario.delete()
    
    messages.success(request, f'Subusuário "{nome}" excluído com sucesso!')
    return redirect('configuracoes:subusuarios:listar_subusuarios')


@login_required
@require_POST
def toggle_ativo_subusuario(request, subusuario_id):
    """Ativa/desativa um subusuário via AJAX"""
    subusuario = get_object_or_404(
        SubUsuario, 
        id=subusuario_id, 
        usuario_principal=request.user
    )
    
    subusuario.ativo = not subusuario.ativo
    subusuario.save()
    
    return JsonResponse({
        'success': True,
        'ativo': subusuario.ativo,
        'message': f'Subusuário {"ativado" if subusuario.ativo else "desativado"} com sucesso!'
    })


# ===== VIEWS PARA GESTÃO DE MÓDULOS DE ACESSO =====

@login_required
def listar_modulos(request):
    """Lista módulos de acesso (apenas para administradores)"""
    modulos = ModuloAcesso.objects.all().order_by('ordem', 'nome')
    
    context = {
        'modulos': modulos,
    }
    return render(request, 'subusuarios/modulos_list.html', context)


@login_required
def cadastrar_modulo(request):
    """Cadastra um novo módulo de acesso"""
    if request.method == 'POST':
        form = ModuloAcessoForm(request.POST)
        if form.is_valid():
            modulo = form.save()
            messages.success(request, f'Módulo "{modulo.nome}" cadastrado com sucesso!')
            return redirect('subusuarios:listar_modulos')
    else:
        form = ModuloAcessoForm()
    
    context = {
        'form': form,
        'titulo': 'Cadastrar Módulo',
        'botao_texto': 'Cadastrar',
    }
    return render(request, 'subusuarios/modulos_form.html', context)


# ===== VIEWS PARA GESTÃO DE PERFIS DE ACESSO =====

@login_required
def listar_perfis(request):
    """Lista perfis de acesso"""
    perfis = PerfilAcesso.objects.all().annotate(
        total_modulos=Count('modulos')
    )
    
    context = {
        'perfis': perfis,
    }
    return render(request, 'subusuarios/perfis_list.html', context)


@login_required
def cadastrar_perfil(request):
    """Cadastra um novo perfil de acesso"""
    if request.method == 'POST':
        form = PerfilAcessoForm(request.POST)
        if form.is_valid():
            perfil = form.save()
            messages.success(request, f'Perfil "{perfil.nome}" cadastrado com sucesso!')
            return redirect('subusuarios:listar_perfis')
    else:
        form = PerfilAcessoForm()
    
    context = {
        'form': form,
        'titulo': 'Cadastrar Perfil de Acesso',
        'botao_texto': 'Cadastrar',
    }
    return render(request, 'subusuarios/perfis_form.html', context)


@login_required
def editar_perfil(request, perfil_id):
    """Edita um perfil de acesso"""
    perfil = get_object_or_404(PerfilAcesso, id=perfil_id)
    
    if request.method == 'POST':
        form = PerfilAcessoForm(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            messages.success(request, f'Perfil "{perfil.nome}" atualizado com sucesso!')
            return redirect('subusuarios:listar_perfis')
    else:
        form = PerfilAcessoForm(instance=perfil)
    
    context = {
        'form': form,
        'perfil': perfil,
        'titulo': 'Editar Perfil de Acesso',
        'botao_texto': 'Atualizar',
    }
    return render(request, 'subusuarios/perfis_form.html', context)


# ===== APIS AJAX =====

@login_required
def api_perfil_modulos(request, perfil_id):
    """Retorna módulos de um perfil via AJAX"""
    try:
        perfil = PerfilAcesso.objects.get(id=perfil_id, ativo=True)
        modulos = list(perfil.modulos.values_list('id', flat=True))
        return JsonResponse({
            'success': True,
            'modulos': modulos
        })
    except PerfilAcesso.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Perfil não encontrado'
        })


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
        return ModuloAcesso.objects.filter(ativo=True).order_by('ordem', 'nome')



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


@require_POST
@login_required
def toggle_ativo_subusuario(request, subusuario_id):
    """Ativa/desativa um subusuário via AJAX"""
    subusuario = get_object_or_404(
        SubUsuario, 
        id=subusuario_id, 
        usuario_principal=request.user
    )
    
    subusuario.ativo = not subusuario.ativo
    subusuario.save()
    
    return JsonResponse({
        'success': True,
        'ativo': subusuario.ativo,
        'message': f'Subusuário {"ativado" if subusuario.ativo else "desativado"} com sucesso!'
    })


# ===== FLUXO DE CONVITE POR E-MAIL =====

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.urls import reverse
import uuid


@login_required
def enviar_convite(request, subusuario_id):
    """Envia convite por e-mail para subusuário definir senha"""
    subusuario = get_object_or_404(
        SubUsuario, 
        id=subusuario_id, 
        usuario_principal=request.user
    )
    
    # Gerar novo token de convite
    subusuario.gerar_novo_token_convite()
    subusuario.save()
    
    # Preparar dados do e-mail
    link_convite = request.build_absolute_uri(
        reverse('configuracoes:subusuarios:definir_senha', args=[subusuario.token_convite])
    )
    
    context_email = {
        'subusuario': subusuario,
        'usuario_principal': request.user,
        'link_convite': link_convite,
        'empresa': getattr(request.user, 'empresa', 'XBPNEUS'),
    }
    
    # Renderizar template do e-mail
    html_message = render_to_string('subusuarios/emails/convite.html', context_email)
    plain_message = strip_tags(html_message)
    
    try:
        # Enviar e-mail
        send_mail(
            subject=f'Convite para acessar o sistema XBPNEUS - {context_email["empresa"]}',
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[subusuario.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        # Marcar convite como enviado
        subusuario.convite_enviado = True
        subusuario.save()
        
        messages.success(
            request, 
            f'Convite enviado com sucesso para {subusuario.email}!'
        )
        
    except Exception as e:
        messages.error(
            request, 
            f'Erro ao enviar convite: {str(e)}'
        )
    
    return redirect('configuracoes:subusuarios:listar_subusuarios')


def definir_senha(request, token):
    """Página para subusuário definir sua senha usando token do convite"""
    try:
        subusuario = SubUsuario.objects.get(token_convite=token)
    except SubUsuario.DoesNotExist:
        messages.error(request, 'Token de convite inválido ou expirado.')
        return redirect('login')
    
    if subusuario.senha_definida:
        messages.info(request, 'Senha já foi definida para este usuário.')
        return redirect('login')
    
    if request.method == 'POST':
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')
        
        if not senha or not confirmar_senha:
            messages.error(request, 'Todos os campos são obrigatórios.')
        elif senha != confirmar_senha:
            messages.error(request, 'As senhas não coincidem.')
        elif len(senha) < 8:
            messages.error(request, 'A senha deve ter pelo menos 8 caracteres.')
        else:
            # Definir senha
            subusuario.set_senha(senha)
            subusuario.convite_enviado = True
            subusuario.save()
            
            messages.success(
                request, 
                'Senha definida com sucesso! Você já pode fazer login no sistema.'
            )
            return redirect('login')
    
    context = {
        'subusuario': subusuario,
        'token': token,
    }
    return render(request, 'subusuarios/definir_senha.html', context)


@login_required
def reenviar_convite(request, subusuario_id):
    """Reenvia convite para subusuário"""
    return enviar_convite(request, subusuario_id)


# ===== AJAX ENDPOINTS =====

@login_required
def ajax_modulos_perfil(request, perfil_id):
    """Retorna módulos de um perfil de acesso via AJAX"""
    try:
        perfil = PerfilAcesso.objects.get(id=perfil_id, ativo=True)
        modulos = list(perfil.modulos.values_list('id', flat=True))
        return JsonResponse({
            'success': True,
            'modulos': modulos
        })
    except PerfilAcesso.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Perfil não encontrado'
        })


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
    
    return JsonResponse({
        'disponivel': disponivel,
        'message': 'Login disponível' if disponivel else 'Login já está em uso'
    })


@login_required
def ajax_validar_email(request):
    """Valida se e-mail já existe via AJAX"""
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
    
    return JsonResponse({
        'disponivel': disponivel,
        'message': 'E-mail disponível' if disponivel else 'E-mail já está em uso'
    })

