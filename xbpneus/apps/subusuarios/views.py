from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import SubUsuario
from .forms import SubUsuarioForm

@login_required
def listar_subusuarios(request):
    """Lista todos os subusuários do usuário principal"""
    subusuarios = SubUsuario.objects.filter(usuario_principal=request.user)
    
    context = {
        'subusuarios': subusuarios,
        'total_subusuarios': subusuarios.count(),
        'subusuarios_ativos': subusuarios.filter(ativo=True).count(),
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
            return redirect('subusuarios:listar_subusuarios')
    else:
        form = SubUsuarioForm(usuario_principal=request.user)
    
    context = {
        'form': form,
        'titulo': 'Cadastrar Subusuário',
        'botao_texto': 'Cadastrar',
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
            subusuario = form.save()
            messages.success(
                request, 
                f'Subusuário "{subusuario.nome}" atualizado com sucesso!'
            )
            return redirect('subusuarios:listar_subusuarios')
    else:
        form = SubUsuarioForm(instance=subusuario, usuario_principal=request.user)
    
    context = {
        'form': form,
        'titulo': 'Editar Subusuário',
        'botao_texto': 'Atualizar',
        'subusuario': subusuario,
    }
    return render(request, 'subusuarios/subusuarios_form.html', context)

@login_required
@require_POST
def excluir_subusuario(request, subusuario_id):
    """Exclui um subusuário"""
    subusuario = get_object_or_404(
        SubUsuario, 
        id=subusuario_id, 
        usuario_principal=request.user
    )
    
    nome_subusuario = subusuario.nome
    subusuario.delete()
    
    messages.success(
        request, 
        f'Subusuário "{nome_subusuario}" excluído com sucesso!'
    )
    
    # Se for uma requisição AJAX, retorna JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    
    return redirect('subusuarios:listar_subusuarios')

@login_required
def alternar_status_subusuario(request, subusuario_id):
    """Alterna o status ativo/inativo de um subusuário"""
    subusuario = get_object_or_404(
        SubUsuario, 
        id=subusuario_id, 
        usuario_principal=request.user
    )
    
    subusuario.ativo = not subusuario.ativo
    subusuario.save()
    
    status_texto = "ativado" if subusuario.ativo else "desativado"
    messages.success(
        request, 
        f'Subusuário "{subusuario.nome}" {status_texto} com sucesso!'
    )
    
    # Se for uma requisição AJAX, retorna JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True, 
            'ativo': subusuario.ativo,
            'status_texto': status_texto
        })
    
    return redirect('subusuarios:listar_subusuarios')

