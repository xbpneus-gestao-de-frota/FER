from django import forms
from .models import ConfiguracaoEmpresa, PreferenciaSistema


class ConfiguracaoEmpresaForm(forms.ModelForm):
    class Meta:
        model = ConfiguracaoEmpresa
        exclude = ['usuario', 'data_criacao', 'data_atualizacao']
        widgets = {
            'razao_social': forms.TextInput(attrs={'class': 'form-control'}),
            'nome_fantasia': forms.TextInput(attrs={'class': 'form-control'}),
            'cnpj': forms.TextInput(attrs={'class': 'form-control', 'data-mask': '00.000.000/0000-00'}),
            'inscricao_estadual': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'data-mask': '(00) 00000-0000'}),
            'email_comercial': forms.EmailInput(attrs={'class': 'form-control'}),
            'site': forms.URLInput(attrs={'class': 'form-control'}),
            'cep': forms.TextInput(attrs={'class': 'form-control', 'data-mask': '00000-000'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control'}),
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'complemento': forms.TextInput(attrs={'class': 'form-control'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}, choices=[
                ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'),
                ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'),
                ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'),
                ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'),
                ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'),
                ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'),
                ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')
            ]),
            'fuso_horario': forms.Select(attrs={'class': 'form-control'}),
            'moeda': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adicionar choices para fuso_horario
        self.fields['fuso_horario'].widget.choices = [
            ('America/Sao_Paulo', 'Brasília (UTC-3)'),
            ('America/Manaus', 'Manaus (UTC-4)'),
            ('America/Rio_Branco', 'Rio Branco (UTC-5)'),
        ]
        
        # Adicionar choices para moeda
        self.fields['moeda'].widget.choices = [
            ('BRL', 'Real (R$)'),
            ('USD', 'Dólar ($)'),
            ('EUR', 'Euro (€)'),
        ]


class PreferenciaSistemaForm(forms.ModelForm):
    class Meta:
        model = PreferenciaSistema
        exclude = ['usuario', 'data_criacao', 'data_atualizacao']
        widgets = {
            'tema': forms.Select(attrs={'class': 'form-control'}),
            'idioma': forms.Select(attrs={'class': 'form-control'}),
            'notificacoes_email': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notificacoes_sistema': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'itens_por_pagina': forms.NumberInput(attrs={'class': 'form-control', 'min': '10', 'max': '100'}),
            'dashboard_compacto': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

