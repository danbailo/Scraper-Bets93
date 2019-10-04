import mysql.connector
from mysql.connector import errorcode

def create_database(cursor, database_name):
	cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
	cursor.execute(f"USE {database_name}")

def create_table(db, cursor, tabelas):
	for nome_tabela in tabelas:
		cursor.execute(tabelas[nome_tabela])

def insert_into_jogos_uni(db, cursor, jogos_uni):
	add_jogos_uni = (
		"INSERT IGNORE INTO jogos_uni "
		"(id, titulo, data, slugLiga, pais, liga, status, posicao) "
		"VALUES (%(id_jogo)s, %(titulo)s, %(data_hora)s, %(slugLiga)s, %(pais)s, %(liga)s, %(status)s, %(posicao)s)"
		)
	cursor.execute(add_jogos_uni, jogos_uni)
	db.commit()	

def insert_into_modal_uni(db, cursor, modal_uni):
	add_modal_uni = (
		"INSERT IGNORE INTO modal_uni "
		"(id, jogo_id, odd_id, cat_id, categoria, propriedade, valor, status) "
		"VALUES (%(id_jogo)s, %(odd_id)s, %(1)s, %(categoria)s, %(propriedade)s, %(valor)s, %(1)s, %(1)s)"
		)
	cursor.execute(add_modal_uni, modal_uni)
	db.commit()	