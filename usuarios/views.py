
from django.shortcuts import render, redirect,get_object_or_404
import random
# notify
from email.message import EmailMessage
import ssl
import smtplib
# importando o forms 
from usuarios.forms import LoginForms,CadastroForms, DeletarContaForms,AlterarSenhaForms,VerifciarUsuario
# criptografia padrão django 
# importando model user 
from django.contrib.auth.models import User
# importando biblioteca para login  e messages 
from django.contrib import auth, messages
# importando view das anotacoes que lista todas as anotações do usuario 
from anotacoes.views import listar_anotacoes
from django.contrib.auth.decorators import login_required
#----------------------------------------------------------------------------------------------------------------------
# Create your views here.
# rota aonde fica a página de login
def index(request):
    # se o usuario estiver logado mas se ele colocar o endereço da url dessa pagina
    # o redireciona para a dashboard
    if request.user.is_authenticated: 
        return redirect('dashboard')
    
    else:
        form = LoginForms()
        # passando o form para dicionario
        contexto = {'login_form':form}
        return render(request,'index.html',contexto)
#----------------------------------------------------------------------------------------------------------------------
# view que recebe o formulário de login 
def logar(request):
    # validando se formulário foi enviado ou não 
    if request.method ==  'POST': 
        
        # pegando dados do formulário para verificar o login
        form = LoginForms(request.POST)
        contexto = {'login_form':form}

        email = request.POST['email_username']
        senha = request.POST['senha']
        # verificando se o formulário foi preenchido corretamente(sem erros no formulario)

        # se for valido, sem erros  
        if form.is_valid():
            usuario = User.objects.filter(email = email) # comandos para a condicao do login
           

            if  usuario.exists():
                # filtrando o registro do usuario pelo email, onde pego o username pelo email, gambiara do django pois só faz login pelo username e senha
                nome = User.objects.filter(email = email).values_list('username',flat = True).get()
                #autenticando o usuário 
                user = auth.authenticate(request,username= nome,password = senha)
               
                #print('variavel usuario IS ACTIVE ')
                

                   
                # se o user e senha  estão corretos, entao achou user NAO É none   
                if user is not None:
                    # realizando o login 
                    auth.login(request,user)
                    # mandando o usuario para a dashboard
                    return redirect('dashboard')
                
               
                           
                else:
                    # percorrendo objeto usuariom django funciona assim mesmo tendo um registro apenas
                    for valor in usuario:
                        validate = valor.is_active
                        receiver = valor.email
                    
                    
                    
                    
                    if validate == False:
                        # chamando metodo que manda para a página de verificacao  e passando o e-mail do usuario como parametro
                        return redirect('pagina_verificacao', email = receiver)
                    
                    else:
                        messages.error(request, 'senha errada')
                        return render(request,'index.html',contexto)


                   
            else:
                messages.error(request, 'Usuário não encontrado')
                return render(request,'index.html',contexto)


        # form invalidio
        else:
            contexto = {'login_form':form}
            return render(request,'index.html',contexto)

    else:
        return redirect('index')

    return render(request,'index.html',contexto)   
#----------------------------------------------------------------------------------------------------------------------
# view que redireciona para a página de criar conta 
def cadastrar(request):
    # se o usuario estiver logado mas se ele colocar o endereço da url dessa pagina
    # o redireciona para a dashboard
    if request.user.is_authenticated: 
       return redirect('dashboard')
    
    else: 
        formulario_cadastro = CadastroForms()
        # passando o form para dicionario
        contexto = {'formulario_cadastro':formulario_cadastro}
        # mandando o formulario para a pagina de cadastro 
        return render(request,'cadastrar.html',contexto)


# view que cria a conta, que recebe os dados do formulário formCriarConta
def insertUsuario(request):
    # se o usuario clicou no enviar formulario
    if request.method == 'POST':
        # pegando os dados do formulario  da requisicao POST
        formulario_cadastro = CadastroForms(request.POST)

        # pegando os valores de cada campo 
        username = request.POST['username']
        username= username.strip()
        nome = request.POST['nome']
        sobrenome = request.POST['sobrenome']
        email = request.POST['email']
        email= email.strip()
        senha = request.POST['senha']        
        # if para ver se o formulário está, valido não tem nenhum erro
        if formulario_cadastro.is_valid():
           # criando usuario
            user =  User.objects.create_user(username=username, email=email,password=senha,first_name=nome, last_name=sobrenome, is_superuser= False, is_active= False)
            user.save()
           
           # redirecionando para à pagina de login 
            return redirect('index')
        
        else:
            contexto = {'formulario_cadastro':formulario_cadastro}
            return render(request,'cadastrar.html',contexto)
        
    else:
        return redirect('cadastrar')
#----------------------------------------------------------------------------------------------------------------------
# so realiza o logout
def logout(request):
    # deslogando o usuario
    auth.logout(request)
    # redirecionando para a pagina principal 
    return redirect('index')
#----------------------------------------------------------------------------------------------------------------------
# mostrando as anotações dos usuarios 
@login_required
def dashboard(request):
    # verifica se o usuario está logado 
        if request.user.is_authenticated: 
            # chamando funcao do aplicativo anotações que lista todas as anotações 

            # funcao que retorna as anotacoes do usuario 
            dados = listar_anotacoes(request.user.id)
            # passando os dados recebidos para a dashboard.html
            return render(request,'dashboard.html',dados) 
        
        else :
            return redirect('index')

''' 
        if request.user.is_authenticated: 
        id = request.user.id 

        # guardando anotacoes do usuario via select pelo seu id 
        anotacoes = Anotacoes.objects.filter(fk_pessoa_id = id)

        # dicionario com as anotacoes 
        dados = {
            'anotacoes' : anotacoes
        }
        return render(request,'dashboard.html',dados) 
    
    else:
        return redirect('index')
'''
#----------------------------------------------------------------------------------------------------------------------
# para acessar essa pagina, o usuario deverá estar logado
@login_required
def pagina_deletar_usuario(request):
    if request.method == 'GET':
        deletar_conta_forms = DeletarContaForms()
        contexto = {
            'deletar_conta_forms' : deletar_conta_forms
        }
        return render(request,'deletar_usuario.html',contexto)

    else:
        return redirect('dashboard')
#----------------------------------------------------------------------------------------------------------------------
def deletar_conta(request):
    if request.method == 'POST':
        deletar_conta_forms = DeletarContaForms(request.POST)

        contexto = {
            'deletar_conta_forms' : deletar_conta_forms
        }
        # pegando a senha do formulario
        senha = request.POST['senha']
        # pegando usuario por id via request
        user = get_object_or_404(User,pk = request.user.id)
        if deletar_conta_forms.is_valid():
            senha_correta =auth.authenticate(username= user.username ,password = senha)
            if senha_correta == None:
               messages.error(request, 'senha errada')
               return render(request,'deletar_usuario.html', contexto)
              
            else:
                
                user.delete()
                return redirect('index')
           
        
        else:
            return render(request,'deletar_usuario.html', contexto)
        


       
        # ao deletar usuario os registros de anotações, grupos e tarefas também são deletados  e já faz o logout sozinho
    else:
        return redirect('dashboard')
#----------------------------------------------------------------------------------------------------------------------
# para acessar essa pagina, o usuario deverá estar logado
@login_required
def pagina_alterar_usuario(request):
    if request.method == 'GET':
        # pegando os dados do usuario via request
        dados_usuario_edit = User.objects.get(id = request.user.id)
        # passando os dados para um dicionario
        dados = {
            'first_name': dados_usuario_edit.first_name,
            'last_name': dados_usuario_edit.last_name,
            'email': dados_usuario_edit.email,
            'username':dados_usuario_edit.username
            # não passou o id pois dá para pegar via request
        }
        contexto = {
            'editar_conta_forms' : dados
        }

        return render(request,'form_editar_usuario.html',contexto)
    
    else:
        return redirect('dashboard')
#----------------------------------------------------------------------------------------------------------------------
def update_usuario(request):
    # se o usuario clicou no enviar formulario
    if request.method == 'POST':
        # pegando dados do formulario 
        nick = request.POST['username']
        nome = request.POST['first_name']
        sobrenome = request.POST['last_name']
        email = request.POST['email']

        # contexto para não limpar os valores do formulario caso fiquem vazios no if das validações
        dados = {
            'first_name': nome,
            'last_name': sobrenome,
            'email': email,
            'username':nick
          
        }
 
        contexto = {
            'editar_conta_forms' : dados
        }


        # validações

        if nick.strip() == '':
            messages.error(request, 'O campo username não pode ficar em branco')
            return render(request,'form_editar_usuario.html',contexto)  
        
        if nome.strip() == '':
            messages.error(request, 'O campo nome não pode ficar em branco')
            return render(request,'form_editar_usuario.html',contexto)  

        if sobrenome.strip() == '':
            messages.error(request, 'O campo sobrenome não pode ficar em branco')
            return render(request,'form_editar_usuario.html',contexto)   

        if email.strip() == '':
            messages.error(request, 'O campo email não pode ficar em branco')
            return render(request,'form_editar_usuario.html',contexto)  

        # validação  para ver se o username já está em uso 

        # exclude é para excluir do select o id do usuario,pois caso ele não altere seu nick

        # mostrará que o nick já está em uso 
        if User.objects.filter(username = nick).exclude(id= request.user.id).exists():
            messages.error(request, 'username em uso, use outro ')
            return render(request,'form_editar_usuario.html',contexto) 
        

        # validação para ver se  o e-mail está livre para uso 

        if User.objects.filter(email = email ).exclude(id= request.user.id).exists():
            messages.error(request, 'email em uso, use outro ')
            return render(request,'form_editar_usuario.html',contexto)  
        
        # atualizando dados 
        usuario_update = User.objects.get(pk = request.user.id)
        usuario_update.username = request.POST['username']
        usuario_update.first_name= request.POST['first_name']
        usuario_update.last_name= request.POST['last_name']    
        usuario_update.email= request.POST['email']

        # atualizando dados do usuario 

        usuario_update.save()

        # redirecionando para pagina
        print('dados atualizados com sucesso ') 
        return redirect('dashboard')

    else:
        return redirect('dashboard')
#----------------------------------------------------------------------------------------------------------------------
# pagina de alterar senha
# para acessar essa pagina, o usuario deverá estar logado
@login_required
def pagina_alterar_senha(request):
    if request.method == 'GET':
        form_senha =  AlterarSenhaForms()
        contexto = {'form_senha':form_senha}
        return render(request,'form_editar_senha.html',contexto)


    else:
        return redirect('dashboard')
#----------------------------------------------------------------------------------------------------------------------
def atualizar_senha(request):
    if request.method == 'POST':
        # colocando os dados na classe do formulario
        form_senha =  AlterarSenhaForms(request.POST)
        # pegando dos dados via formulario
        senha_nova = request.POST['senha']
        senha_nova= senha_nova.strip() # tirando os espaços de inicio e fim do campo 
        confirmar_senha = request.POST['confirmar_senha']
        confirmar_senha=   confirmar_senha.strip() # tirando os espaços de inicio e fim do campo 
        senha_atual = request.POST['senha_atual']
        senha_atual= senha_atual.strip() # tirando os espaços de inicio e fim do campo 
        # contexto 
        contexto = {'form_senha':form_senha}
        # pegando usuario por id via request
        user = get_object_or_404(User,pk = request.user.id)
        
        if form_senha.is_valid():
            senha_correta =auth.authenticate(username= user.username ,password = senha_atual)
            if senha_correta == None:
                messages.error(request, 'senha  atual está errada')
                
                return render(request,'form_editar_senha.html', contexto)

            # se a senha atual estiver correta, atualiza a senha 
            else:
                # set_password é o metodo padrão do django para atualizações de senha
                user.set_password(senha_nova)
                # atualizando 
                user.save()
                # redirecionando 
                return redirect('dashboard')
     
                

        else:
            contexto = {'form_senha':form_senha}
            return render(request,'form_editar_senha.html',contexto)


    else:
        return redirect('dashboard')
#----------------------------------------------------------------------------------------------------------------------
# metodo de gerar um número com 6 digitos 
def gerar_numero():
    
    teste = 0 
    # lista
    codigo = [] 
    # de 1 ate 6 
    for contador in range(0,6):
        # adicionando valor na posicao da lista 
        codigo.append (random.randint(0,9) )
    
    # juntando os numeros mas para isso preciso transformar em string 
    codigo_string = "".join(map(str, codigo))
    # transformando em número 
    codigo_final = int(codigo_string)
    return  codigo_final
#----------------------------------------------------------------------------------------------------------------------
def Notifica_usuario(receiver, subject, body):
    print()

    email_sender = 'notifications.worktodo@gmail.com'
    email_password = 'keccwwdnreawqxje'
    email_receiver = receiver

    Subject = subject
    Body    = body

    em = EmailMessage()
    em['From']    = email_sender
    em['To']      = email_receiver
    em['Subject'] = Subject
    em.set_content(Body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())
#----------------------------------------------------------------------------------------------------------------------
def pagina_verificacao(request,email):
    '''
    receiver: e-mail do usuario

    essa funcao foi chamada  pelo metodo de logar na parte do if is_active == False na linha 78
    '''
    # gera um código de 6 digitos e em seguida envia um e-mail para o usuario
    codigo = gerar_numero()
    Notifica_usuario(email, "Work To Do - Verification", f"Código de verificação: {codigo}")

    # chamando formulário 
    form = VerifciarUsuario()
    # dicionario com codigo do usuário e o formulario de verificar

    codigo = str(codigo)

    contexto = {
        'dicionario_codigo' : hash(codigo),
        'numero': codigo,
        'form_verificar': form
    }

  
    return render(request, 'verificacao.html',contexto)
#----------------------------------------------------------------------------------------------------------------------

def verificar_codigo(request):
    # se clicou  no formulario

    if request.method == 'POST':
        form_verificar = VerifciarUsuario(request.POST)
        hash = {
            'Teste'
        }
        contexto = {
            'form_verificar':form_verificar,
            'hash': hash
        }
        codigo = request.POST['codigo']
        codigo_hash = request.POST['codigo_hash']
        if form_verificar.is_valid():
            return redirect('index') 

        else:
            return render(request,'verificacao.html',contexto)
        
        # transformando em string e colocando em hash
        # codigo = str(codigo)
        # codigo em hash codigo_digitado_hash = (hash(codigo))
    else:
        return redirect('index')




   
  
     

