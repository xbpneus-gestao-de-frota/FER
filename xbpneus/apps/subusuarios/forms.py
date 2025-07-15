from django import forms
from .models import SubUsuario, ModuloAcesso, PerfilAcesso


class SubUsuarioForm(forms.ModelForm):
    modulos = forms.ModelMultipleChoiceField(
        queryset=ModuloAcesso.objects.filter(ativo=True),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'
        }),
        required=False,
        label="Liberações de Acesso"
    )
    
    perfil_acesso = forms.ModelChoiceField(
        queryset=PerfilAcesso.objects.filter(ativo=True),
        required=False,
        empty_label="Selecione um perfil (opcional)",
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'id_perfil_acesso'
        }),
        label="Perfil de Acesso",
        help_text="Selecione um perfil para aplicar permissões pré-definidas"
    )
    
    class Meta:
        model = SubUsuario
        fields = ['nome', 'email', 'funcao', 'modulos', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome completo do subusuário'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@exemplo.com'
            }),
            'funcao': forms.Select(attrs={
                'class': 'form-select'
            }),
            'ativo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'nome': 'Nome Completo',
            'email': 'E-mail',
            'funcao': 'Função',
            'ativo': 'Usuário Ativo',
        }
        help_texts = {
            'nome': 'Digite o nome completo do subusuário',
            'email': 'E-mail será usado para comunicações',
            'funcao': 'Selecione a função/cargo do subusuário',
            'ativo': 'Desmarque para desativar o subusuário',
        }
    
    def __init__(self, *args, **kwargs):
        self.usuario_principal = kwargs.pop('usuario_principal', None)
        super().__init__(*args, **kwargs)
        
        # Organizar módulos por categoria para melhor visualização
        self.fields['modulos'].queryset = ModuloAcesso.objects.filter(ativo=True).order_by('ordem', 'nome')
    
    def clean_email(self):
        email = self.cleaned_data['email']
        
        # Verifica se já existe outro subusuário com o mesmo email para o mesmo usuário principal
        queryset = SubUsuario.objects.filter(
            email=email, 
            usuario_principal=self.usuario_principal
        )
        
        # Se estamos editando, exclui o próprio registro da verificação
        if self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)
        
        if queryset.exists():
            raise forms.ValidationError(
                'Já existe um subusuário com este e-mail cadastrado.'
            )
        
        return email
    
    def save(self, commit=True):
        subusuario = super().save(commit=False)
        if self.usuario_principal:
            subusuario.usuario_principal = self.usuario_principal
        if commit:
            subusuario.save()
            self.save_m2m()  # Salvar relacionamentos many-to-many
        return subusuario


class PerfilAcessoForm(forms.ModelForm):
    """Formulário para criar/editar perfis de acesso"""
    modulos = forms.ModelMultipleChoiceField(
        queryset=ModuloAcesso.objects.filter(ativo=True),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'
        }),
        required=False,
        label="Módulos Incluídos"
    )
    
    class Meta:
        model = PerfilAcesso
        fields = ['nome', 'descricao', 'modulos', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Gestor Completo, Operacional Básico'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descrição do perfil e suas permissões'
            }),
            'ativo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class ModuloAcessoForm(forms.ModelForm):
    """Formulário para criar/editar módulos de acesso"""
    class Meta:
        model = ModuloAcesso
        fields = ['nome', 'slug', 'descricao', 'icone', 'ordem', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Gestão de Frota'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: frota'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descrição do módulo'
            }),
            'icone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: bi-truck (ícone Bootstrap)'
            }),
            'ordem': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'ativo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class FiltroSubUsuarioForm(forms.Form):
    """Formulário para filtros na listagem de subusuários"""
    funcao = forms.ChoiceField(
        choices=[('', 'Todas as Funções')] + SubUsuario.FUNCAO_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    ativo = forms.ChoiceField(
        choices=[('', 'Todos'), ('True', 'Ativos'), ('False', 'Inativos')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    modulo = forms.ModelChoiceField(
        queryset=ModuloAcesso.objects.filter(ativo=True),
        required=False,
        empty_label="Todos os Módulos",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

