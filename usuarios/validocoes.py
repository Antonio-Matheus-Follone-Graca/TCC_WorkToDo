# esse arquivo faz parte das validacoes referentes ao usuario, onde suas funcoes sao chamadas no forms.py 


# o django já tem um método nativo para campos não vazios e colocando min min_length= valor nos campos do forms.py ele já valida para vc 

# e  validação interna para e-mail 


# importando model User 

from django.contrib.auth.models import User

def senhas_diferentes(senha1,senha2,lista_de_erros):
    '''
        verifica se a senha é diferente do confirmar senha 
    '''

    if senha1 != senha2:
        lista_de_erros['confirmar_senha'] = 'Senhas não são iguais'


def username_sem_arroba(username,lista_de_erros):
    if "@" in username:
        lista_de_erros['username'] = 'digite seu username corretamente'
    



def nick_em_uso(nick,lista_de_erros):
    '''
        funcao que verifica se o username do  usuario está em uso 
        nick: username 
        lista_de_erros = dicionario com mensagem e campo do erro
        pagina_cadastro: se for true ou false muda a instrucao do filter
    '''

 
 
    # se o username já existe na tabela auth_user 
    if User.objects.filter(username = nick).exists():
        lista_de_erros['username'] = 'esse nick já existe, use outro, por favor.'


def email_em_uso(email,lista_de_erros):
    '''
        funcao que verifica se o email no cadastrar usuario está em uso 
        nick: username 
        lista_de_erros = dicionario com mensagem e campo do erro    
    '''
    # se o username já existe na tabela auth_user 
    if User.objects.filter(email = email).exists() == True:
        lista_de_erros['email'] = 'esse email já está em uso, use outro, por favor.'


def campo_vazio(campo,lista_de_erros):
    if not campo:
        return True 

    else:
        return False


def codigo_numeros_errados(codigo,lista_de_erros):
    if codigo.isdigit() == False:
        lista_de_erros['codigo'] = 'digite apenas números'



