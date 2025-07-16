from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q, Count
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from .models import SubUsuario, ModuloAcesso, PerfilAcesso
from .forms import SubUsuarioForm, PerfilAcessoForm, ModuloAcessoForm, FiltroSubUsuarioForm
from .utils import enviar_convite_subusuario, reenviar_convite_subusuario, validar_token_convite, definir_senha_subusuario


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
        'perfis_acesso': PerfilAcesso.objects.filter(ativo=True),
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




# ===== VIEWS PARA FLUXO DE CONVITE POR E-MAIL =====

def definir_senha_view(request, token):
    """View para subusuário definir senha via token de convite"""
    subusuario = validar_token_convite(token)
    
    if request.method == 'POST' and subusuario:
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')
        
        # Validações
        if not senha or not confirmar_senha:
            messages.error(request, 'Todos os campos são obrigatórios.')
        elif senha != confirmar_senha:
            messages.error(request, 'As senhas não coincidem.')
        else:
            try:
                # Validar força da senha
                validate_password(senha)
                
                # Definir senha
                if definir_senha_subusuario(subusuario, senha):
                    messages.success(
                        request, 
                        'Senha definida com sucesso! Você já pode acessar o sistema.'
                    )
                    # Redirecionar para login ou dashboard
                    return redirect('/')  # Ajustar conforme necessário
                else:
                    messages.error(request, 'Erro ao definir senha. Tente novamente.')
                    
            except ValidationError as e:
                for error in e.messages:
                    messages.error(request, error)
    
    context = {
        'subusuario': subusuario,
        'token': token,
    }
    return render(request, 'subusuarios/definir_senha.html', context)


@login_required
@require_POST
def reenviar_convite_view(request, subusuario_id):
    """Reenvia convite para subusuário"""
    subusuario = get_object_or_404(
        SubUsuario, 
        id=subusuario_id, 
        usuario_principal=request.user
    )
    
    if reenviar_convite_subusuario(subusuario, request):
        messages.success(
            request, 
            f'Convite reenviado com sucesso para {subusuario.email}!'
        )
    else:
        messages.error(
            request, 
            f'Erro ao reenviar convite para {subusuario.email}. Tente novamente.'
        )
    
    return redirect('configuracoes:subusuarios:listar_subusuarios')


@login_required
def status_convite_view(request, subusuario_id):
    """Retorna status do convite via AJAX"""
    subusuario = get_object_or_404(
        SubUsuario, 
        id=subusuario_id, 
        usuario_principal=request.user
    )
    
    return JsonResponse({
        'convite_enviado': subusuario.convite_enviado,
        'senha_definida': subusuario.senha_definida,
        'primeiro_acesso': subusuario.primeiro_acesso,
        'ativo': subusuario.ativo,
        'email': subusuario.email,
        'data_criacao': subusuario.data_criacao.isoformat(),
    })


@login_required
@require_POST
def enviar_convite_view(request, subusuario_id):
    """Envia convite para subusuário que ainda não recebeu"""
    subusuario = get_object_or_404(
        SubUsuario, 
        id=subusuario_id, 
        usuario_principal=request.user
    )
    
    if subusuario.senha_definida:
        messages.warning(
            request, 
            f'{subusuario.nome} já definiu sua senha e pode acessar o sistema.'
        )
    else:
        if enviar_convite_subusuario(subusuario, request):
            messages.success(
                request, 
                f'Convite enviado com sucesso para {subusuario.email}!'
            )
        else:
            messages.error(
                request, 
                f'Erro ao enviar convite para {subusuario.email}. Tente novamente.'
            )
    
    return redirect('configuracoes:subusuarios:listar_subusuarios')

