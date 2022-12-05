from unicodedata import name
from django.urls import path

from . import views

urlpatterns = [
    # rotas 
    # index 
    path('',views.index, name="index"),
    # faz o método de logar
    path('logar',views.logar, name="logar"),
    # pagina do formulario de cadastrar 
    path('cadastrar',views.cadastrar,name="cadastrar"),
    # rota que faz o insert do usuario 
    path('insertUsuario',views.insertUsuario, name='insertUsuario'),
    path('dashboard',views.dashboard,name='dashboard'),
    # logout
    path('logout',views.logout, name='logout'),
    # manda para à pagina de deletar usuario
    path('pagina_deletar_usuario', views.pagina_deletar_usuario, name="pagina_deletar_usuario"),
    # formulario de deletar conta
    path('deletar_conta/',views.deletar_conta, name="deletar_conta"),
    # manda para página de alterar usuario
    path('pagina_alterar_usuario',views.pagina_alterar_usuario, name="pagina_alterar_usuario"),
    # edita os dados do usuario
    path('update_usuario', views.update_usuario, name='update_usuario'),
    # pagina de alterar senha
    path('pagina_alterar_senha',views.pagina_alterar_senha, name='pagina_alterar_senha'),
    # atualiza a senha em si 
    path('atualizar_senha',views.atualizar_senha, name='atualizar_senha')
   

]