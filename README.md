# Scraper Bets93

## Descrição
Este projeto consiste em coletar todos os dados do site Bets93 e armazená-los num banco de dados MySQL.

---
## Requisitos

* `Python 3`
* `pip (Gerenciador de pacotes do Python)`
* `Google Chrome Versão 77`
* `Selenium Driver`
* `MySQL 5.7`
  
---
## Dependências

Para instalar as dependências, execute os comandos abaixo num terminal/prompt de comando:

* Linux
  * `python3 -m pip install -r requirements.txt --user`

* Windows
  * `python -m pip install -r requirements.txt --user`

### Instalando Selenium Driver no Linux

* `sudo apt-get install -y unzip xvfb libxi6 libgconf-2-4`
* Caso você não tenha o Java instalado no computador, instale-o usando o comando abaixo:
  * `sudo apt-get install default-jdk`
* [Download -  chromedriver_linux64.zip](https://chromedriver.storage.googleapis.com/77.0.3865.40/chromedriver_linux64.zip)
* `unzip chromedriver_linux64.zip`
* `sudo mv chromedriver /usr/bin/chromedriver`
* `sudo chown root:root /usr/bin/chromedriver`
* `sudo chmod +x /usr/bin/chromedriver`
---
## Como usar

Para executar o programa, abra um terminal/prompt de comando aberto, siga os passos abaixo:
* `cd src/`
  * Linux
  * `python3 main.py NOME_DE_USUARIO SENHA NOME_BANCO_DADOS`

  * Windows
  * `python main.py NOME_DE_USUARIO SENHA NOME_BANCO_DADOS`

Onde o NOME_DE_USUARIO e a SENHA, estão relacionados ao usuário e senha do **BANCO DE DADOS** e o NOME_BANCO_DADOS é o nome do banco de dados que o usuário irá se conectar.

*Exemplo*

* `python main.py teste 1234 NOME_BANCO_DADOS`

* Exemplo caso o usuário do banco de dados não possue senha.
  * `python main.py teste "" NOME_BANCO_DADOS`
 

---