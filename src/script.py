from selenium import webdriver
from core import MySQLcompatible
from bs4 import BeautifulSoup
import requests
import re
import datetime
import time
import utils

headers = {
	'sec-fetch-mode': 'cors',
	'cookie': '__cfduid=d286a6b04f21dc52264db8885f48b8f971570143846',
	'accept-encoding': 'gzip, deflate, br',
	'accept-language': 'en,en-US;q=0.9,pt-BR;q=0.8,pt;q=0.7',
	'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
	'accept': 'application/json, text/javascript, */*; q=0.01',
	'referer': 'https://bets93.net/',
	'authority': 'bets93.net',
	'x-requested-with': 'XMLHttpRequest',
	'sec-fetch-site': 'same-origin',
}	

tabelas = {}

tabelas['jogos_uni'] = (
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
") ENGINE=MyISAM DEFAULT CHARSET=latin1;")

tabelas['modal_uni'] = (
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
") ENGINE=MyISAM DEFAULT CHARSET=latin1;")


options = webdriver.ChromeOptions()
options.add_argument('headless')
browser = webdriver.Chrome(options=options)
browser.get("https://bets93.net/")
browser.find_element_by_xpath("//div[@class='lateral']/div/ul").click()

pattern_campeonato = re.compile(r"c_visivel")
pattern_jogo = re.compile(r"j_visivel_")

soup = BeautifulSoup(browser.page_source, "html.parser")
tabela_jogos = soup.find(class_="jogos")
jogos = tabela_jogos.findAll("div",recursive=False)

with MySQLcompatible("daniel", "123456789") as database:
	db = database[0]
	cursor = database[1]
	utils.create_database(cursor, "bets93")
	utils.create_table(cursor, tabelas)
	utils.truncate_table(cursor, tabelas)

	for jogo in jogos:		
		attr = jogo.get("id")
		if pattern_campeonato.match(attr):
			NOME_CAMP = jogo.find(class_="camp").text
			slugLiga = NOME_CAMP.lower().replace(' ','-')
			slugLiga = re.sub(pattern=r'(^-|-$)',repl='', string=slugLiga)
			pais = NOME_CAMP.split()[0]
			liga = NOME_CAMP.split()[1:]
			liga = ' '.join(liga)
			status = 1
			posicao = 1
		elif pattern_jogo.match(attr):
			id_jogo = int(attr.split('_')[-1])
			titulo = jogo.find(class_="times fundojogos").text.split()[:-3]
			titulo = ' '.join(titulo)        
			data_hora = jogo.find(class_="datahora").text
			ano = int(data_hora.split()[0].split('/')[2])
			mes = int(data_hora.split()[0].split('/')[1])
			dia = int(data_hora.split()[0].split('/')[0])
			horas = int(data_hora.split()[-1].split(':')[0])
			minutos = int(data_hora.split()[-1].split(':')[1])
			data_hora = str(datetime.datetime(ano,mes,dia,horas,minutos))

			dados_jogos_uni = {
				'id_jogo':id_jogo, 'titulo': titulo, 'data_hora': data_hora, 'slugLiga': slugLiga,
				'pais':pais, 'liga': liga, 'status': status, 'posicao': posicao
			}
			utils.insert_into_jogos_uni(db, cursor, dados_jogos_uni)            
			print("Dados inseridos na tabela 'jogos_uni'")

			params = (('id_jogo', id_jogo),)
			while True:
				try:
					response = requests.get('https://bets93.net/api.php', headers=headers, params=params)
					json_response = response.json()
					break
				except Exception as err:
					pass
			response.close()

			valores = []  
			for dicionario in json_response:
				valores.append((dicionario['id_tipo_modalidade'], dicionario['id_modalidade'], dicionario['id_odd'], dicionario['odd']))        
			valores = sorted(valores, key=lambda x:int(x[0])/1)

			categoria = []        
			propriedade = []
			odd_id = []
			valor = []

			for id_tipo_modalidade, id_modalidade, id_odd, odd in valores:
				categoria.append(int(id_tipo_modalidade))
				propriedade.append(int(id_modalidade))
				odd_id.append(int(id_odd))
				valor.append(float(odd))

			status = 1

			botao = "jogo_"+str(id_jogo)+"_outros"
			while True:
				try:
					browser.find_element_by_id(botao).click()
					break
				except Exception: 
					browser.find_element_by_class_name("btn.btn-danger").click()			
			time.sleep(1)
			soup = BeautifulSoup(browser.page_source, "html.parser")
			modal = soup.find(id="modal")

			camps = modal.findAll(class_="camp")
			for i in range(len(camps)):
				camps[i] = camps[i].text
			dict_categorias = dict(zip(set(categoria),camps))

			props = modal.findAll(class_="col-9 col-sm-9",recursive=True)
			for i in range(len(props)):
				props[i] = props[i].text
			dict_propriedades = dict(zip(propriedade,props))

			for i in range(len(categoria)):
				dados_modal_uni = { 
					'jogo_id': id_jogo,
					'odd_id':odd_id[i], 
					'cat_id':categoria[i], 
					'categoria':dict_categorias[categoria[i]],
					'id_modal':propriedade[i],
					'propriedade':dict_propriedades[propriedade[i]], 
					'valor':valor[i],
					'status':status
				}
				utils.insert_into_modal_uni(db, cursor, dados_modal_uni)		
			print("Dados inseridos na tabela 'modal_uni'\n")