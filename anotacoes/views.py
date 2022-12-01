from django.shortcuts import render,redirect,get_object_or_404

from anotacoes.forms import FormAnotacoes

# importando model de anotacoes

from anotacoes.models import Anotacoes

from django.contrib import messages

# importando model de user 

from django.contrib.auth.models import User


# importando model de anotacoes 
from anotacoes.models import Anotacoes

# importando model de grupos 

from grupos.models import Grupo

from django.contrib.auth.decorators import login_required


# Create your views here.


# manda para a pagina de  formulário 

# para acessar esta pagina, o usuario deverá estar logado 
@login_required
def form_anotacoes(request):
     # pegando o grupo pelo id do usuario 
     valores_grupos = Grupo.objects.filter(fk_pessoa_id = request.user.id)
   
    
     # chamando formulario 
     form_anotacoes = FormAnotacoes()
     contexto = {'form_anotacoes':form_anotacoes,'grupo':valores_grupos}
     return render(request,'form_anotacoes.html',contexto)


# faz o insert das anotações 
def insert_anotacoes(request):
     # se o usuario clicou no post 

     if request.method ==  'POST': 
          # pegando os dados do formulario
          form_anotacoes = FormAnotacoes(request.POST) 
          contexto = {'form_anotacoes':form_anotacoes}
          
          titulo = request.POST['title']
          mensagem = request.POST['body']
          grupo = request.POST['fk_grupo']
          
          
          if form_anotacoes.is_valid():
                # pegando usuario que fez a anotação  
               user = get_object_or_404(User, pk = request.user.id)
               # se estiver vazio é pq no campo select o usuario não selecionou nenhum grupo 
               if grupo.strip() == "" :
                  objeto_grupo = None
               
               else:
                    # pegando o objeto do grupo 
                    objeto_grupo= get_object_or_404(Grupo, pk=grupo)
              
               # grupo = get_object_or_404(Grupo, pk = grupo)
              
              
               anotacoes = Anotacoes.objects.create(title = titulo, body = mensagem,fk_pessoa = user,fk_grupo= objeto_grupo)
               anotacoes.save()
               return redirect('dashboard')
          
          else:
               return render(request,'form_anotacoes.html',contexto)
          
               
          return render(request,'dashboard.html')
     
     # se o usuario tentar acessar esse metodo sem clicar no enviar formulario 

     # o redireciona para a página do formulario
     else:
          return redirect('form_anotacoes')
     

def deleta_anotação(request,anotacao_id):
     if request.method == 'GET':
          # pega a receita pelo id do parametro funcao 
      anotacao = get_object_or_404(Anotacoes,pk = anotacao_id)
      anotacao.delete()
      # redirecionando para a dashboard
      return redirect('dashboard')


     else: 
          # redirecionando para a dashboard
          return redirect('dashboard') 



# view que manda para  pagina de  formulario de editar anotação 
# para acessar esta pagina, o usuario deverá estar logado 
@login_required
def editar_anotação(request, editar_anotacao_id):

    # pega todos os da anotação pelo id dela 
     anotacao_edit = Anotacoes.objects.get(id = editar_anotacao_id)
     # pegando o grupo atual do usuario 
     grupo_edit = anotacao_edit.fk_grupo
     # pegando os grupos que pertence à ele, caso ele queira mudar 
     valores_grupos_editar = Grupo.objects.filter(fk_pessoa_id = request.user.id)
     form = FormAnotacoes(instance= anotacao_edit) # coloca valores no formulario 
     contexto = None; 
     if grupo_edit is None:
         # não passo a grupo grupo_edit para o template senão dará erro 
          contexto= {'form_anotacoes_atualizar':form,'id_anotacao':editar_anotacao_id,'valores_grupos_editar':valores_grupos_editar}
     
     # é pq tem grupo na anotação 
     else:
          valores_grupos_editar = valores_grupos_editar.exclude(id = grupo_edit.id)
          contexto= {'form_anotacoes_atualizar':form,'id_anotacao':editar_anotacao_id,'grupo_edit':grupo_edit,'valores_grupos_editar':valores_grupos_editar}       
     return render(request,'editar_anotacoes.html',contexto)


# metodo de atualizar anotação 
def atualizar_anotacao(request):
     if request.method == 'POST':
          # pegando o id da anotação 
          anotacao_id = request.POST['id_anotacao']
          form_anotacoes_atualizar = FormAnotacoes(request.POST)
          # pois se acontecer um erro no formulario, a pagina será recarregada e o campo id estará com valor nulo 
          contexto = {'form_anotacoes_atualizar':form_anotacoes_atualizar,'id_anotacao':anotacao_id}
          if form_anotacoes_atualizar.is_valid():
               # pegando anotacao no banco de dados via id 
               # pk = primary key 
               anotacao_update = Anotacoes.objects.get(pk = anotacao_id)

               # alterando os dados 

               anotacao_update.title = request.POST['title']
               anotacao_update.body = request.POST['body']
               anotacao_update.fk_grupo_id = request.POST['fk_grupo_edit']
               

               # atualizando a anotação 
               anotacao_update.save()
                
               
             
             
               return redirect('dashboard') 
          
          else:
               anotacao_id = anotacao_id
               return render(request,'editar_anotacoes.html',contexto)

          

     else :
          return redirect('dashboard')   


# metodo que lista as anotações do usuario e retorna as anotações, onde chamo essa função no metodo logar da view do usuario   

def listar_anotacoes(id_usuario):
     '''
          funcao que lista todas as anotações do usuario e retorna as anotações
          id_usuario: id do usuario logado 
          
     '''
    
     id = id_usuario
     # guardando anotacoes do usuario via select pelo seu id 
     anotacoes = Anotacoes.objects.filter(fk_pessoa_id = id)
     # dicionario com as anotacoes 
     dados = {
          'anotacoes' : anotacoes
     }
     return dados 


# funcao que lista todas as anotações de acordo com fk_grupo e retorna elas

def anotacoes_por_grupo(fk_grupo):
     anotacoes_grupo= Anotacoes.objects.filter(fk_grupo_id = fk_grupo)
     return anotacoes_grupo



def buscar(request):
     # se o campo pesquisar anotação tem um valor 
     if 'pesquisar_anotacao' in request.GET:
          anotacao_pesquisada = request.GET['pesquisar_anotacao']
       
          # filtrando pesquisa pelo id do usuario 
             
          # pesquisando a anotação pelo titulo
          pesquisar_anotacao =  Anotacoes.objects.filter(title__icontains = anotacao_pesquisada, fk_pessoa= request.user.id)

          # se não retornou nada pelo cmapo titulo tenta pelo body 
          if pesquisar_anotacao.count() == 0:
               pesquisar_anotacao =  Anotacoes.objects.filter(body__icontains = anotacao_pesquisada, fk_pessoa= request.user.id)
               
               
               
               

          dados = {
               'resultado_pesquisa': pesquisar_anotacao
          }
          return render(request,'buscar_anotacao.html',dados)
     
     else:
          return redirect('dashboard')



 
    
    

   

   
    
          

   
   
   