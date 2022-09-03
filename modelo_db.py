import psycopg2
import time
class connection_db:
    def __init__(self):
        self.host = 'ec2-34-234-240-121.compute-1.amazonaws.com'
        self.database = 'd9fcln1s12ch0t'
        self.user = 'iybppouzayyqmj'
        self.port = 5432
        self.password = 'c2b21316792112ba2970c6258f31d9568debe56cd54102ea5c41c44718fe194d'

    def get_connection(self):
        try: 

            conn = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password)
            #print(conn)
            print('[CONEXÃO FEITA]')
           # print('--------------------')
        except Exception as e:
            #print('Error no GetConection')
            #print(e)
            pass
        return conn
    

    def insert_user(self,nome):

        conn = self.get_connection()
        
        #print(conn)
        cursor = conn.cursor()
        time_stamp = time.time()
        cursor.execute("INSERT INTO contas (username,created_on, last_login) VALUES (%s,%s,%s);", (nome.strip(),time_stamp,time_stamp))
        conn.commit()
        cursor.close()
        conn.close()

    def get_all_users(self):
    
        conn = self.get_connection()
        cursor = conn.cursor()
        # cursor.execute("INSERT INTO lista_promocoes (nome_empresa, tipo_produto, preco,bairro, imagem) VALUES (%s,%s,%s,%s,%s);", (nome_empresa,tipo_produto,preco,bairro,render_file))
        # conn.commit()
        cursor.execute("SELECT * FROM contas")
        lista = cursor.fetchall()

        cursor.close()
        conn.close()

        return lista

    def get_all_users_minus(self, userid):
    
        conn = self.get_connection()
        cursor = conn.cursor()
        # cursor.execute("INSERT INTO lista_promocoes (nome_empresa, tipo_produto, preco,bairro, imagem) VALUES (%s,%s,%s,%s,%s);", (nome_empresa,tipo_produto,preco,bairro,render_file))
        # conn.commit()
        cursor.execute("SELECT * FROM contas WHERE userid != %s;",(userid))
        lista = cursor.fetchall()

        cursor.close()
        conn.close()

        return lista
    
    def gel_userid(self, nome):
    
        conn = self.get_connection()
        cursor = conn.cursor()
        # cursor.execute("INSERT INTO lista_promocoes (nome_empresa, tipo_produto, preco,bairro, imagem) VALUES (%s,%s,%s,%s,%s);", (nome_empresa,tipo_produto,preco,bairro,render_file))
        # conn.commit()
        cursor.execute("SELECT userid FROM contas WHERE username = '"  + nome +"'")
        lista = cursor.fetchall()

        cursor.close()
        conn.close()

        return lista

    def get_user_by_id(self, id):

        conn = self.get_connection()
        cursor = conn.cursor()
        # cursor.execute("INSERT INTO lista_promocoes (nome_empresa, tipo_produto, preco,bairro, imagem) VALUES (%s,%s,%s,%s,%s);", (nome_empresa,tipo_produto,preco,bairro,render_file))
        # conn.commit()
        cursor.execute("SELECT username FROM contas WHERE userid = '"  + id +"'")
        lista = cursor.fetchall()

        cursor.close()
        conn.close()

        return lista
        
    # def checar_gabarito(self, id_questao):
        
    #     conn = self.get_connection()
    #     cursor = conn.cursor()
    #     # cursor.execute("INSERT INTO lista_promocoes (nome_empresa, tipo_produto, preco,bairro, imagem) VALUES (%s,%s,%s,%s,%s);", (nome_empresa,tipo_produto,preco,bairro,render_file))
    #     # conn.commit()
    #     cursor.execute("SELECT username FROM contas WHERE userid = '"  + id_questao +"'")
    #     lista = cursor.fetchall()

    #     cursor.close()
    #     conn.close()

    #     return lista

    def insert_convite(self,evento,link, momento,user_1, user_2,quantidade):
        conn = self.get_connection()
        
        #print(conn)
        cursor = conn.cursor()
        time_stamp = time.time()
        cursor.execute("INSERT INTO convites (evento,link, momento,user_1, user_2,quantidade) VALUES (%s,%s,%s,%s,%s,%s);", (evento,link, momento,user_1, user_2,quantidade))
        conn.commit()
        cursor.close()
        conn.close()

    def get_my_convites(self, nome_to):
        
        conn = self.get_connection()
        cursor = conn.cursor()
        # cursor.execute("INSERT INTO lista_promocoes (nome_empresa, tipo_produto, preco,bairro, imagem) VALUES (%s,%s,%s,%s,%s);", (nome_empresa,tipo_produto,preco,bairro,render_file))
        # conn.commit()
        cursor.execute("SELECT * FROM convites WHERE user_2 = '"  + nome_to +"'")
        lista = cursor.fetchall()

        cursor.close()
        conn.close()

        return lista

    def insert_game(self, evento,link,momento, user_1,user_2,point_user_1, point_user_2,winner, total_questao,lista_questao,lista_id_questoes):
        conn = self.get_connection()
        
        #print(conn)
        cursor = conn.cursor()
        #time_stamp = time.time()
        cursor.execute("INSERT INTO games (evento,link,momento, user_1,user_2,point_user_1, point_user_2,winner, total_questao,lista_questao,lista_id_questoes) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);", (evento,link,momento, user_1,user_2,point_user_1, point_user_2,winner, total_questao,lista_questao,lista_id_questoes))
        conn.commit()
        cursor.close()
        conn.close()

    def get_lista_game(self, momento):
            
        conn = self.get_connection()
        cursor = conn.cursor()
        # cursor.execute("INSERT INTO lista_promocoes (nome_empresa, tipo_produto, preco,bairro, imagem) VALUES (%s,%s,%s,%s,%s);", (nome_empresa,tipo_produto,preco,bairro,render_file))
        # conn.commit()
        cursor.execute("SELECT * FROM games WHERE momento = '"  + momento +"'")
        lista = cursor.fetchall()

        cursor.close()
        conn.close()

        return lista

    def alter_game_point_user_1(self, point_user_1 ,momento ):
        conn = self.get_connection()
        cursor = conn.cursor()
        # cursor.execute("INSERT INTO lista_promocoes (nome_empresa, tipo_produto, preco,bairro, imagem) VALUES (%s,%s,%s,%s,%s);", (nome_empresa,tipo_produto,preco,bairro,render_file))
        # conn.commit()
        cursor.execute("UPDATE games SET point_user_1 ='" + point_user_1 +"' WHERE momento = '"+momento+"'")
        # lista = cursor.fetchall()

        cursor.close()
        conn.close()

    def alter_game_point_user_2(self, point_user_2 ,momento ):
        conn = self.get_connection()
        cursor = conn.cursor()
        # cursor.execute("INSERT INTO lista_promocoes (nome_empresa, tipo_produto, preco,bairro, imagem) VALUES (%s,%s,%s,%s,%s);", (nome_empresa,tipo_produto,preco,bairro,render_file))
        # conn.commit()
        cursor.execute("UPDATE games SET point_user_2 ='" + point_user_2 +"' WHERE momento = '"+momento+"'")
        # lista = cursor.fetchall()

        cursor.close()
        conn.close()

        