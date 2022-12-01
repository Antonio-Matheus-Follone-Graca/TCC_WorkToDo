#importa urls do django, views anotacoes

from django.urls import path

#importando todas as views

from . import views


#definindo urls 

#rotas
urlpatterns = [
    #index da view de nome index
    path('anotacoes/form_anotacoes', views.form_anotacoes, name='form_anotacoes'),
    path('anotacoes/insert_anotacoes',views.insert_anotacoes, name='insert_anotacoes'),
    # deleta anotação  com parametro do tipo inteiro 
    path('deleta/<int:anotacao_id>',views.deleta_anotação, name ='deleta_anotação'),
    # rota  editar anotacao com parametro do tipo inteiro, redireciona para o formulario 
    path('edita/<int:editar_anotacao_id>',views.editar_anotação, name='editar_anotacao'),
    # atualiza o formulario em si 
    path('atualiza_anotacao',views.atualizar_anotacao, name ='atualizar_anotacao'),
    # view de buscar 
    path('buscar',views.buscar, name='buscar')
    
]