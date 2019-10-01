#data for example
#https://github.com/datacharmer/test_db
#https://medium.com/@ramojol/python-context-managers-and-the-with-statement-8f53d4d9f87


#CRUD in SQL
#Create           - INSERT
#Read (Retrieve)  - SELECT
#Update (Modify)  -	UPDATE
#Delete (Destroy) - DELETE
from core import MySQLcompatible
import utils

if __name__ == "__main__":

    tabelas = {}

    tabelas['campeonato'] = (
    "CREATE TABLE `campeonato` ("
    " `nome_campeonato` varchar(100) NOT NULL,"
    " `partidas` varchar(150) NOT NULL,"
    " PRIMARY KEY (`nome_campeonato`)"
    ") ENGINE=InnoDB")

    with MySQLcompatible('daniel','123456789',) as db:
        utils.create_database(db, "bets93")
        utils.create_table(db, tabelas, "campeonato")
