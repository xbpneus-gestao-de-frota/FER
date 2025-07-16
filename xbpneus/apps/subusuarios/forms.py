from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import SubUsuario, ModuloAcesso, PerfilAcesso


class SubUsuarioForm(forms.ModelForm):
    # Campos de autenticação
    senha = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite a senha'
        }),
        label="Senha",
        help_text="Deixe em branco para enviar convite por e-mail",
        required=False
    )
    
    confirmar_senha = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirme a senha'
        }),
        label="Confirmar Senha",
        required=False
    )
    
    enviar_convite = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'id': 'id_enviar_convite'
        }),
        label="Enviar convite por e-mail",
        help_text="Marque para enviar um convite para o subusuário definir sua própria senha",
        required=False,
        initial=False  # Mudando para False para mostrar campos de senha por padrão
    )
    
    # Liberações de acesso com interface melhorada
    modulos = forms.ModelMultipleChoiceField(
        queryset=ModuloAcesso.objects.filter(ativo=True).order_by('id'),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Selecione os Pilares"
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
        help_text="Selecione um perfil para aplicar permissões pré-definidas automaticamente"
    )
    
    class Meta:
        model = SubUsuario
        fields = ['nome', 'email', 'login', 'funcao', 'modulos', 'ativo']
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
    
    def __init__(self, *args, **kwargs):
        self.usuario_principal = kwargs.pop('usuario_principal', None)
        super().__init__(*args, **kwargs)
        
        # Organizar módulos por categoria para melhor visualização
        self.fields['modulos'].queryset = ModuloAcesso.objects.filter(ativo=True).order_by('ordem', 'nome')
        
        # Se estamos editando, preencher campos de senha como opcionais
        if self.instance.pk:
            self.fields['senha'].help_text = "Deixe em branco para manter a senha atual"
            self.fields['enviar_convite'].initial = False
    
    def clean_login(self):
        login = self.cleaned_data['login']
        
        # Verifica se já existe outro subusuário com o mesmo login para o mesmo usuário principal
        queryset = SubUsuario.objects.filter(
            login=login, 
            usuario_principal=self.usuario_principal
        )
        
        # Se estamos editando, exclui o próprio registro da verificação
        if self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)
        
        if queryset.exists():
            raise forms.ValidationError(
                'Já existe um subusuário com este login cadastrado.'
            )
        
        return login
    
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
    
    def clean_modulos(self):
        modulos = self.cleaned_data.get("modulos")
        if not modulos:
            raise ValidationError("Selecione pelo menos um pilar.")
        return modulos
    
    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get('senha')
        confirmar_senha = cleaned_data.get('confirmar_senha')
        enviar_convite = cleaned_data.get('enviar_convite')
        
        # Validação de senha
        if senha and not enviar_convite:
            # Se senha foi fornecida, validar
            if senha != confirmar_senha:
                raise forms.ValidationError({
                    'confirmar_senha': 'As senhas não coincidem.'
                })
            
            # Validar força da senha
            try:
                validate_password(senha)
            except ValidationError as e:
                raise forms.ValidationError({
                    'senha': e.messages
                })
        elif not senha and not enviar_convite:
            # Se nem senha nem convite foram especificados
            raise forms.ValidationError(
                'Você deve definir uma senha ou marcar para enviar convite por e-mail.'
            )
        
        return cleaned_data
    
    def save(self, commit=True):
        subusuario = super().save(commit=False)
        if self.usuario_principal:
            subusuario.usuario_principal = self.usuario_principal
        
        # Gerenciar senha
        senha = self.cleaned_data.get('senha')
        enviar_convite = self.cleaned_data.get('enviar_convite')
        
        if senha and not enviar_convite:
            # Definir senha diretamente
            subusuario.set_senha(senha)
        elif enviar_convite:
            # Preparar para envio de convite
            subusuario.convite_enviado = False
            subusuario.senha_definida = False
            subusuario.gerar_novo_token_convite()
        
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

