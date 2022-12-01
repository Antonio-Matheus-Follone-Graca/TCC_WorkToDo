
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    # index
    # incluindo na index as urls do app usuarios
    path('',include('usuarios.urls')),
    path('anotacoes/',include('anotacoes.urls')),
    path('grupo/', include('grupos.urls')),
    path('tarefa/',include('tarefas.urls')),
    path('admin/', admin.site.urls),

]
