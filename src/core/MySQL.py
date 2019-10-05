import mysql.connector

class MySQL:
    def __init__(self, user=None, password=None, host=None, database=None):
        if host is None: self.host = 'localhost'
        if user is None or password is None: return None
            
        config = {
            'user': user,
            'password': password,
            'database': database, 
            'host': self.host,
        }
        try:
            self.connect = mysql.connector.connect(**config)
        except Exception as err:
            print('CONNECT ERROR -',err)
            return None

    def __enter__(self):
        self.cursor = self.connect.cursor()
        return self.connect,self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.connect.close()