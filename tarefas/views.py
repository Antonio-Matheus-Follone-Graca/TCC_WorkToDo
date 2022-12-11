from django.shortcuts import render,redirect,get_object_or_404
import tarefas

from tarefas.forms import FormTarefas

# importando model de anotacoes



from django.contrib import messages

# importando model de user 

from django.contrib.auth.models import User

# importando model de tarefa 

from tarefas.models import Tarefas


from grupos.models import Grupo


from datetime import datetime, date

from django.contrib.auth.decorators import login_required

# importando módulo do django para que o usuario precise estar logado para acessar as paginas







# Create your views here.



# renderiza  o formulario de tarefas
# para acessar esta pagina, o usuario deve estar logado
@login_required
def form_tarefas(request):
    # pegando o grupo pelo id do usuario 
    valores_grupos = Grupo.objects.filter(fk_pessoa_id = request.user.id)
   
 
    # chamando formulario 
    form_tarefas = FormTarefas()
   
    contexto = {'form_tarefa':form_tarefas,'grupo':valores_grupos}
    return render(request,'form_tarefas.html',contexto) 



def insert_tarefa(request):
    if request.method == 'POST':
        # pegando dados
        form_tarefas = FormTarefas(request.POST)
        contexto = {'form_tarefa':form_tarefas}

        titulo = request.POST['title']
        mensagem = request.POST['body']
        grupo = request.POST['fk_grupo']
        date_start = request.POST['date_start']
        date_completion = request.POST['date_completion']
        # formatando as datas para o formato datetime que  o banco de dados aceita: YYYY-MM-DD H:M:S  (ano-mes-dia Hora:Minuto:Segundo)
      
        date_start = datetime.strptime(date_start,'%d/%m/%Y %H:%M:%S').strftime("%Y-%m-%d %H:%M:%S")
        date_completion = datetime.strptime(date_completion,'%d/%m/%Y %H:%M:%S').strftime("%Y-%m-%d %H:%M:%S")

        # chamando funcao de automacao que só aceita datas de hoje para frente

        date_start_ja_passou = data_ja_passou(date_start)
        date_completion_ja_passou = data_ja_passou(date_completion)

        # se deu tudo certo(datas  validas)
        if date_start_ja_passou == False and date_completion_ja_passou == False:

            if form_tarefas.is_valid():
                # pegando usuario que fez a anotação  
                user = get_object_or_404(User, pk = request.user.id)
                # se estiver vazio é pq no campo select o usuario não selecionou nenhum grupo 
                if grupo.strip() == "" :
                    objeto_grupo = None
    
                else:
                    # pegando o objeto do grupo 
                    objeto_grupo= get_object_or_404(Grupo, pk=grupo)
                
                
                tarefa = Tarefas.objects.create(title = titulo, body = mensagem , fk_pessoa = user, fk_grupo = objeto_grupo, date_start = date_start, date_completion = date_completion)
                
                # fazendo o insert 


                tarefa.save()

                return redirect('listar_tarefas')
            
            # se o formulario não for valido

            else:
                return render(request,'form_tarefas.html',contexto)
        

        elif date_start_ja_passou == True and date_completion_ja_passou == True:
            messages.error(request, 'data de conclusao e início inválidas: o dia ou a hora do dia já passou')
            return render(request,'form_tarefas.html',contexto)

        
        elif date_start_ja_passou == True:
            messages.error(request, 'data de início inválida: o dia ou a  hora do dia já passou')
            return render(request,'form_tarefas.html',contexto)

        
        elif date_completion_ja_passou == True:
            messages.error(request, 'data de conclusao inválida: o dia ou a hora do dia já passou')
            return render(request,'form_tarefas.html',contexto)
        
      
            

    else:
        return render(request,'form_tarefas.html',contexto)
        


# para acessar esta pagina, o usuario deve estar logado
@login_required
def listar_tarefas(request):
    # listando grupos do usuario via select pelo seu 
    tarefas = Tarefas.objects.filter(fk_pessoa_id = request.user.id)
    #dicionario com as tarefas  para o  template 

    dados = {
        'tarefas': tarefas
    
    }
    
    return render(request,'listar_tarefas.html',dados) 


def deletar_tarefa(request,tarefa_id): 

    if request.method == 'GET':
        print('TESTTANDO ')
        # pega a receita pelo id do parametro funcao 
        tarefas = get_object_or_404(Tarefas,pk = tarefa_id)
        tarefas.delete()
        # redirecionando para a pagina de listar tarefa
        return redirect('listar_tarefas')
    else: 
      # redirecionando para a dashboard
      return redirect('dashboard') 



# manda para pagina de formulario de editar 
# para acessar esta pagina, o usuario deve estar logado
@login_required
def editar_tarefa(request, id_editar_tarefa):

    if request.method == 'GET' and  id_editar_tarefa:

        # pega todos os da anotação pelo id dela 
        tarefa_edit = Tarefas.objects.get(id = id_editar_tarefa)
     
     
     
        # pegando o grupo atual do usuario 
        grupo_edit = tarefa_edit.fk_grupo
        # pegando os grupos que pertence à ele, caso ele queira mudar 
        valores_grupos_editar = Grupo.objects.filter(fk_pessoa_id = request.user.id)
        form = FormTarefas(instance= tarefa_edit) # coloca valores no formulario 
        contexto = None; 
        if grupo_edit is None:
            # não passo a grupo grupo_edit para o template senão dará erro 
            contexto= {'form_tarefa':form,'id_tarefa':id_editar_tarefa,'valores_grupos_editar':valores_grupos_editar}

        # é pq tem grupo na anotação 
        else:
            valores_grupos_editar = valores_grupos_editar.exclude(id = grupo_edit.id)
            contexto= {'form_tarefa':form,'id_tarefa':id_editar_tarefa,'grupo_edit':grupo_edit,'valores_grupos_editar':valores_grupos_editar}
    

    

        return render(request,'editar_tarefa.html',contexto)
    
    else:
        return redirect('dashboard')



# atualiza a tarefa em si 


def atualizar_tarefa(request):
    if request.method == 'POST':
        # pegando o id da tarefa
        tarefa_id = request.POST['id_tarefa'] 
        form_tarefa_edit = FormTarefas(request.POST)
        # pegando dados da data
        date_start_edit = request.POST['date_start']
        date_completion_edit = request.POST['date_completion']
        # formatando as datas para o formato datetime que  o banco de dados aceita: YYYY-MM-DD H:M:S  (ano-mes-dia Hora:Minuto:Segundo)
        date_start_edit = datetime.strptime(date_start_edit,'%d/%m/%Y %H:%M:%S').strftime("%Y-%m-%d %H:%M:%S")
        date_completion_edit = datetime.strptime(date_completion_edit,'%d/%m/%Y %H:%M:%S').strftime("%Y-%m-%d %H:%M:%S")
        # criando contexto com id do usuario ,pois se acontecer um erro no formulario, a pagina será recarregada e o campo id  estará com valor nulo 

        contexto ={
            'form_tarefa' : form_tarefa_edit,
            'id_tarefa' : tarefa_id
        }

        # chamando funcao de automacao que só aceita datas de hoje para frente

        date_start_ja_passou = data_ja_passou(date_start_edit)
        date_completion_ja_passou = data_ja_passou(date_completion_edit)
          # se deu tudo certo(datas  validas)
        if date_start_ja_passou == False and date_completion_ja_passou == False:
            if form_tarefa_edit.is_valid():
            
                # pegando o id da tarefa no banco de dados
                # pk = primary key 
                tarefa_update = Tarefas.objects.get(pk = tarefa_id)

                # alterando os dados
                tarefa_update.title = request.POST['title']
                tarefa_update.body = request.POST['body']
                tarefa_update.date_start = date_start_edit
                tarefa_update.date_completion = date_completion_edit
            # tarefa_update.status = request.POST['status']
                tarefa_update.fk_grupo_id = request.POST['fk_grupo_edit']
                

                # atualizando a tarefa

                # se deu tudo certo 
                tarefa_update.save()
                return redirect('listar_tarefas')
            
            else:
                tarefa_id = tarefa_id
                return render(request,'editar_tarefa.html',contexto)

                
        elif date_start_ja_passou == True and date_completion_ja_passou == True:
            messages.error(request, 'data de conclusao e início inválidas: o dia ou a hora do dia já passou')
            return render(request,'form_tarefas.html',contexto)

        
        elif date_start_ja_passou == True:
            messages.error(request, 'data de início inválida: o dia ou a  hora do dia já passou')
            return render(request,'form_tarefas.html',contexto)

        
        elif date_completion_ja_passou == True:
            messages.error(request, 'data de conclusao inválida: o dia ou a hora do dia já passou')
            return render(request,'form_tarefas.html',contexto)
        

    else:
        return redirect('dashboard') 




# atualiza a data da tarefa e o status 

def concluir_tarefa(request,tarefa_id):
    # se o usuario clicou no link de concluir tarefa 
    if request.method == 'GET':
        concluir_tarefa_id = tarefa_id
        # pegando o id da tarefa no banco de dados
        # pk = primary key 
        concluir_tarefa_update = Tarefas.objects.get(pk = concluir_tarefa_id)
        concluir_tarefa_update.status='concluída'
        # pega a data com horas de agora 
        concluir_tarefa_update.date_conclusao = datetime.now()

        # atualizando os campos da tarefa
        concluir_tarefa_update.save()

        # redireciona para á pagina de listar tarefas
        return redirect('listar_tarefas')


    # senão manda para a dashboard de volta
    else:
        return redirect('dashboard')


def buscar_tarefa(request):
        # se o campo pesquisar tarefa tem um valor 
        if 'pesquisar_tarefa' in request.GET:
            tarefa_pesquisada = request.GET['pesquisar_tarefa']
   
            # filtrando pesquisa pelo id do usuario 
         
            # pesquisando a tarefa pelo titulo
            pesquisar_tarefa =  Tarefas.objects.filter(title__icontains = tarefa_pesquisada, fk_pessoa= request.user.id)
            # se não retornou nada pelo campo titulo tenta pelo body 
            if pesquisar_tarefa.count() == 0:
                pesquisar_tarefa =  Tarefas.objects.filter(body__icontains = tarefa_pesquisada, fk_pessoa= request.user.id)
           
           
           
           
            dados = {
            'resultado_tarefa_pesquisa': pesquisar_tarefa
            }
            return render(request,'buscar_tarefa.html',dados)
        
        else:
            return redirect('dashboard')

def  data_ja_passou(data):
    '''
     verifica se a data informada já passou e retorna true ou false 
    '''

    hoje = datetime.now()
    # removendo os milisegundos do datetime.now() para comparar com o parametro data
    #YYYY-MM-DD H:M:S  (ano-mes-dia Hora:Minuto:Segundo)
    hoje = hoje.strftime("%Y-%m-%d %H:%M:%S")
    if data < hoje:
        return True
    
    # datas exatamente iguais, mesmo horas, segundos e minutos
    elif data == hoje:
        return False

    else:
        return False



      
      
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
       
 
 
 
 

  
 
 
 
 
  
 

 

 
 