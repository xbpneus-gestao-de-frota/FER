from django import forms
from .models import SubUsuario

class SubUsuarioForm(forms.ModelForm):
    class Meta:
        model = SubUsuario
        fields = ['nome', 'email', 'funcao', 'ativo']
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
        return subusuario

