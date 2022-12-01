from datetime import datetime, date

def campo_tem_numero(valor_campo, nome_campo, lista_de_erros):
    """
        verifica se o campo possui algum número
    """
    if any(char.isdigit() for char in valor_campo):
        lista_de_erros[nome_campo] = 'Não inclua números neste campo'


def data_inicio_maior_que_data_conclusao(data_inicio, data_conclusao,lista_de_erros):
    """
        verifica as datas 
    """
    if data_inicio > data_conclusao :
        lista_de_erros['date_start'] = 'data de inicio maior que a data de conclusão'


def data_menor_data_atual(data,nome_campo,lista_de_erros):
    """
        verifica as datas 
    """
    data_atual = datetime.now() 
    if data < data_atual :
        lista_de_erros[nome_campo] = 'data invalida: o dia ou hora do dia já passou '
    
   
    
   
   








