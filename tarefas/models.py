from tokenize import blank_re
from django.db import models

# importando da model  User do django

from django.contrib.auth.models import User

from grupos.models import Grupo

from datetime import datetime

# Create your models here.

class Tarefas(models.Model):
    title = models.CharField(max_length=200,blank=False) # campo obrigatorio 
    body = models.TextField(blank=True) # campo pode ser vazio 
    date_start = models.DateTimeField(blank=False)
    date_completion = models.DateTimeField(blank=False ) # data maxima para concluir a tarefa
    date_conclusao= models.DateTimeField(blank = True, null = True)  # data que a tarefa foi concluisa
    status = models.CharField(blank= True, null = True, max_length = 200,default='pendente')
    date= models.DateField(default=datetime.now,blank=True)
    fk_pessoa = models.ForeignKey(User, on_delete = models.CASCADE, blank= True) # pode ser o username da pessoa ou id, tanto faz 
    fk_grupo = models.ForeignKey(Grupo, on_delete = models.CASCADE, null= True, blank=True ) # o grupo pode ser vazio(null) no banco de dados e blank true para vazio
    


   
   

  

  