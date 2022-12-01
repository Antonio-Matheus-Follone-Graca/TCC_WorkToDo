from django import forms
from django import forms

from grupos.models import Grupo

from django.forms.widgets import TextInput

class FormGrupos(forms.ModelForm):
    # puxando os campos da tabela 
    class Meta:
        model = Grupo
        exclude = ['fk_pessoa'] # não quero mostrar esse campo 
        labels = {
            'title': ('Titulo do grupo'),
            'description':('Descrição'),
            'color':('Cor')
        }
        widgets = {
            'color': TextInput(attrs={'type': 'color'}),
        }