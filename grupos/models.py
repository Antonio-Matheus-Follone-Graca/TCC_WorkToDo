from email.policy import default
from django.db import models

# importando da model  User do django

from django.contrib.auth.models import User

# Create your models here.

class Grupo(models.Model):
    title = models.CharField(max_length = 200, blank= False, null=False) # deve ter um valor 
    description = models.CharField(max_length = 200, blank = True)
    color = models.CharField(max_length = 200, blank = True, default= '#808080') 
    fk_pessoa = models.ForeignKey(User, on_delete = models.CASCADE, null = True, blank= True) # pode ser o username da pessoa ou id, tanto faz 

  
  
   
   

