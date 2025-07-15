from django import forms
from .models_estoque import PneuEstoque, VinculacaoPneu, HistoricoMovimentacao
from .models import Veiculo


class PneuEstoqueForm(forms.ModelForm):
    """Formulário para entrada de pneus no estoque"""
    
    class Meta:
        model = PneuEstoque
        fields = [
            'numero_nf', 'fornecedor', 'data_entrada',
            'marca', 'modelo', 'medida', 'tipo',
            'numero_serie', 'dot', 'valor_unitario',
            'observacoes'
        ]
        widgets = {
            'numero_nf': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: NF-123456'
            }),
            'fornecedor': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: XBPNEUS Distribuidora'
            }),
            'data_entrada': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'marca': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Michelin, Bridgestone'
            }),
            'modelo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: XZA3, R249'
            }),
            'medida': forms.Select(attrs={
                'class': 'form-select'
            }),
            'tipo': forms.Select(attrs={
                'class': 'form-select'
            }),
            'numero_serie': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: SN123456789'
            }),
            'dot': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 2024',
                'maxlength': 10
            }),
            'valor_unitario': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 1500.00',
                'step': '0.01'
            }),
            'observacoes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observações sobre o pneu...'
            }),
        }


class VinculacaoPneuForm(forms.ModelForm):
    """Formulário para vincular pneu do estoque ao veículo"""
    
    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop('usuario', None)
        super().__init__(*args, **kwargs)
        
        if self.usuario:
            # Filtrar apenas veículos do usuário
            self.fields['veiculo'].queryset = Veiculo.objects.filter(usuario=self.usuario)
            
            # Filtrar apenas pneus disponíveis do usuário
            self.fields['pneu_estoque'].queryset = PneuEstoque.objects.filter(
                usuario=self.usuario,
                status='disponivel'
            )
    
    class Meta:
        model = VinculacaoPneu
        fields = [
            'pneu_estoque', 'veiculo', 'posicao',
            'data_montagem', 'km_montagem',
            'pressao_atual', 'observacoes'
        ]
        widgets = {
            'pneu_estoque': forms.Select(attrs={
                'class': 'form-select'
            }),
            'veiculo': forms.Select(attrs={
                'class': 'form-select'
            }),
            'posicao': forms.Select(attrs={
                'class': 'form-select'
            }),
            'data_montagem': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'km_montagem': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 150000'
            }),
            'pressao_atual': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 120.0',
                'step': '0.1'
            }),
            'observacoes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observações sobre a montagem...'
            }),
        }


class RemocaoPneuForm(forms.ModelForm):
    """Formulário para remoção de pneu do veículo"""
    
    class Meta:
        model = VinculacaoPneu
        fields = [
            'data_remocao', 'km_remocao', 'motivo_remocao'
        ]
        widgets = {
            'data_remocao': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'km_remocao': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 180000'
            }),
            'motivo_remocao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Motivo da remoção (desgaste, furo, troca, etc.)'
            }),
        }


class AtualizacaoSulcoForm(forms.ModelForm):
    """Formulário para atualização de medidas de sulco"""
    
    class Meta:
        model = VinculacaoPneu
        fields = [
            'sulco_externo', 'sulco_central', 'sulco_interno',
            'pressao_atual', 'observacoes'
        ]
        widgets = {
            'sulco_externo': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 8.5',
                'step': '0.1'
            }),
            'sulco_central': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 8.0',
                'step': '0.1'
            }),
            'sulco_interno': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 8.2',
                'step': '0.1'
            }),
            'pressao_atual': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 120.0',
                'step': '0.1'
            }),
            'observacoes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observações sobre o estado atual...'
            }),
        }


class HistoricoMovimentacaoForm(forms.ModelForm):
    """Formulário para registro de movimentação"""
    
    class Meta:
        model = HistoricoMovimentacao
        fields = [
            'tipo_movimento', 'veiculo', 'km_veiculo',
            'custo', 'descricao'
        ]
        widgets = {
            'tipo_movimento': forms.Select(attrs={
                'class': 'form-select'
            }),
            'veiculo': forms.Select(attrs={
                'class': 'form-select'
            }),
            'km_veiculo': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 150000'
            }),
            'custo': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 250.00',
                'step': '0.01'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descrição detalhada da movimentação...'
            }),
        }


class FiltroEstoqueForm(forms.Form):
    """Formulário para filtros de relatório de estoque"""
    
    STATUS_CHOICES = [
        ('', 'Todos os Status'),
        ('disponivel', 'Disponível'),
        ('em_uso', 'Em uso'),
        ('reformado', 'Reformado'),
        ('descartado', 'Descartado'),
    ]
    
    TIPO_CHOICES = [
        ('', 'Todos os Tipos'),
        ('novo', 'Novo'),
        ('usado', 'Usado'),
        ('reformado', 'Reformado'),
    ]
    
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    tipo = forms.ChoiceField(
        choices=TIPO_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    marca = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Filtrar por marca...'
        })
    )
    
    medida = forms.ChoiceField(
        choices=[('', 'Todas as Medidas')] + PneuEstoque.MEDIDAS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    data_entrada_inicio = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    data_entrada_fim = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )

