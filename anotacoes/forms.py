# importando django forms 


from django.shortcuts import render,redirect,get_object_or_404


from django import forms

from anotacoes.models import Anotacoes


class  FormAnotacoes(forms.ModelForm):
   
   
   
    # puxando os campos da tabela 
    class Meta:
        model = Anotacoes
      
        exclude = ['fk_pessoa','fk_grupo','date']        
       # exclude = ['fk_pessoa'] # não vou mostrar esse campo pois já irei seta-lo com o seu valor  no create 
        labels = {
            'title': ('Título'),
            'body': ('Corpo')
        }
        
        
        
        
        
  
    
        # não precisa de validacoes, a de campo vazio é feita automaticamente pelo django

        # mas caso queira fazer código abaixo
    '''
    def clean(self):

        # dicionario com lista de erros 
        lista_de_erros = {}

        # chamada de funcao 
        if lista_de_erros is not None:

            # looping de cada erro 
            for erro in lista_de_erros:
                mensagem_erro = lista_de_erros[erro]
         # atribuindo erro na classe 
        self.add_error("titulo","preencha o campo ")

        return self.cleaned_data
    '''
    

   
