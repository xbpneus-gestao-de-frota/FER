from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Sum, Avg
from .models import Veiculo, Pneu, HistoricoPneu
from .forms import VeiculoForm, PneuForm, HistoricoPneuForm

@login_required
def dashboard_frota(request):
    """Dashboard principal da gestão de frota"""
    veiculos = Veiculo.objects.filter(usuario=request.user)
    total_veiculos = veiculos.count()
    total_pneus = Pneu.objects.filter(veiculo__usuario=request.user).count()
    
    # Estatísticas
    custo_total_pneus = Pneu.objects.filter(veiculo__usuario=request.user).aggregate(
        total=Sum('custo')
    )['total'] or 0
    
    # Pneus que precisam de atenção (profundidade baixa)
    pneus_atencao = Pneu.objects.filter(
        veiculo__usuario=request.user,
        profundidade_sulco__lt=3.0
    ).count()
    
    context = {
        'total_veiculos': total_veiculos,
        'total_pneus': total_pneus,
        'custo_total_pneus': custo_total_pneus,
        'pneus_atencao': pneus_atencao,
        'veiculos': veiculos[:5],  # Últimos 5 veículos
    }
    return render(request, 'frota/dashboard.html', context)

@login_required
def listar_veiculos(request):
    """Lista todos os veículos do usuário"""
    veiculos = Veiculo.objects.filter(usuario=request.user)
    return render(request, 'frota/veiculos_lista.html', {'veiculos': veiculos})

@login_required
def cadastrar_veiculo(request):
    """Cadastra um novo veículo"""
    if request.method == 'POST':
        form = VeiculoForm(request.POST)
        if form.is_valid():
            veiculo = form.save(commit=False)
            veiculo.usuario = request.user
            veiculo.save()
            messages.success(request, 'Veículo cadastrado com sucesso!')
            return redirect('frota:listar_frota')
    else:
        form = VeiculoForm()
    
    return render(request, 'frota/veiculo_form.html', {'form': form, 'titulo': 'Cadastrar Veículo'})

@login_required
def editar_veiculo(request, veiculo_id):
    """Edita um veículo existente"""
    veiculo = get_object_or_404(Veiculo, id=veiculo_id, usuario=request.user)
    
    if request.method == 'POST':
        form = VeiculoForm(request.POST, instance=veiculo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Veículo atualizado com sucesso!')
            return redirect('frota:listar_frota')
    else:
        form = VeiculoForm(instance=veiculo)
    
    return render(request, 'frota/veiculo_form.html', {
        'form': form, 
        'titulo': 'Editar Veículo',
        'veiculo': veiculo
    })

@login_required
def detalhes_veiculo(request, veiculo_id):
    """Mostra detalhes do veículo e seus pneus"""
    veiculo = get_object_or_404(Veiculo, id=veiculo_id, usuario=request.user)
    pneus = veiculo.pneus.all()
    
    context = {
        'veiculo': veiculo,
        'pneus': pneus,
    }
    return render(request, 'frota/veiculo_detalhes.html', context)

@login_required
def listar_pneus(request):
    """Lista todos os pneus do usuário"""
    pneus = Pneu.objects.filter(veiculo__usuario=request.user)
    return render(request, 'frota/pneus_lista.html', {'pneus': pneus})

@login_required
def cadastrar_pneu(request, veiculo_id=None):
    """Cadastra um novo pneu"""
    veiculo = None
    if veiculo_id:
        veiculo = get_object_or_404(Veiculo, id=veiculo_id, usuario=request.user)
    
    if request.method == 'POST':
        form = PneuForm(request.POST, usuario=request.user)
        if form.is_valid():
            pneu = form.save()
            messages.success(request, 'Pneu cadastrado com sucesso!')
            return redirect('frota:detalhes_frota', veiculo_id=pneu.veiculo.id)
    else:
        form = PneuForm(usuario=request.user, initial={'veiculo': veiculo} if veiculo else None)
    
    return render(request, 'frota/pneu_form.html', {
        'form': form, 
        'titulo': 'Cadastrar Pneu',
        'veiculo': veiculo
    })

@login_required
def editar_pneu(request, pneu_id):
    """Edita um pneu existente"""
    pneu = get_object_or_404(Pneu, id=pneu_id, veiculo__usuario=request.user)
    
    if request.method == 'POST':
        form = PneuForm(request.POST, instance=pneu, usuario=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pneu atualizado com sucesso!')
            return redirect('frota:detalhes_frota', veiculo_id=pneu.veiculo.id)
    else:
        form = PneuForm(instance=pneu, usuario=request.user)
    
    return render(request, 'frota/pneu_form.html', {
        'form': form, 
        'titulo': 'Editar Pneu',
        'pneu': pneu
    })

@login_required
def relatorios(request):
    """Página de relatórios"""
    veiculos = Veiculo.objects.filter(usuario=request.user)
    
    # Relatório por veículo
    relatorio_veiculos = []
    for veiculo in veiculos:
        pneus = veiculo.pneus.all()
        custo_total = pneus.aggregate(total=Sum('custo'))['total'] or 0
        profundidade_media = pneus.aggregate(media=Avg('profundidade_sulco'))['media'] or 0
        
        relatorio_veiculos.append({
            'veiculo': veiculo,
            'total_pneus': pneus.count(),
            'custo_total': custo_total,
            'profundidade_media': round(profundidade_media, 1),
        })
    
    # Pneus por medida
    pneus_por_medida = Pneu.objects.filter(veiculo__usuario=request.user).values('medida').annotate(
        quantidade=Count('id'),
        custo_total=Sum('custo')
    ).order_by('-quantidade')
    
    context = {
        'relatorio_veiculos': relatorio_veiculos,
        'pneus_por_medida': pneus_por_medida,
    }
    return render(request, 'frota/relatorios.html', context)

