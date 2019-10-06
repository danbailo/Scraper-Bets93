# Scraper Bets93

## Descrição
Este projeto consiste em coletar todos os dados do site Bets93 e armazená-los num banco de dados MySQL.

---
## Requisitos

* `Python 3`
* `pip (Gerenciador de pacotes do Python)`
* `Google Chrome Versão 77`
* `Selenium Driver (Já disponível no arquivo .zip para Windows) -`[ Download](https://chromedriver.storage.googleapis.com/index.html?path=77.0.3865.40/)
* `MySQL 5.7`
  
---
## Dependências

Para instalar as dependências, execute os comandos abaixo num terminal/prompt de comando:

* Linux
  * `python3 -m pip install -r requirements.txt --user`

* Windows
  * `python -m pip install -r requirements.txt --user`

**Instalando Selenium Driver no Linux**

* `sudo apt-get install -y unzip xvfb libxi6 libgconf-2-4`
* Caso você não tenha o Java instalado no computador, instale-o usando o comando abaixo:
  * `sudo apt-get install default-jdk`

---
## Como usar

Para executar o programa, abra um terminal/prompt de comando aberto, siga os passos abaixo:
* `cd src/`
  * Linux
  * `python3 main.py NOME_DE_USUARIO SENHA`

  * Windows
  * `python main.py NOME_DE_USUARIO SENHA`

Onde o NOME_DE_USUARIO e a SENHA, estão relacionados ao usuário e senha do **BANCO DE DADOS**.

*Exemplo*

`python main.py teste 1234`

---