import mysql.connector
from mysql.connector import errorcode

def show_databases(cursor):
	try:
		print('Databases existing:')
		cursor.execute('SHOW DATABASES')
		for line in cursor:
			print(line[0])		
	except Exception as err:
		print('ERROR!: {}'.format(err))

def connect_database(cursor, database_name):
	try:
		if is_connected(cursor):
			print('\nYou are already connected in to the database!\n')
			return None
		cursor.execute('USE {}'.format(database_name))
		print('\nSuccessfully Connected with {}!\n'.format(database_name))
	except Exception as err:
		print('ERROR!: {}'.format(err))        

def create_database(cursor, database_name):
    try:
        cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(database_name))
    except Exception as err:
        pass

def create_table(db, cursor, tabelas):
	for table_name in tabelas:
		table_description = tabelas[table_name]
		print("Creating table {} ".format(table_name))
		cursor.execute(table_description)
	# cursor.close()
	# db.close()

def insert_into_campeonato(db, cursor, dados_campeonato):
	add_campeonato = ("INSERT IGNORE INTO campeonato "
	"(idjogo, nome_campeonato, partida, data_hora) "
	"VALUES (%(idjogo)s, %(nome_campeonato)s, %(partida)s, %(data_hora)s)")
	cursor.execute(add_campeonato, dados_campeonato)
	# print("Campeonato inserido com sucesso!")
	db.commit()	
	# cursor.close()
	# db.close()

def insert_into_jogos(db, cursor, dados_jogos):
	add_campeonato = ("INSERT IGNORE INTO jogos "
	"(id_jogo, dados, valor) "
	"VALUES (%(idjogo)s, %(dados)s, %(valor)s)")
	cursor.execute(add_campeonato, dados_jogos)
	# print("Jogos inserido com sucesso!")
	db.commit()	
	# cursor.close()
	# db.close()

def drop_database(cursor, database_name):
    try:
        cursor.execute('DROP DATABASE {}'.format(database_name))
    except Exception as err:
        pass

def query(cursor, query):
	try:
		cursor.execute(query)
		for line in cursor:
			for i in range(len(line)):
				print(line[i], end = '; ')
			print()						
	except Exception as err:
		print('ERROR!: {}'.format(err))

def is_connected(cursor):
	cursor.execute('SELECT DATABASE()')
	for line in cursor:
		if line[0] is None: return False
		else: return True