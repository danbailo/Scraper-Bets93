import mysql.connector

class BancoDados:
    def __init__(self, usuario, senha, nome_banco_dados):
        self.conn = mysql.connector.connect(user=usuario,passwd=senha, database=nome_banco_dados)
        self.cursor = self.conn.cursor()
        
    def truncate_tables(self):
        self.cursor.execute("TRUNCATE TABLE jogos_uni")
        self.cursor.execute("TRUNCATE TABLE modal_uni")

    def insert_into_jogos_uni(self,jogos_uni):
        add_jogos_uni = (
            "INSERT IGNORE INTO jogos_uni "
            "(id, titulo, data, slugLiga, pais, liga, status, posicao) "
            "VALUES (%(id_jogo)s, %(titulo)s, %(data_hora)s, %(slugLiga)s, %(pais)s, %(liga)s, %(status)s, %(posicao)s)"
        )
        self.cursor.execute(add_jogos_uni, jogos_uni)
        self.conn.commit()	

    def insert_into_modal_uni(self,modal_uni):
        add_modal_uni = (
            "INSERT IGNORE INTO modal_uni "
            "(jogo_id, odd_id, cat_id, categoria, id_modal, propriedade, valor, status) "
            "VALUES (%(jogo_id)s, %(odd_id)s, %(cat_id)s, %(categoria)s, %(id_modal)s, %(propriedade)s, %(valor)s, %(status)s)"
        )
        self.cursor.execute(add_modal_uni, modal_uni)
        self.conn.commit()