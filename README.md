# TCC_WorkToDo

## fork do meu projeto de tcc pela Universidade de Mogi das Cruzes(UMC) do curso Sistemas de informação de 2019-2022## 

O link original está aqui **<https://github.com/This-Is-NPC/WorkToDo>** 

## Tecnologias usadas:
  * Python e framework django 
  * Html
  * Css
  * Javascript
  * PostgreSql



## Instalando bibliotecas necessárias para o projeto rodar e rodando o projeto

1. Baixe o projeto e abra no cmd a pasta do projeto;
2. Crie uma venv com o comando python -m venv nome-venv;
3. Ative a venv digitando : nome-venv\Scripts\activate;
4. Importe as bibliotecas com pip install -r requirements.txt;
5. Crie um banco no pgadmin de nome tcc(ou caso queira mudar o banco de dados usado ou o nome do banco, vá respectivamente na pasta tcc do projeto em arquivos e abra o arquivo settings.py, linhas 86 e 88;
6. Digite a senha do seu banco de dados e username do seu banco  no arquivo settings.py da pasta tcc respectivamente nas linhas 89 e 90; 
7. Após isso ative a venv do projeto e rode python manage.py makemigrations e manage.py migrate; 
8. Com a venv ativada, digite no cmd: python manage.py runserver

