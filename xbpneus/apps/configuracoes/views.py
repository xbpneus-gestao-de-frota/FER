from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .models import ConfiguracaoEmpresa, PreferenciaSistema
from .forms import ConfiguracaoEmpresaForm, PreferenciaSistemaForm


@login_required
def dashboard_configuracoes(request):
    """Dashboard principal das configurações"""
    try:
        config_empresa = ConfiguracaoEmpresa.objects.get(usuario=request.user)
    except ConfiguracaoEmpresa.DoesNotExist:
        config_empresa = None
    
    try:
        preferencias = PreferenciaSistema.objects.get(usuario=request.user)
    except PreferenciaSistema.DoesNotExist:
        preferencias = None
    
    context = {
        'config_empresa': config_empresa,
        'preferencias': preferencias,
    }
    return render(request, 'configuracoes/dashboard.html', context)


@login_required
def configuracao_empresa(request):
    """Configurações da empresa"""
    try:
        config = ConfiguracaoEmpresa.objects.get(usuario=request.user)
    except ConfiguracaoEmpresa.DoesNotExist:
        config = None
    
    if request.method == 'POST':
        form = ConfiguracaoEmpresaForm(request.POST, instance=config)
        if form.is_valid():
            config = form.save(commit=False)
            config.usuario = request.user
            config.save()
            messages.success(request, 'Configurações da empresa atualizadas com sucesso!')
            return redirect('configuracoes:empresa')
    else:
        form = ConfiguracaoEmpresaForm(instance=config)
    
    context = {
        'form': form,
        'config': config,
    }
    return render(request, 'configuracoes/empresa.html', context)


@login_required
def preferencias_usuario(request):
    """Preferências do usuário"""
    try:
        preferencias = PreferenciaSistema.objects.get(usuario=request.user)
    except PreferenciaSistema.DoesNotExist:
        preferencias = None
    
    if request.method == 'POST':
        form = PreferenciaSistemaForm(request.POST, instance=preferencias)
        if form.is_valid():
            pref = form.save(commit=False)
            pref.usuario = request.user
            pref.save()
            messages.success(request, 'Preferências atualizadas com sucesso!')
            return redirect('configuracoes:preferencias')
    else:
        form = PreferenciaSistemaForm(instance=preferencias)
    
    context = {
        'form': form,
        'preferencias': preferencias,
    }
    return render(request, 'configuracoes/preferencias.html', context)

