#importa urls do django, views anotacoes

from django.urls import path

#importando todas as views

from . import views


#definindo urls 

#rotas
urlpatterns = [
    #index da view de nome index
    path('form_tarefas', views.form_tarefas, name='form_tarefas'),
    # rota que manda os dados para o formulario 
    path('criar_tarefa',views.insert_tarefa, name='insert_tarefa'),
    path('listar_tarefas',views.listar_tarefas, name= 'listar_tarefas'),
    # rota com parametro do tipo inteiro
    path('deletar_tarefa/<int:tarefa_id>',views.deletar_tarefa, name='deletar_tarefa'),
    # rota para mandar para á pagina de editar tarefa
    path('editar_tarefa/<int:id_editar_tarefa>',views.editar_tarefa, name='editar_tarefa'),
    path('atualizar_tarefa',views.atualizar_tarefa, name="atualizar_tarefa"),
    # rota que conclui a tarefa
    path('concluir_tarefa/<int:tarefa_id>',views.concluir_tarefa, name="concluir_tarefa"),
    #rota que faz a pesquisa da tarefa
    path('buscar_tarefa', views.buscar_tarefa, name='buscar_tarefa')
    
]