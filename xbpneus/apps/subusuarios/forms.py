from django import forms
from django.contrib.auth.hashers import make_password
from .models import SubUsuario, ModuloAcesso
from django.core.exceptions import ValidationError


class SubUsuarioForm(forms.ModelForm):
    senha = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite a senha'
        }),
        required=False,
        label="Senha",
        help_text="Deixe em branco para enviar convite por e-mail"
    )
    
    confirmar_senha = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirme a senha'
        }),
        required=False,
        label="Confirmar Senha"
    )
    
    enviar_convite = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'id': 'id_enviar_convite'
        }),
        required=False,
        initial=False,
        label="Enviar convite por e-mail",
        help_text="Marque para enviar um convite para o subusuário definir sua própria senha"
    )
    
    modulos = forms.ModelMultipleChoiceField(
        queryset=ModuloAcesso.objects.filter(ativo=True).order_by('id'),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Selecione as Áreas de Acesso"
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Sempre mostra TODOS os módulos ativos!
        self.fields['modulos'].queryset = ModuloAcesso.objects.filter(ativo=True).order_by('id')
    
    class Meta:
        model = SubUsuario
        fields = [
            'nome', 'email', 'login', 'funcao', 'modulos', 'senha', 'confirmar_senha', 'ativo'
        ]
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome completo do subusuário'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@exemplo.com'
            }),
            'login': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'usuario123'
            }),
            'funcao': forms.Select(attrs={
                'class': 'form-select'
            }),
            'ativo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'nome': 'Nome Completo *',
            'email': 'E-mail *',
            'login': 'Login/Usuário *',
            'funcao': 'Função *',
            'ativo': 'Usuário Ativo',
        }
        help_texts = {
            'nome': 'Digite o nome completo do subusuário',
            'email': 'E-mail será usado para comunicações e login',
            'login': 'Nome de usuário único para acesso ao sistema',
            'funcao': 'Selecione a função/cargo do subusuário',
            'ativo': 'Desmarque para desativar o subusuário',
        }

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get('senha')
        confirmar_senha = cleaned_data.get('confirmar_senha')
        enviar_convite = cleaned_data.get('enviar_convite')
        
        # Se não vai enviar convite, senha é obrigatória
        if not enviar_convite:
            if not senha:
                raise ValidationError('Senha é obrigatória quando não enviar convite por e-mail.')
            
            if senha != confirmar_senha:
                raise ValidationError('As senhas não coincidem.')
        
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Definir o usuário principal
        if self.usuario_principal:
            instance.usuario_principal = self.usuario_principal
        
        # Se tem senha, criptografar
        if self.cleaned_data.get('senha'):
            instance.password = make_password(self.cleaned_data['senha'])
        
        if commit:
            instance.save()
            self.save_m2m()
        
        return instance

