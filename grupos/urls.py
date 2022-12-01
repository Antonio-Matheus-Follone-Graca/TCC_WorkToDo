#importa urls do django, views grupo 

from django.urls import path

# importando todas as views

from . import views

# definindo urls 

# rotas

urlpatterns = [
    # rota para criar grupo 
    path('form_criar_grupo', views.form_criar_grupo, name = 'form_criar_grupo'),
    path('insert_grupo',views.insert_grupo, name='insert_grupo'),
    # rota que lista os grupos
    path('listar_grupo',views.listar_grupos, name='listar_grupos'),
    #rota de mostrar grupo antes do usuario deleta-lo
    path('deletar_grupo/<int:grupo_id>',views.pagina_deletar_grupo, name ='pagina_deletar_grupo'),
    #rota que deleta o grupo 
    path('apagar_grupo/<int:grupo_id_deletar>/<str:tipo>',views.apagar_grupo, name='apagar_grupo'),
    # rota para mandar para o formulario de editar grupo
    path('pagina_editar_grupo/<int:grupo_id_editar>', views.pagina_editar_grupo, name= 'pagina_editar_grupo'),
    # rota que faz o update 
    path('atualizar_grupo',views.atualizar_grupo, name='atualizar_grupo'),
    path('buscar_grupo', views.buscar_grupo, name='buscar_grupo')
]
