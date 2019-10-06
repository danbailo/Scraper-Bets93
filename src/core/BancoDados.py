import mysql.connector

class BancoDados:
    def __init__(self, usuario=None, senha=None, nome_banco_dados="bets93"):
        if usuario is None or senha is None: 
            assert("Por favor, digite o usuário e a senha!")
        self.conn = mysql.connector.connect(user=usuario,passwd=senha)
        self.cursor = self.conn.cursor()
        self.cursor.execute(f"USE {nome_banco_dados}")
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS `jogos_uni` ("
            "  `id` int(11) NOT NULL,"
            "  `titulo` varchar(250) NOT NULL,"
            "  `data` datetime NOT NULL,"
            "  `slugLiga` varchar(120) DEFAULT NULL,"
            "  `pais` varchar(100) DEFAULT NULL,"
            "  `liga` varchar(100) DEFAULT NULL,"
            "  `status` int(11) NOT NULL,"
            "  `posicao` int(11) NOT NULL,"
            "   PRIMARY KEY(`id`)"    
            ") ENGINE=MyISAM DEFAULT CHARSET=latin1;"
        )
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS `modal_uni` ("
            "  `id` int(11) NOT NULL AUTO_INCREMENT,"
            "  `jogo_id` int(11) NOT NULL,"
            "  `odd_id` int(11) NOT NULL,"
            "  `cat_id` int(11) NOT NULL,"
            "  `categoria` varchar(250) NOT NULL,"
            "  `id_modal` int(11) NOT NULL,"    
            "  `propriedade` varchar(250) NOT NULL,"
            "  `valor` decimal(8,2) NOT NULL DEFAULT '0.00',"
            "  `status` int(11) NOT NULL,"
            "   PRIMARY KEY (`id`)"    
            ") ENGINE=MyISAM DEFAULT CHARSET=latin1;"
        )

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