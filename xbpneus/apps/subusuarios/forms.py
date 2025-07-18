from django import forms
from .models import SubUsuario, ModuloAcesso

class SubUsuarioForm(forms.ModelForm):
    modulos = forms.ModelMultipleChoiceField(
        queryset=ModuloAcesso.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Selecione as Áreas de Acesso"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['modulos'].queryset = ModuloAcesso.objects.filter(ativo=True).order_by('id')

    class Meta:
        model = SubUsuario
        fields = ['nome', 'email', 'login', 'funcao', 'modulos', 'ativo']
