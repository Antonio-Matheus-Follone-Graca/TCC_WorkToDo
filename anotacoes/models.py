from django.db import models

# importando da model  User do django

from django.contrib.auth.models import User

from grupos.models import Grupo

from datetime import datetime

# Create your models here.

class Anotacoes(models.Model):
    title = models.CharField(max_length=200,blank=False) # campo obrigatorio 
    body = models.TextField(blank=True) # campo pode ser vazio 
    fk_pessoa = models.ForeignKey(User, on_delete = models.CASCADE, blank= True) # pode ser o username da pessoa ou id, tanto faz 
    fk_grupo = models.ForeignKey(Grupo, on_delete = models.CASCADE, null= True, blank=True ) # o grupo pode ser vazio(null) no banco de dados e blank true para vazio
    date= models.DateField(default=datetime.now,blank=True)


   
   

  

  