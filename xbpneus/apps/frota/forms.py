from django import forms
from .models import Veiculo, Pneu, HistoricoPneu

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

