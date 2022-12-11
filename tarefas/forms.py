# importando django forms 
from django import forms
from tarefas.models import Tarefas
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker
from tarefas.validacoes import *
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
#------------------------------------------------------------------------------------------------------------
class  FormTarefas(forms.ModelForm):
    # puxando os campos da tabela
    def clean(self):
        cleaned_data = super(FormTarefas,self).clean()
        date_start = cleaned_data.get('date_start')
        date_completion = cleaned_data.get('date_completion')
        lista_de_erros = {}
        # chamando as funcoes#
        data_inicio_maior_que_data_conclusao(date_start,date_completion,lista_de_erros)
        # coloquei na views de tarefas, no metodo data_ja_passou para automacao do tcc
        #data_menor_data_atual(date_start,'date_start',lista_de_erros)
        #data_menor_data_atual(date_completion,'date_completion',lista_de_erros)
        # se a lista de erros estiver com um valor, então há um erro nela
        if lista_de_erros is not None:
        # looping de cada erro
            for erro in lista_de_erros:                                                                     
                mensagem_erro = lista_de_erros[erro]     
                # atribuindo erro na classe
                self.add_error(erro,mensagem_erro)
        return self.cleaned_data
#------------------------------------------------------------------------------------------------------------
    class Meta:                                                                                             
        model = Tarefas                                                                                    
        exclude = ['fk_pessoa','fk_grupo','date','status','date_conclusao']                                 
        labels = {                                                                                          
         'title': ('Título  da tarefa'),                                                                    
         'body': ('Corpo'),                                                                                 
         'date_completion': ('Data prevista para conclusão'),                                               
         'date_start': ('Data de início da tarefa ')                                                        
        }                                                                                                   
        widgets = {                                                                                         
            'date_start': DateTimePicker(                                                                   
                options={                                                                                   
                    'useCurrent': True,                                                                     
                    'collapse': False,                                                                      
                },                                                                                          
                attrs={                                                                                     
                    'append': 'fa fa-calendar',                                                             
                    'icon_toggle': True,                                                                    
                }                                                                                           
            ),                                                                                              
            'date_completion': DateTimePicker(                                                              
                options={
                    'useCurrent': True,
                    'collapse': False,
                },
                attrs={
                    'append': 'fa fa-calendar',
                    'icon_toggle': True,
                }
            ),
        }
#------------------------------------------------------------------------------------------------------------
