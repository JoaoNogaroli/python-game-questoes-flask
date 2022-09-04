from re import search
from tokenize import Number
from unicodedata import numeric
from flask import Flask, request, render_template, redirect, url_for,session
from cliente_app import conexao_cliente_primeira_msg
from modelo_db import connection_db
from modelo_pusher import connection_pusher
import psycopg2
import time
import pusher
from server.pegardado import pegardado2
from flask_paginate import Pagination, get_page_parameter
import pandas as pd
import ast


pusher_client = pusher.Pusher(
    app_id='1468023',
    key='3eef3f7cf3be6643b599',
    secret='3abd13233fdb05a859ce',
    cluster='sa1',
    ssl=True
    )

app = Flask(__name__)


app.config['SECRET_KEY'] = 'testesecret'

# @app.route('/')
# def index():
    
#     return render_template('index.html', url_for=url_for)

@app.route('/')
def index():

    return render_template('index.html',url_for=url_for)

@app.route('/perfil_page', methods=['POST'])
def perfil_page():

    nome = str(request.form['nome'])

    convites = connection_db().get_my_convites(nome)
    print(convites)
    print(len(convites))

    return render_template('/perfil_page.html',nome=nome, convites=convites)


@app.route('/go_to_pagina3_filtros', methods=['POST'])
def go_to_pagina3_filtros():

    nome_from = request.form['nome']
    # print('-----')
    # print(nome_from)

    try:
        connection_db().insert_user(nome_from)
        #session['msg_from'] = nome
        # print('[----Usuário inserido-----]')
    except Exception as e:
        #session['msg_from'] = nome
        # print(e)
        # print("Não inserido --")
        # msg_true = True
        # msg = 'Usuário já cadastrado'

        # return render_template('index.html', url_for=url_for,msg=msg,msg_true=msg_true)
        # print('[---Usuário já consta no BD]---')
        # print(e)
        pass

    try:    
        userid = connection_db().gel_userid(nome_from)
        # print('[---userid---]: ',userid)
    except:
        # print('[---Error em pegar o ID---]')
        pass
    try:
        total_users = connection_db().get_all_users_minus(userid)
        # print(total_users)
    except:
        # print('[---Error ao pegar a lista menos o atual]---')
        pass


    df = pegardado2()
    disciplinas = df['disciplina'].unique()

    
    userid = connection_db().gel_userid(nome_from)

    total_users = connection_db().get_all_users_minus(userid)
    # print(total_users)

    return render_template('page3-filtros.html',disciplinas=disciplinas,total_users=total_users,nome_from=nome_from)


@app.route('/disciplina_retornar_topico', methods=['POST'])
def disciplina_retornar_topico():
    dicio = pegardado2()
    try:
        disciplina = request.form['disciplina']
        print(disciplina)
        lista_assunto = dicio[dicio['disciplina']==disciplina]['assunto'].unique()
        
        
        return list(lista_assunto)
    except Exception as e:
        print(e)
        return 'fail'

# _------------------<><><><>

# @app.route('/enviar_nome', methods=['POST'])
# def enviar_nome():

#     nome = request.form['nome']
#     nome = nome.strip()
    
#     try:
#         connection_db().insert_user(nome)
#         #session['msg_from'] = nome
#         print('[----Usuário inserido-----]')
#     except Exception as e:
#         #session['msg_from'] = nome
#         # print(e)
#         # print("Não inserido --")
#         # msg_true = True
#         # msg = 'Usuário já cadastrado'

#         # return render_template('index.html', url_for=url_for,msg=msg,msg_true=msg_true)
#         print('[---Usuário já consta no BD]---')
#         print(e)
#     lista_client = []


#     lista = ['0',
#     'adm_geral',
#     'Questão 1:',
#     ' Liderança',
#     'O Jornal O Estado de São Paulo publicou reportagem denominada “De Nobel da Paz a líder de guerra, Abiy Ahmed encara eleição na Etiópia”, em que discutia como o primeiro-ministro do país africano enfrenta a vontade das urnas pela primeira vez, desde que chegou ao cargo, em um processo eleitoral bastante questionado a partir do seguinte quadro:\n“Mesmo a votação desta segunda-feira, antes anunciada como a primeira eleição livre do país, e uma chance de virar a página em décadas de governos autocráticos, apenas reforçou as divisões internas e alimentou advertências sombrias de que o futuro da Etiópia está em dúvida.”\n  (O Estado de São Paulo. “De Nobel da Paz a líder de guerra, Abiy Ahmed encara eleição na Etiópia”. Internacional, São Paulo, ano 2021. Disponível em: https://internacional.estadao.com.br/noticias/geral)\n  No contexto desta publicação, a liderança de governos autocráticos é caracterizada por',
#     ' a)  busca da popularidade com os liderados.\n b)  divisão dos poderes de decisão entre chefe e grupo.\n c)  delegação do poder de decisão ao grupo.\n d)  abuso de autoridade e delegação de poder.\n e)  centralização de poder de decisão no chefe.',
#     'E']

#     lista = [s.replace('\n', '<br>') for s in lista]
#     #print(lista)
#     import pickle

#     data=pickle.dumps(lista)
#     msg_recebida = pickle.loads(data)

#     msg = msg_recebida
#     msg[4] = msg[4].replace('<br>',' ')
#     #print(msg[4])'
#     msg[5] = msg[5].split('<br>')

#     try:    
#         userid = connection_db().gel_userid(nome)
#         print('[---userid---]: ',userid)
#     except:
#         print('[---Error em pegar o ID---]')

#     try:
#         total_users = connection_db().get_all_users_minus(userid)
#         print(total_users)
#     except:
#         print('[---Error ao pegar a lista menos o atual]---')

#     return render_template('teste.html', nome=nome, msg=msg, total_users=total_users, len=len,userid=userid[0][0])

# @app.route('/chat_client', methods = ['POST'])
# def chat_client():

    
#     msg_from = request.form['msg_from']
#     msg_from_i = int(request.form['msg_from_i'])
#     msg_to = request.form['msg_to']
#     msg_to_i =int(request.form['msg_to_i'])

#     message = request.form['message']
#     momento = request.form['momento']

#     #evento = request.form['evento']

#     if msg_from_i < msg_to_i:
#         evento = f'{msg_from_i}_evento_{msg_to_i}'
#     else:
#         evento = f'{msg_to_i}_evento_{msg_from_i}'

#     dicio =  {
#         'msg_from':msg_from,
#         'msg_from_i':msg_from_i,
#         'msg_to':msg_to,
#         'msg_to_i':msg_to_i,
#         'evento':evento,
#         'message':message,
#         'momento':momento}
#     #return {'evento':dicio['evento'], 'message':dicio['message']}

    
#     try:
#         connection_pusher(evento,dicio)

#         return 'mensagem_enviada'

#     except Exception as e:
#         print(e)
#         return 'fail'

@app.route('/link_questao', methods=['POST'])
def link_questao():

    disciplina = request.form['disciplina']
    topico = request.form['topico']
    quantidade = int(request.form['quantidade'])
    momento = request.form['momento']
    nome_from = request.form['nome_from']
    i_nome_from = connection_db().gel_userid(nome_from)
    print('-------')
    i_nome_from = int(i_nome_from[0][0])
    # i_nome_from
    nome_chat_to = request.form['nome_chat_to']
    i_nome_chat_to = int(request.form['i_nome_chat_to'])

    evento_chat = f'{i_nome_chat_to}_evento'

    # if i_nome_from < i_nome_chat_to:
    #     evento = f'{i_nome_from}_evento_{i_nome_chat_to}'
    # else:
    #     evento = f'{i_nome_chat_to}_evento_{i_nome_from}'

    # evento é nome_solicitante(nome_from) _evento_ nome_convidado (nome_chat_to)

    evento = f'{i_nome_from}_evento_{i_nome_chat_to}'


    # print(disciplina)
    # print(topico)
    # print(quantidade)
    print('---------------------------------------')
    df = pegardado2()

    df1 = df[df['disciplina']==str(disciplina)]
    # print(df1)
    df2 = df1[df1['assunto'].str.strip().replace(' ','')==str(topico)]

    try:
       df3 = df2.sample(quantidade)
       lista = df3.values.tolist()
    except Exception:
        df3 = df2
        lista = df3.values.tolist()


    topico = topico.strip().replace(' ','')

    lista_id_questoes = []

    for item in lista:
        id = item[0]
        # print(id)
        lista_id_questoes.append(id)
    print('[Lista id criada ----]')




    
    # link ='http://127.0.0.1:5000/'+disciplina+'/questao/'+topico+'/'+str(quantidade)+'/'+momento+'/_evento_/'+evento+'/_i_/'+str(i_nome_from)
    
    link ='https://projeto-questoes-chat-nixquest.herokuapp.com/'+disciplina+'/questao/'+topico+'/'+str(quantidade)+'/'+momento+'/_evento_/'+evento+'/_i_/'+str(i_nome_from)
    try:
        connection_db().insert_convite(evento,link,momento,nome_from,nome_chat_to,str(quantidade))
        print('[convite inserido no bd]')
    except Exception as e:
        print('[Error ao inserir Convite]')
        print(e)
        pass

    try:
        user_1 = nome_from
        user_2 = nome_chat_to
        point_user_1 = '0'
        point_user_2 = '0'
        winner = None
        total_questao = len(lista)
        lista_questao = str(lista)
        lista_id_questoes = str(lista_id_questoes)
    
        connection_db().insert_game(evento,link,momento, user_1,user_2,point_user_1, point_user_2,winner, total_questao,lista_questao,lista_id_questoes) 

    except Exception as e:
        print(e)
        pass

    dicio = {
        'evento_chat':evento_chat,
        'evento':evento,
        'link':link,
        
    }

    return dicio

@app.route('/msg_chat_enviar', methods=['POST'])
def msg_chat_enviar():
    nome_from = request.form['nome_from']
    evento= request.form['evento']
    msg_a_enviar = request.form['msg_a_enviar']

    dicio = {

        'nome_from':nome_from,  
        'evento':evento,  
        'msg_a_enviar':msg_a_enviar,    

    }
    try:
        connection_pusher(evento,dicio)

        return 'mensagem enviada ao Pusher'
    except:

        return 'mensagem nao enviada'

    
# @app.route('/<disciplina>/questao/<topico>/<momento>/_evento_/<evento>/?', methods=['POST'])
@app.route('/<disciplina>/questao/<topico>/<quantidade>/<momento>/_evento_/<evento>/_i_/<i_nome_from>')
def entender_link_gerar(disciplina,topico,quantidade,momento,evento,i_nome_from):

    try:
        username = connection_db().get_user_by_id(i_nome_from)
        username = username[0][0]
        print('--------')
        print("USERNAME -> :", username)
    except:
        username = 'TEstando'
        pass

    lista = connection_db().get_lista_game(momento)
    lista1 = list(lista[0])
    
    lista = ast.literal_eval(lista1[-2])
    # print(lista)

    topico = topico.strip().replace(' ','')

    
    try:
        alter = request.form['alternativa_selecionada']
        # print('----')
        # print(alter)
    except Exception as e:
        # print('-------
        pass
    
    cod_1 = evento[0:3]
    cod_2 = evento[-3:]

    user_1 = connection_db().get_user_by_id(cod_1)
    user_2 = connection_db().get_user_by_id(cod_2)
    
    dicio_users ={
        'user_1':user_1,
        'cod_1':cod_1,
        'user_2':user_2,
        'cod_2':cod_2,
        'evento':evento,
    }
   
    for i in range(0, len(lista)):
        lista[i][5] = lista[i][5].split('\n')          

#     ------> pAGINATION FAIL
    # quantos_por_pagina = 1
    # pagination = Pagination(page=page, total=len(lista), search=search,per_page=quantos_por_pagina)
    # if page==1:
    #     lista = lista[0:(page)*quantos_por_pagina]
    # else:
    #     lista = lista[(page-1)*quantos_por_pagina:(page)*quantos_por_pagina]

    print('LISTA FINAl')
    print(lista)
    print('------------')
    print(lista[0])

    return render_template('questao_page.html', dicio_users=dicio_users, lista=lista,range=range, len=len)


@app.route('/tratar_questao', methods=['POST'])
def  tratar_questao():

    user = request.form['user']
    print("--USER ENVIANDO RESPSOTA----")
    print(user)
    nome_texto_questao = request.form['nome_texto_questao']
    id_questao = request.form['id_questao']
    gab_questao = str(request.form['gab_questao']).strip().lower()
    alternativa_selecionada = str(request.form['alternativa_selecionada']).strip().lower()
    momento_to_focus = request.form['momento_to_focus']
    # print('Gab')
    # print(gab_questao)
    # print('ALt')
    # print(alternativa_selecionada)
    print('-- ID---')
    print(id_questao)
    if gab_questao == alternativa_selecionada:
        print("[CERTO]")
        resultado = 'Certo!'
        ponto=1
    else:
        print("[ERRADO]")
        resultado = 'Errado!'
        ponto=-1

    evento = request.form['evento']

    dicio ={
        'user':user,
        'id_questao':id_questao,
        'nome_texto_questao':nome_texto_questao,
        'gab':gab_questao,
        'alt':alternativa_selecionada,
        'resultado':resultado,
        'momento_to_focus':momento_to_focus,
        'evento':evento,
        'ponto':ponto
    }
    print(dicio)
    
    try:
        # print("EVENTO --->")
        # print(evento)
        connection_pusher(evento,dicio)

        # return 'mensagem enviada ao Pusher'
    except:
        pass
        # return 'mensagem nao enviada'

    return dicio

@app.route('/checar_login_page_questoes', methods=["POST"])
def checar_login_page_questoes():

    try:
        username = str(request.form['username'])
        user_1 = str(request.form['user_1'])
        user_2 = str(request.form['user_2'])


        dicio = {
            'username':username,
            'user_1':user_1,
            'user_2':user_2,
        }
        print(dicio)
        
        # if (username != user_1) or ( username != user_2):
        #     return 'no'

        # else:
        #     return 'ok'
        # print(type(username))
        # print(type(user_1))
        # print(type(user_2))

        if username == user_1:
            dicio = {
                'ok':'ok', 'username': username,'res':'username=user1',
            }
            return dicio
        elif username == user_2:
            dicio = {
                'ok':'ok', 'username': username,'res':'username=user2',
            }
            return dicio
        else:
            dicio = {
                'ok':'no', 'username':username,
            }
            return dicio
    except Exception as e:
        print(e)
        dicio = {
                'ok':'no', 
                'username':''
            }
        return dicio
        

if __name__ == "__main__":
    app.run(debug=True)