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



# Views AJAX para combos dependentes
from django.http import JsonResponse
from .models_auxiliares import MarcaVeiculo, ModeloVeiculo, CorVeiculo
from .forms import VeiculoAutomatizadoForm

@login_required
def cadastrar_veiculo_automatizado(request):
    """Cadastra um novo veículo usando o formulário automatizado"""
    if request.method == 'POST':
        form = VeiculoAutomatizadoForm(request.POST)
        if form.is_valid():
            veiculo = form.save(commit=False)
            veiculo.usuario = request.user
            veiculo.save()
            messages.success(request, 'Veículo cadastrado com sucesso!')
            return redirect('frota:listar_frota')
    else:
        form = VeiculoAutomatizadoForm()
    
    return render(request, 'frota/veiculo_automatizado_form.html', {'form': form})

@login_required
def editar_veiculo_automatizado(request, veiculo_id):
    """Edita um veículo usando o formulário automatizado"""
    veiculo = get_object_or_404(Veiculo, id=veiculo_id, usuario=request.user)
    
    if request.method == 'POST':
        form = VeiculoAutomatizadoForm(request.POST, instance=veiculo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Veículo atualizado com sucesso!')
            return redirect('frota:listar_frota')
    else:
        form = VeiculoAutomatizadoForm(instance=veiculo)
    
    return render(request, 'frota/veiculo_automatizado_form.html', {
        'form': form, 
        'veiculo': veiculo,
        'editando': True
    })

def ajax_carregar_modelos(request):
    """AJAX: Carrega modelos baseados na marca selecionada"""
    marca_id = request.GET.get('marca_id')
    
    if not marca_id:
        return JsonResponse({'modelos': []})
    
    try:
        marca = MarcaVeiculo.objects.get(id=marca_id, ativo=True)
        modelos = ModeloVeiculo.objects.filter(
            marca=marca, 
            ativo=True
        ).order_by('nome')
        
        modelos_data = []
        for modelo in modelos:
            modelos_data.append({
                'id': modelo.id,
                'nome': modelo.nome_completo,
                'quantidade_eixos': modelo.quantidade_eixos,
                'tipo_veiculo': modelo.tipo_veiculo.get_nome_display(),
                'ano_inicio': modelo.ano_inicio,
                'ano_fim': modelo.ano_fim
            })
        
        return JsonResponse({'modelos': modelos_data})
    
    except MarcaVeiculo.DoesNotExist:
        return JsonResponse({'modelos': []})

def ajax_carregar_anos(request):
    """AJAX: Carrega anos disponíveis baseados no modelo selecionado"""
    modelo_id = request.GET.get('modelo_id')
    
    if not modelo_id:
        return JsonResponse({'anos': []})
    
    try:
        modelo = ModeloVeiculo.objects.get(id=modelo_id, ativo=True)
        anos = modelo.anos_disponiveis
        
        anos_data = [{'value': ano, 'text': str(ano)} for ano in anos]
        
        return JsonResponse({
            'anos': anos_data,
            'modelo_info': {
                'nome': modelo.nome_completo,
                'quantidade_eixos': modelo.quantidade_eixos,
                'tipo_veiculo': modelo.tipo_veiculo.get_nome_display(),
                'capacidade_carga': float(modelo.capacidade_carga) if modelo.capacidade_carga else None,
                'motor_padrao': modelo.motor_padrao,
                'combustivel': modelo.combustivel
            }
        })
    
    except ModeloVeiculo.DoesNotExist:
        return JsonResponse({'anos': []})

def ajax_info_modelo(request):
    """AJAX: Retorna informações detalhadas do modelo"""
    modelo_id = request.GET.get('modelo_id')
    
    if not modelo_id:
        return JsonResponse({'info': {}})
    
    try:
        modelo = ModeloVeiculo.objects.get(id=modelo_id, ativo=True)
        
        info = {
            'marca': modelo.marca.nome,
            'nome': modelo.nome,
            'nome_completo': modelo.nome_completo,
            'tipo_veiculo': modelo.tipo_veiculo.get_nome_display(),
            'quantidade_eixos': modelo.quantidade_eixos,
            'capacidade_carga': float(modelo.capacidade_carga) if modelo.capacidade_carga else None,
            'motor_padrao': modelo.motor_padrao,
            'combustivel': modelo.combustivel,
            'ano_inicio': modelo.ano_inicio,
            'ano_fim': modelo.ano_fim,
            'anos_disponiveis': modelo.anos_disponiveis
        }
        
        # Adicionar especificações técnicas se disponíveis
        if hasattr(modelo, 'especificacao'):
            spec = modelo.especificacao
            info['especificacoes'] = {
                'potencia_motor': spec.potencia_motor,
                'torque_motor': spec.torque_motor,
                'transmissao': spec.transmissao,
                'freios': spec.freios,
                'suspensao_dianteira': spec.suspensao_dianteira,
                'suspensao_traseira': spec.suspensao_traseira,
                'tanque_combustivel': spec.tanque_combustivel,
                'pneus_dianteiros': spec.pneus_dianteiros,
                'pneus_traseiros': spec.pneus_traseiros
            }
        
        return JsonResponse({'info': info})
    
    except ModeloVeiculo.DoesNotExist:
        return JsonResponse({'info': {}})

def ajax_validar_placa(request):
    """AJAX: Valida se a placa já existe no sistema"""
    placa = request.GET.get('placa', '').upper().strip()
    veiculo_id = request.GET.get('veiculo_id')  # Para edição
    
    if not placa:
        return JsonResponse({'valida': True, 'mensagem': ''})
    
    # Verificar se a placa já existe
    query = Veiculo.objects.filter(placa=placa)
    
    # Se estamos editando, excluir o veículo atual da verificação
    if veiculo_id:
        query = query.exclude(id=veiculo_id)
    
    if query.exists():
        return JsonResponse({
            'valida': False, 
            'mensagem': 'Esta placa já está cadastrada no sistema.'
        })
    
    return JsonResponse({'valida': True, 'mensagem': 'Placa disponível.'})

