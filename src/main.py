from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from utils import dict_id_modalidade, dict_tipo_modalidades
from core import BancoDados
import datetime
import requests
import re
import sys

def get_browser(url):
	options = webdriver.ChromeOptions()
	options.add_argument('headless')
	driver = webdriver.Chrome(options=options)
	driver.get(url)
	WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='lateral']/div/ul"))).click()	
	return driver

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print("\nPara executar o programa, digite o usuário e senha do banco de dados na linha de comando!")
		print("\npython main.py USUARIO SENHA")
		print("\nExemplo:")
		print("\tpython main.py teste 1234")
		print('\nPara usuário que não tem senha, deve-se colocar ""')
		print("\nExemplo:")
		print('\tpython main.py teste ""')
		exit(-1)
		
	bd = BancoDados(usuario=sys.argv[1], senha=sys.argv[2], nome_banco_dados="bets93")
	bd.truncate_tables()
	
	base_url = "https://bets93.net/"
	driver = get_browser(base_url)
	soup = BeautifulSoup(driver.page_source, "html.parser")
	pattern_campeonato = re.compile(r"c_visivel")
	pattern_jogo = re.compile(r"j_visivel_")
	jogos = soup.find(class_="jogos").findAll("div",recursive=False)
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

			bd.insert_into_jogos_uni({
				'id_jogo':id_jogo, 
				'titulo': titulo, 
				'data_hora': data_hora, 
				'slugLiga': slugLiga,
				'pais':pais, 
				'liga': liga, 
				'status': 1, 
				'posicao': 1
			})     		
			stop = 0
			while True:
				response = requests.get(base_url+"api.php?id_jogo="+str(id_jogo))
				if response.status_code == 200:
					try: json_response = response.json()
					except Exception: 
						stop+=1
						continue
					break
				elif stop > 15:
					assert("\nErro ao fazer as requisições, por favor, execute o programa novamente!\n")
					exit(-1)
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

			for i in range(len(categoria)):
				bd.insert_into_modal_uni({ 
					'jogo_id': id_jogo,
					'odd_id':odd_id[i], 
					'cat_id':categoria[i], 
					'categoria':dict_tipo_modalidades[categoria[i]],
					'id_modal':propriedade[i],
					'propriedade':dict_id_modalidade[propriedade[i]], 
					'valor':valor[i],
					'status':1
				})		
			print(f'Partida "{titulo}" inserida no banco de dados com sucesso!')
			print(f"ID:{id_jogo}\n")
	print("Todos os dados foram inseridos com sucesso!")
	bd.cursor.close()
	bd.conn.close()

