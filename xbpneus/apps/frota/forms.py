from django import forms
from .models import Veiculo, Pneu, HistoricoPneu
from .models_auxiliares import MarcaVeiculo, ModeloVeiculo, CorVeiculo, TipoVeiculo
from datetime import datetime

class VeiculoForm(forms.ModelForm):
    """Formulário para cadastro de veículos"""
    
    class Meta:
        model = Veiculo
        fields = ['placa', 'modelo', 'cor', 'km', 'ano']
        widgets = {
            'placa': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: ABC-1234',
                'maxlength': 8
            }),
            'modelo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Scania R450'
            }),
            'cor': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Branco'
            }),
            'km': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 150000'
            }),
            'ano': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 2020',
                'min': 1990,
                'max': 2030
            }),
        }
    
    def clean_placa(self):
        placa = self.cleaned_data['placa'].upper()
        # Validação básica de formato de placa
        if len(placa) < 7:
            raise forms.ValidationError('Placa deve ter pelo menos 7 caracteres.')
        return placa

class VeiculoAutomatizadoForm(forms.ModelForm):
    """Formulário automatizado para cadastro de veículos com combos dependentes"""
    
    marca = forms.ModelChoiceField(
        queryset=MarcaVeiculo.objects.filter(ativo=True),
        empty_label="Selecione a marca...",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_marca',
            'onchange': 'carregarModelos()'
        }),
        label='Marca'
    )
    
    modelo_veiculo = forms.ModelChoiceField(
        queryset=ModeloVeiculo.objects.none(),
        empty_label="Primeiro selecione a marca...",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_modelo_veiculo',
            'onchange': 'carregarAnos()'
        }),
        label='Modelo'
    )
    
    ano = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_ano'
        }),
        label='Ano'
    )
    
    cor_veiculo = forms.ModelChoiceField(
        queryset=CorVeiculo.objects.filter(ativo=True),
        empty_label="Selecione a cor...",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_cor_veiculo'
        }),
        label='Cor'
    )
    
    class Meta:
        model = Veiculo
        fields = ['placa', 'marca', 'modelo_veiculo', 'ano', 'cor_veiculo', 'km', 'chassi', 'renavam']
        widgets = {
            'placa': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: ABC-1234',
                'maxlength': 8,
                'style': 'text-transform: uppercase;'
            }),
            'km': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 150000',
                'min': 0
            }),
            'chassi': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 9BM123456789012345',
                'maxlength': 17
            }),
            'renavam': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 12345678901',
                'maxlength': 11
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Se estamos editando um veículo existente
        if self.instance and self.instance.pk:
            if self.instance.marca_veiculo:
                self.fields['marca'].initial = self.instance.marca_veiculo.marca
                self.fields['modelo_veiculo'].queryset = ModeloVeiculo.objects.filter(
                    marca=self.instance.marca_veiculo.marca,
                    ativo=True
                )
                self.fields['modelo_veiculo'].initial = self.instance.modelo_veiculo
                
                # Carregar anos disponíveis para o modelo
                if self.instance.modelo_veiculo:
                    anos = self.instance.modelo_veiculo.anos_disponiveis
                    self.fields['ano'].choices = [(ano, ano) for ano in anos]
                    self.fields['ano'].initial = self.instance.ano
        
        # Ordenar cores por popularidade
        self.fields['cor_veiculo'].queryset = CorVeiculo.objects.filter(ativo=True).order_by('-popular', 'nome')
    
    def clean_placa(self):
        placa = self.cleaned_data['placa'].upper().replace('-', '').replace(' ', '')
        
        # Validação de formato de placa brasileira
        if len(placa) != 7:
            raise forms.ValidationError('Placa deve ter exatamente 7 caracteres.')
        
        # Formato antigo: ABC1234
        if placa[:3].isalpha() and placa[3:].isdigit():
            return f"{placa[:3]}-{placa[3:]}"
        
        # Formato Mercosul: ABC1D23
        if (placa[:3].isalpha() and placa[3].isdigit() and 
            placa[4].isalpha() and placa[5:].isdigit()):
            return f"{placa[:3]}{placa[3]}{placa[4]}{placa[5:]}"
        
        raise forms.ValidationError('Formato de placa inválido.')
    
    def clean_chassi(self):
        chassi = self.cleaned_data.get('chassi', '').upper()
        if chassi and len(chassi) != 17:
            raise forms.ValidationError('Chassi deve ter exatamente 17 caracteres.')
        return chassi
    
    def clean_renavam(self):
        renavam = self.cleaned_data.get('renavam', '').replace(' ', '').replace('-', '')
        if renavam and not renavam.isdigit():
            raise forms.ValidationError('RENAVAM deve conter apenas números.')
        if renavam and len(renavam) != 11:
            raise forms.ValidationError('RENAVAM deve ter exatamente 11 dígitos.')
        return renavam
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Definir marca baseada no modelo selecionado
        if self.cleaned_data.get('modelo_veiculo'):
            instance.marca_veiculo = self.cleaned_data['modelo_veiculo'].marca
        
        if commit:
            instance.save()
        return instance

class PneuForm(forms.ModelForm):
    """Formulário para cadastro de pneus"""
    
    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop('usuario', None)
        super().__init__(*args, **kwargs)
        
        if self.usuario:
            self.fields['veiculo'].queryset = Veiculo.objects.filter(usuario=self.usuario)
    
    class Meta:
        model = Pneu
        fields = [
            'veiculo', 'posicao', 'marca', 'modelo', 'medida', 
            'pressao', 'profundidade_sulco', 'custo', 'data_instalacao',
            'km_instalacao', 'fornecedor', 'lote_fabricacao', 
            'numero_serie', 'marca_fogo', 'observacoes'
        ]
        widgets = {
            'veiculo': forms.Select(attrs={'class': 'form-control'}),
            'posicao': forms.Select(attrs={'class': 'form-control'}),
            'marca': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Michelin'
            }),
            'modelo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: XZA2 Energy'
            }),
            'medida': forms.Select(attrs={'class': 'form-control'}),
            'pressao': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 120.0',
                'step': '0.1'
            }),
            'profundidade_sulco': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 8.5',
                'step': '0.1'
            }),
            'custo': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 1500.00',
                'step': '0.01'
            }),
            'data_instalacao': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'km_instalacao': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 150000'
            }),
            'fornecedor': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: XBPNEUS'
            }),
            'lote_fabricacao': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: LOT2024001'
            }),
            'numero_serie': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: SN123456789'
            }),
            'marca_fogo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: DOT 1234'
            }),
            'observacoes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observações técnicas sobre o pneu...'
            }),
        }

class HistoricoPneuForm(forms.ModelForm):
    """Formulário para histórico de pneus"""
    
    class Meta:
        model = HistoricoPneu
        fields = ['tipo_evento', 'data_evento', 'km_evento', 'descricao', 'custo']
        widgets = {
            'tipo_evento': forms.Select(attrs={'class': 'form-control'}),
            'data_evento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'km_evento': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 160000'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descrição do evento...'
            }),
            'custo': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 250.00',
                'step': '0.01'
            }),
        }

