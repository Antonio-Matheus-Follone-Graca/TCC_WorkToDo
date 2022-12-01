import psycopg2
from email.message import EmailMessage
import ssl
import smtplib
# Função para criar conexão no banco-----------------------------------------------------------------------
def conecta_db():
    con = psycopg2.connect(host='localhost', database='tcc', user='postgres',  password='123456')
    return con
#----------------------------------------------------------------------------------------------------------
# Select para pegar o email do usuario---------------------------------------------------------------------
def user_get(id):
        print(id)
        consulta_sql = f" SELECT username,email FROM public.auth_user where id={id};"
        
        cursor.execute(consulta_sql)
        resultado_usuario = cursor.fetchall()

        return resultado_usuario
#----------------------------------------------------------------------------------------------------------
# Envia email----------------------------------------------------------------------------------------------
def SentEmail(sender, password, receiver, UserName, TaskName, TaskBody):
    print()

    email_sender = sender
    email_password = password
    email_receiver = receiver

    Subject = f'Olá, {UserName} a tarefa {TaskName} venceu!'
    Body    = f'Caro {UserName}, por favor, verifique a seguinte tarefa:\nTítulo: {TaskName}\nCorpo: {TaskBody}'

    em = EmailMessage()
    em['From']    = email_sender
    em['To']      = email_receiver
    em['Subject'] = Subject
    em.set_content(Body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())
#----------------------------------------------------------------------------------------------------------
email_sender = 'gabrielfollone27@gmail.com'
email_password = 'tsbqylktkwboejfq'
teste = conecta_db()
cursor = teste.cursor()
TTarefas = []
#----------------------------------------------------------------------------------------------------------
consulta_sql = f" SELECT * FROM public.tarefas_tarefas where  date_completion < (SELECT CURRENT_DATE)   and status != 'concluída'  ;"
cursor.execute(consulta_sql)
#----------------------------------------------------------------------------------------------------------
resultado  =  cursor.rowcount
campos = cursor.fetchall()
for tarefas in campos:
    #id tarefas[0]
    #Título tarefas[1]
    #Corpo tarefas[2]
    #fk_pessoa tarefas[8]
    id_usuario = tarefas[8]
    rodando =user_get(tarefas[8])
    print(rodando)
    UserName = rodando[0][0]
    UserMail = rodando[0][1]
    Sender = SentEmail(email_sender, email_password, UserMail, UserName, tarefas[1], tarefas[2])
