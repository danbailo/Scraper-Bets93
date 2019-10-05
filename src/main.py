from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from time import time
from core import MySQL
import requests
import re
import datetime
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

options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(options=options)
driver.get("https://bets93.net/")
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='lateral']/div/ul"))).click()

pattern_campeonato = re.compile(r"c_visivel")
pattern_jogo = re.compile(r"j_visivel_")

soup = BeautifulSoup(driver.page_source, "html.parser")
tabela_jogos = soup.find(class_="jogos")
jogos = tabela_jogos.findAll("div",recursive=False)

with MySQL("daniel", "123456789") as database:
	db = database[0]
	cursor = database[1]
	utils.create_database(cursor, "bets93")
	utils.create_table(cursor)
	utils.truncate_table(cursor)

	for jogo in jogos:		
		attr = jogo.get("id")
		if pattern_campeonato.match(attr):
			NOME_CAMP = jogo.find(class_="camp").text
			slugLiga = NOME_CAMP.lower().replace(' ','-')
			slugLiga = re.sub(pattern=r'(^-|-$)',repl='', string=slugLiga)
			pais = NOME_CAMP.split()[0]
			liga = NOME_CAMP.split()[1:]
			liga = ' '.join(liga)
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
				'id_jogo':id_jogo, 
				'titulo': titulo, 
				'data_hora': data_hora, 
				'slugLiga': slugLiga,
				'pais':pais, 
				'liga': liga, 
				'status': 1, 
				'posicao': 1
			}
			utils.insert_into_jogos_uni(db, cursor, dados_jogos_uni)            
			# print("Dados inseridos na tabela 'jogos_uni'")

			params = (('id_jogo', str(id_jogo)),)
			
			stop = 0
			while True:
				start = time()
				response = requests.get('https://bets93.net/api.php', headers=headers, params=params)
				if response.ok: 
					json_response = response.json()
					break
				elif stop > 15:
					assert("\nErro ao fazer as requisições, por favor, execute o programa novamente!\n")
					exit(-1)
				else: stop+=1
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

			botao = "jogo_"+str(id_jogo)+"_outros"
			try: WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, botao))).click()
			except Exception: WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "btn.btn-danger"))).click()

			soup = BeautifulSoup(driver.page_source, "html.parser")
			modal = soup.find(id="modal")
			camps = modal.findAll(class_="camp")
			props = modal.findAll(class_="col-9 col-sm-9",recursive=True)
			while (len(set(categoria)) != len(camps)) or (len(propriedade) != len(props)):
				soup = BeautifulSoup(driver.page_source, "html.parser")
				modal = soup.find(id="modal")				
				camps = modal.findAll(class_="camp")
				props = modal.findAll(class_="col-9 col-sm-9",recursive=True)

			for i in range(len(camps)): camps[i] = camps[i].text
			dict_categorias = dict(zip(set(categoria),camps))
			for i in range(len(props)): props[i] = props[i].text
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
					'status':1
				}
				utils.insert_into_modal_uni(db, cursor, dados_modal_uni)		
			# print("Dados inseridos na tabela 'modal_uni'\n")
			print(f'Partida "{titulo}" inserida no banco de dados com sucesso!')
			print(f"ID:{id_jogo}\n")
			try: WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "btn.btn-danger"))).click()
			except Exception: pass
	print("Todos os dados foram inseridos com sucesso!")