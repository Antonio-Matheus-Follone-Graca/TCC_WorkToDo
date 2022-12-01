# importando django forms 
from django import forms

# importando todas as funcocoes do arquivo de validações dos campos do formulário

from usuarios.validocoes import * 

class LoginForms(forms.Form):
    email_username = forms.CharField(label='Email', max_length=200)
    senha = forms.CharField(label='Senha',min_length=6)

    # validacoes do formulário 

    def clean(self):
        email_username = self.cleaned_data.get('email_username')
        senha = self.cleaned_data.get('senha')

        # dicionario com lista de erros 
        
         
        lista_de_erros = {}

        # se a lista de erros estiver com um valor, então há um erro nela 
        if lista_de_erros is not None:
        # looping de cada erro 
            for erro in lista_de_erros:
                mensagem_erro = lista_de_erros[erro]
                # atribuindo erro na classe 
                self.add_error(erro,mensagem_erro)
        

        
        # retornando dados da classe clean 

        return self.cleaned_data


        



class CadastroForms(forms.Form):
    username = forms.CharField(label='username, deve ser único', max_length=200)
    nome = forms.CharField(label='nome',max_length=200)
    sobrenome = forms.CharField(label='sobrenome',max_length=200)
    email = forms.EmailField(label='email',max_length=200)
    senha = forms.CharField(label='senha',min_length=6)
    confirmar_senha = forms.CharField(label='confirmar senha',min_length=6)

    def clean(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        senha = self.cleaned_data.get('senha')
        nome = self.cleaned_data.get('nome')
        sobrenome = self.cleaned_data.get('sobrenome')
        senha = self.cleaned_data.get('senha')
        confirmar_senha = self.cleaned_data.get('confirmar_senha')

        # dicionario com lista de erros 
        lista_de_erros = {}
       # validação do campo vazio, else se for False  chama as outras funções

       # pois preciso das outras funcoes para validacoes, porém com elas a função nativa do django forms de validar campo vazio não roda 
        if campo_vazio(username,lista_de_erros) == True:
           pass 
        else:
            senhas_diferentes(senha,confirmar_senha,lista_de_erros)
            username_sem_arroba (username,lista_de_erros)
            nick_em_uso(nick= username, lista_de_erros=lista_de_erros)
            email_em_uso(email,lista_de_erros)
   
        # se a lista de erros estiver com um valor, então há um erro nela 
        if lista_de_erros is not None:
        # looping de cada erro 
            for erro in lista_de_erros:
                mensagem_erro = lista_de_erros[erro]
                # atribuindo erro na classe 
                self.add_error(erro,mensagem_erro)
    
    
        # retornando dados da classe clean 
        return self.cleaned_data


class DeletarContaForms(forms.Form):
    senha = forms.CharField(label='Senha',min_length=6, required = True )


class AlterarSenhaForms(forms.Form):
    # campo de digitar senha, confirmar senha e digitar a senha atual para  a atualização da senha
    senha = forms.CharField(label='senha nova',min_length=6)
    confirmar_senha = forms.CharField(label='confirmar senha',min_length=6)
    senha_atual = forms.CharField(label='senha atual',min_length=6)

    def clean(self):
        senha = self.cleaned_data.get('senha')
        confirmar_senha = self.cleaned_data.get('confirmar_senha')
        # dicionario com lista de erros 
        lista_de_erros = {}
        # validação do campo vazio, else se for False  chama as outras funções
        # pois preciso das outras funcoes para validacoes, porém com elas a função nativa do django forms de validar campo vazio não roda 
        senhas_diferentes(senha,confirmar_senha,lista_de_erros)
         
           
           
   
     # se a lista de erros estiver com um valor, então há um erro nela 
        if lista_de_erros is not None:
        # looping de cada erro 
            for erro in lista_de_erros:
                mensagem_erro = lista_de_erros[erro]
                # atribuindo erro na classe 
                self.add_error(erro,mensagem_erro)
 
 
        # retornando dados da classe clean 
        return self.cleaned_data
















































