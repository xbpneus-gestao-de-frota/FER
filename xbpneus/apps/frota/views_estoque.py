from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Sum, Q
from django.http import JsonResponse
from .models_estoque import PneuEstoque, VinculacaoPneu, HistoricoMovimentacao
from .forms_estoque import (
    PneuEstoqueForm, VinculacaoPneuForm, RemocaoPneuForm,
    AtualizacaoSulcoForm, HistoricoMovimentacaoForm, FiltroEstoqueForm
)
from .models import Veiculo


@login_required
def dashboard_estoque(request):
    """Dashboard do estoque de pneus"""
    pneus_estoque = PneuEstoque.objects.filter(usuario=request.user)
    
    # Estatísticas
    total_pneus = pneus_estoque.count()
    pneus_disponiveis = pneus_estoque.filter(status='disponivel').count()
    pneus_em_uso = pneus_estoque.filter(status='em_uso').count()
    pneus_reformados = pneus_estoque.filter(status='reformado').count()
    pneus_descartados = pneus_estoque.filter(status='descartado').count()
    
    # Valor total do estoque
    valor_total = pneus_estoque.aggregate(total=Sum('valor_unitario'))['total'] or 0
    valor_disponivel = pneus_estoque.filter(status='disponivel').aggregate(
        total=Sum('valor_unitario')
    )['total'] or 0
    
    # Pneus por marca
    pneus_por_marca = pneus_estoque.values('marca').annotate(
        total=Count('id')
    ).order_by('-total')[:5]
    
    # Últimas movimentações
    ultimas_movimentacoes = HistoricoMovimentacao.objects.filter(
        pneu_estoque__usuario=request.user
    )[:10]
    
    context = {
        'total_pneus': total_pneus,
        'pneus_disponiveis': pneus_disponiveis,
        'pneus_em_uso': pneus_em_uso,
        'pneus_reformados': pneus_reformados,
        'pneus_descartados': pneus_descartados,
        'valor_total': valor_total,
        'valor_disponivel': valor_disponivel,
        'pneus_por_marca': pneus_por_marca,
        'ultimas_movimentacoes': ultimas_movimentacoes,
    }
    return render(request, 'frota/estoque/dashboard.html', context)


@login_required
def listar_estoque(request):
    """Lista pneus do estoque com filtros"""
    pneus = PneuEstoque.objects.filter(usuario=request.user)
    form = FiltroEstoqueForm(request.GET)
    
    if form.is_valid():
        if form.cleaned_data['status']:
            pneus = pneus.filter(status=form.cleaned_data['status'])
        if form.cleaned_data['tipo']:
            pneus = pneus.filter(tipo=form.cleaned_data['tipo'])
        if form.cleaned_data['marca']:
            pneus = pneus.filter(marca__icontains=form.cleaned_data['marca'])
        if form.cleaned_data['medida']:
            pneus = pneus.filter(medida=form.cleaned_data['medida'])
        if form.cleaned_data['data_entrada_inicio']:
            pneus = pneus.filter(data_entrada__gte=form.cleaned_data['data_entrada_inicio'])
        if form.cleaned_data['data_entrada_fim']:
            pneus = pneus.filter(data_entrada__lte=form.cleaned_data['data_entrada_fim'])
    
    context = {
        'pneus': pneus,
        'form': form,
    }
    return render(request, 'frota/estoque/lista.html', context)


@login_required
def cadastrar_pneu_estoque(request):
    """Cadastra pneu no estoque"""
    if request.method == 'POST':
        form = PneuEstoqueForm(request.POST)
        if form.is_valid():
            pneu = form.save(commit=False)
            pneu.usuario = request.user
            pneu.save()
            
            # Registrar histórico
            HistoricoMovimentacao.objects.create(
                pneu_estoque=pneu,
                tipo_movimento='entrada',
                descricao=f'Entrada no estoque via NF {pneu.numero_nf}',
                usuario=request.user
            )
            
            messages.success(request, 'Pneu cadastrado no estoque com sucesso!')
            return redirect('frota:listar_estoque')
    else:
        form = PneuEstoqueForm()
    
    return render(request, 'frota/estoque/cadastrar.html', {
        'form': form,
        'titulo': 'Cadastrar Pneu no Estoque'
    })


@login_required
def vincular_pneu(request):
    """Vincula pneu do estoque ao veículo"""
    if request.method == 'POST':
        form = VinculacaoPneuForm(request.POST, usuario=request.user)
        if form.is_valid():
            vinculacao = form.save()
            
            # Registrar histórico
            HistoricoMovimentacao.objects.create(
                pneu_estoque=vinculacao.pneu_estoque,
                tipo_movimento='montagem',
                veiculo=vinculacao.veiculo,
                km_veiculo=vinculacao.km_montagem,
                descricao=f'Montagem no veículo {vinculacao.veiculo.placa} - {vinculacao.get_posicao_display()}',
                usuario=request.user
            )
            
            messages.success(request, 'Pneu vinculado ao veículo com sucesso!')
            return redirect('frota:detalhes_veiculo', veiculo_id=vinculacao.veiculo.id)
    else:
        form = VinculacaoPneuForm(usuario=request.user)
    
    return render(request, 'frota/estoque/vincular.html', {
        'form': form,
        'titulo': 'Vincular Pneu ao Veículo'
    })


@login_required
def remover_pneu(request, vinculacao_id):
    """Remove pneu do veículo"""
    vinculacao = get_object_or_404(
        VinculacaoPneu,
        id=vinculacao_id,
        veiculo__usuario=request.user,
        ativo=True
    )
    
    if request.method == 'POST':
        form = RemocaoPneuForm(request.POST, instance=vinculacao)
        if form.is_valid():
            vinculacao = form.save(commit=False)
            vinculacao.ativo = False
            vinculacao.save()
            
            # Registrar histórico
            HistoricoMovimentacao.objects.create(
                pneu_estoque=vinculacao.pneu_estoque,
                tipo_movimento='remocao',
                veiculo=vinculacao.veiculo,
                km_veiculo=vinculacao.km_remocao,
                descricao=f'Remoção do veículo {vinculacao.veiculo.placa} - {vinculacao.motivo_remocao}',
                usuario=request.user
            )
            
            messages.success(request, 'Pneu removido do veículo com sucesso!')
            return redirect('frota:detalhes_veiculo', veiculo_id=vinculacao.veiculo.id)
    else:
        form = RemocaoPneuForm(instance=vinculacao)
    
    return render(request, 'frota/estoque/remover.html', {
        'form': form,
        'vinculacao': vinculacao,
        'titulo': 'Remover Pneu do Veículo'
    })


@login_required
def atualizar_sulco(request, vinculacao_id):
    """Atualiza medidas de sulco do pneu"""
    vinculacao = get_object_or_404(
        VinculacaoPneu,
        id=vinculacao_id,
        veiculo__usuario=request.user,
        ativo=True
    )
    
    if request.method == 'POST':
        form = AtualizacaoSulcoForm(request.POST, instance=vinculacao)
        if form.is_valid():
            form.save()
            
            # Registrar histórico
            HistoricoMovimentacao.objects.create(
                pneu_estoque=vinculacao.pneu_estoque,
                tipo_movimento='manutencao',
                veiculo=vinculacao.veiculo,
                descricao=f'Atualização de medidas - Sulcos: {vinculacao.sulco_externo}/{vinculacao.sulco_central}/{vinculacao.sulco_interno}mm',
                usuario=request.user
            )
            
            messages.success(request, 'Medidas atualizadas com sucesso!')
            return redirect('frota:detalhes_veiculo', veiculo_id=vinculacao.veiculo.id)
    else:
        form = AtualizacaoSulcoForm(instance=vinculacao)
    
    return render(request, 'frota/estoque/atualizar_sulco.html', {
        'form': form,
        'vinculacao': vinculacao,
        'titulo': 'Atualizar Medidas do Pneu'
    })


@login_required
def detalhes_pneu_estoque(request, pneu_id):
    """Detalhes do pneu no estoque"""
    pneu = get_object_or_404(PneuEstoque, id=pneu_id, usuario=request.user)
    historico = pneu.historico.all()
    vinculacoes = pneu.vinculacoes.all()
    
    context = {
        'pneu': pneu,
        'historico': historico,
        'vinculacoes': vinculacoes,
    }
    return render(request, 'frota/estoque/detalhes.html', context)


@login_required
def relatorio_estoque(request):
    """Relatório completo do estoque"""
    pneus = PneuEstoque.objects.filter(usuario=request.user)
    
    # Estatísticas por status
    stats_status = pneus.values('status').annotate(
        quantidade=Count('id'),
        valor_total=Sum('valor_unitario')
    )
    
    # Estatísticas por marca
    stats_marca = pneus.values('marca').annotate(
        quantidade=Count('id'),
        valor_total=Sum('valor_unitario')
    ).order_by('-quantidade')
    
    # Estatísticas por medida
    stats_medida = pneus.values('medida').annotate(
        quantidade=Count('id'),
        valor_total=Sum('valor_unitario')
    ).order_by('-quantidade')
    
    # Pneus com baixo sulco (em uso)
    pneus_atencao = VinculacaoPneu.objects.filter(
        veiculo__usuario=request.user,
        ativo=True
    ).filter(
        Q(sulco_externo__lt=2.0) |
        Q(sulco_central__lt=2.0) |
        Q(sulco_interno__lt=2.0)
    )
    
    context = {
        'stats_status': stats_status,
        'stats_marca': stats_marca,
        'stats_medida': stats_medida,
        'pneus_atencao': pneus_atencao,
        'total_pneus': pneus.count(),
        'valor_total_estoque': pneus.aggregate(total=Sum('valor_unitario'))['total'] or 0,
    }
    return render(request, 'frota/estoque/relatorio.html', context)


@login_required
def api_pneus_disponiveis(request):
    """API para buscar pneus disponíveis (AJAX)"""
    medida = request.GET.get('medida', '')
    marca = request.GET.get('marca', '')
    
    pneus = PneuEstoque.objects.filter(
        usuario=request.user,
        status='disponivel'
    )
    
    if medida:
        pneus = pneus.filter(medida=medida)
    if marca:
        pneus = pneus.filter(marca__icontains=marca)
    
    data = [{
        'id': pneu.id,
        'text': f"{pneu.marca} {pneu.modelo} - {pneu.medida} - {pneu.numero_serie}",
        'marca': pneu.marca,
        'modelo': pneu.modelo,
        'medida': pneu.medida,
        'numero_serie': pneu.numero_serie,
        'valor': str(pneu.valor_unitario)
    } for pneu in pneus[:20]]
    
    return JsonResponse({'results': data})

