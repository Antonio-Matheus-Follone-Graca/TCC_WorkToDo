from multiprocessing import context
from django.shortcuts import render,get_object_or_404

from django.shortcuts import render, redirect


# importando formulario 

from grupos.forms import FormGrupos

# importando model grupos

from grupos.models import Grupo


# importando funcao de Anotacoes 

from anotacoes.views import anotacoes_por_grupo

from django.contrib.auth.decorators import login_required

# Create your views here.

# view que manda para à pagina de  formulario de criar grupo
# para acessar esta pagina, o usuario deve estar logado
@login_required
def form_criar_grupo(request):
   # formulario 
    form_grupo = FormGrupos()  
    contexto = {'form_grupo_insert':form_grupo}
    return render(request,'form_criarGrupo.html',contexto)


def insert_grupo(request):
    # se o usuario clicou no enviar formulario 
    if request.method == 'POST':
        # pegando o id do usuario atraves do request.user.id, pois é uma variavel super global
        id_usuario = request.user.id
        # pegando a classe do formulario
        form_criar_grupo= FormGrupos(request.POST)
        contexto = {'form_grupo_insert':form_criar_grupo}
        # pegando dados do formulario e colocando em variaveis
        titulo_grupo = request.POST['title']
        descricao_grupo = request.POST['description']
        cor_grupo = request.POST['color']
        # se o formulario for valido
        if form_criar_grupo.is_valid():
            # faz  cadastro de grupo  
            grupo =  Grupo.objects.create(title = titulo_grupo, description = descricao_grupo, color = cor_grupo, fk_pessoa_id= id_usuario )
            # cadastrando 
            grupo.save()

            # redirecionando para pagina  de listar grupos
            return redirect('listar_grupos')
             


        # se o formulario não for valido 
        else:
            return render(request,'form_criarGrupo.html',contexto)
        


    else:
        return redirect('form_criar_grupo')

# para acessar esta pagina, o usuario deve estar logado
@login_required
def listar_grupos(request):
    # pegando id do usuario 
    id_usuario = request.user.id 

    # listando grupos do usuario via select pelo seu id
    grupos = Grupo.objects.filter(fk_pessoa_id = id_usuario)

   

    # pegando os numeros de anotações cadastradas 

    # chamando funcoes de listar anotacoes 
  
    

    #dicionario com grupos para o  template 
    dados = {
        'grupos': grupos,

    }
    return render(request,'listar_grupos.html',dados)


# mostra a pagina de deletar grupo, onde terão duas opcoes, deletar com todas anotações e tarefas o grupo, ou apenas deletar o grupo

# manda para a pagina de deletar 

# para acessar esta pagina, o usuario deve estar logado
@login_required
def pagina_deletar_grupo(request,grupo_id):
    if request.method == 'GET':
        # pegando dados do grupo a ser deletado 
        grupo_deletar = Grupo.objects.filter(id= grupo_id)
        contexto = {
            'grupo_deletar':grupo_deletar
        }
        return render(request,'excluir_grupo.html',contexto)


    else:
        return redirect('listar_grupo')


# parametro id e tipo foram definidos no urls.py do app grupos
def apagar_grupo(request,grupo_id_deletar,tipo):
   
    
    # se clicou no link 
    if request.method == 'GET':
        grupo_deletar = get_object_or_404(Grupo,pk = grupo_id_deletar)
        # caso o usuario altera o valor tipo no inspecionar elemento
        if tipo != 'deletar_tudo' and tipo != 'deletar_apenas_grupo':
            return redirect('dashboard')
        
        else:
            # chama a funcao de listar anotacoes da views.py do app anotacoes  por grupo e em seguida atualiza o fk grupo de anotações para nulo
            valor = anotacoes_por_grupo(grupo_id_deletar)
            
            # OBSERVACOES: 

            # como não há problemas nos codigos abaixo de deletar anotação ou tarefa com grupos vazio, não há a necessidade de fazer o codigo de validação

            # FIM OBSERVACOES
           
            # de acordo com o tipo de deleção 
            
            # se for apenas grupo faz um update das chaves estrangeiras para null, para em seguida poder deletar o grupo 
            if tipo.strip() == 'deletar_apenas_grupo':
                # filtrando as anotações que tenham o id do grupo que quero deletar e setando para null

                # pois tenho que fazer isso para depois deletar o grupo 

                
               
                # atualizando o campo fk grupo de anotações para nulo
                valor.update(fk_grupo_id = None)
                # agora deletando os grupos
                
                grupo_deletar.delete()
            
            elif tipo.strip() == 'deletar_tudo':
              # deletando anotacoes
              valor.delete()
              # deletando grupo
              grupo_deletar.delete()

        # manda para á pagina de listar grupo 
        return redirect('listar_grupos')
    
    else:
        return redirect('dashboard')


# manda para o formulário de editar grupo 
# para acessar esta pagina, o usuario deve estar logado
@login_required
def pagina_editar_grupo(request,grupo_id_editar): 
    if request.method =='GET':
        # pegando os dados do grupo pelo id 
        grupo_edit = Grupo.objects.get(id = grupo_id_editar)
        # passando esses dados para o formulario 
        form_grupo = FormGrupos(instance = grupo_edit )  
        contexto = {
            'form_grupo_edit':form_grupo,
            'id_grupo':grupo_id_editar
        }
        return render(request, 'form_editar_grupo.html', contexto)
    else: 
        return redirect('listar_grupos')



# faz o update de
def atualizar_grupo(request):
    # se o usuario clicou no enviar formulario 
    if request.method == 'POST':
        id_grupo = request.POST['id_grupo_edit'] 
        form_grupo = FormGrupos(request.POST)
        # pois se acontecer um erro no formulario, a pagina será recarregada e mostrara o erro 
        contexto = {
            'form_grupo_edit':form_grupo,
            'id_grupo':id_grupo
        }

        if form_grupo.is_valid():
            # pegando anotação no banco de dados via id 
            # pk primary key 
            grupo_update = Grupo.objects.get(pk = id_grupo)
            grupo_update.title = request.POST['title']
            grupo_update.description = request.POST['description']
            grupo_update.color = request.POST['color']

            # atualizando o grupo 

            grupo_update.save()

            return redirect('listar_grupos')
        
        else:
            id_grupo = id_grupo
            return render(request,'form_editar_grupo.html',contexto)
            


    else:
        return redirect('listar_grupos')


def buscar_grupo(request):
    if 'pesquisar_grupo' in request.GET:
        grupo_pesquisado = request.GET['pesquisar_grupo']
        # filtrando pesquisa pelo id do usuario
        # pesquisando a tarefa pelo titulo

        pesquisar_grupo = Grupo.objects.filter(title__icontains = grupo_pesquisado, fk_pessoa= request.user.id)
        # senão retornou nada pelo campo titulo tenta pelo description

        if pesquisar_grupo.count() == 0:
            pesquisar_grupo = Grupo.objects.filter(description__icontains = grupo_pesquisado, fk_pessoa= request.user.id)
            
        dados = {
               'resultado_pesquisa_grupo': pesquisar_grupo
            }
        
        return render(request,'buscar_grupo.html',dados)
    
    else:
        return redirect('dashboard')


    
        