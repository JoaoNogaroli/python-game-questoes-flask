from distutils.log import error
from flask import Flask, request, render_template, redirect, url_for,session
from cliente_app import conexao_cliente_primeira_msg
from modelo_db import connection_db
from modelo_pusher import connection_pusher
import psycopg2
import time
import pusher

 
pusher_client = pusher.Pusher(
    app_id='1468023',
    key='3eef3f7cf3be6643b599',
    secret='3abd13233fdb05a859ce',
    cluster='sa1',
    ssl=True
    )

app = Flask(__name__)


app.config['SECRET_KEY'] = 'testesecret'

@app.route('/')
def index():

    return render_template('index.html', url_for=url_for)

@app.route('/enviar_nome', methods=['POST'])
def enviar_nome():

    nome = request.form['nome']
    nome = nome.strip()
    
    try:
        connection_db().insert_user(nome)
        #session['msg_from'] = nome

    except Exception as e:
        #session['msg_from'] = nome
        # print(e)
        # print("Não inserido --")
        # msg_true = True
        # msg = 'Usuário já cadastrado'

        # return render_template('index.html', url_for=url_for,msg=msg,msg_true=msg_true)
        pass
    lista_client = []


    lista = ['0',
    'adm_geral',
    'Questão 1:',
    ' Liderança',
    'O Jornal O Estado de São Paulo publicou reportagem denominada “De Nobel da Paz a líder de guerra, Abiy Ahmed encara eleição na Etiópia”, em que discutia como o primeiro-ministro do país africano enfrenta a vontade das urnas pela primeira vez, desde que chegou ao cargo, em um processo eleitoral bastante questionado a partir do seguinte quadro:\n“Mesmo a votação desta segunda-feira, antes anunciada como a primeira eleição livre do país, e uma chance de virar a página em décadas de governos autocráticos, apenas reforçou as divisões internas e alimentou advertências sombrias de que o futuro da Etiópia está em dúvida.”\n  (O Estado de São Paulo. “De Nobel da Paz a líder de guerra, Abiy Ahmed encara eleição na Etiópia”. Internacional, São Paulo, ano 2021. Disponível em: https://internacional.estadao.com.br/noticias/geral)\n  No contexto desta publicação, a liderança de governos autocráticos é caracterizada por',
    ' a)  busca da popularidade com os liderados.\n b)  divisão dos poderes de decisão entre chefe e grupo.\n c)  delegação do poder de decisão ao grupo.\n d)  abuso de autoridade e delegação de poder.\n e)  centralização de poder de decisão no chefe.',
    'E']

    lista = [s.replace('\n', '<br>') for s in lista]
    #print(lista)
    import pickle

    data=pickle.dumps(lista)
    msg_recebida = pickle.loads(data)

    msg = msg_recebida
    msg[4] = msg[4].replace('<br>',' ')
    #print(msg[4])'
    msg[5] = msg[5].split('<br>')

    userid = connection_db().gel_userid(nome)
    total_users = connection_db().get_all_users_minus(userid)
    print(total_users)

    return render_template('teste.html', nome=nome, msg=msg, total_users=total_users, len=len,userid=userid[0][0])


# @app.route('/set_conversa', methods=['POST'])
# def set_conversa():

#     msg_from =  request.form['msg_from']
#     msg_from_i = int(connection_db().gel_userid(msg_from)[0][0])
#     print(msg_from)

#     msg_to = request.form['msg_to']
#     msg_to_i =int(connection_db().gel_userid(msg_to)[0][0])
#     session['msg_to'] = msg_to

#     if msg_from_i < msg_to_i:
#         evento = f'{msg_from_i}_evento_{msg_to_i}'
#     else:
#         evento = f'{msg_to_i}_evento_{msg_from_i}'


#     dicio = {'evento':evento,'name_from':msg_from,'name_from_i':msg_from_i,'name_to:':msg_to,'name_to_i':msg_to_i}
    
#     # try:
#     #     connection_pusher(evento,dicio)

#     #     return dicio
#     # except Exception as e:
#     #     print(e)
#     #     return 'fail'
#     return dicio

@app.route('/chat_client', methods = ['POST'])
def chat_client():

    
    msg_from = request.form['msg_from']
    msg_from_i = int(request.form['msg_from_i'])
    msg_to = request.form['msg_to']
    msg_to_i =int(request.form['msg_to_i'])

    message = request.form['message']
    momento = request.form['momento']

    #evento = request.form['evento']

    if msg_from_i < msg_to_i:
        evento = f'{msg_from_i}_evento_{msg_to_i}'
    else:
        evento = f'{msg_to_i}_evento_{msg_from_i}'

    dicio =  {
        'msg_from':msg_from,
        'msg_from_i':msg_from_i,
        'msg_to':msg_to,
        'msg_to_i':msg_to_i,
        'evento':evento,
        'message':message,
        'momento':momento}
    #return {'evento':dicio['evento'], 'message':dicio['message']}

    
    try:
        connection_pusher(evento,dicio)

        return 'mensagem_enviada'

    except Exception as e:
        print(e)
        return 'fail'

    # return dicio
    # evento = 

if __name__ == "__main__":
    app.run()