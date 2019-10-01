#https://docs.python.org/3/reference/datamodel.html#object.__new__

import mysql.connector
from mysql.connector import errorcode

#A classe retorna um objeto do tipo cursor, isso porque foi definido do __enter__ do mesmo;

class MySQLcompatible:
    """MySQL databate connection compatible with statement"""
    def __init__(self, user=None, password=None, host=None, database=None):
        if host is None: self.host = 'localhost'
        # if port is None: self.port = 3306
        if user is None or password is None: return None
            
        config = {
            'user': user,
            'password': password,
            'database': database, 
            'host': self.host,
            # 'port':self.port
            }
        try:
            self.connect = mysql.connector.connect(**config)            
            # return self.connect
        except Exception as err:
            print('CONNECT ERROR -',err)
            return None

    def __enter__(self):
        self.cursor = self.connect.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.connect.close()