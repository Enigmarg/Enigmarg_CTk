import mysql.connector
import os

class Database():
    def __init__(self):
        self.host = os.getenv("HOST")
        self.user = os.getenv("USER")
        self.password = os.getenv("PASSWORD")
        self.database = os.getenv("DATABASE")

    def connect(self):
        try:
            self.cnx = mysql.connector.connect(
                host = self.host,
                user = self.user,
                password = self.password,
                database = self.database
            )
            print("Conexão bem sucedida!")
            self.cursor = self.cnx.cursor(buffered=True)
            return self.cnx
        except mysql.connector.Error as err:
            print(f"Falha na conexão! {err}")
            return None
        
    def add_user_to_database(self, email, password, role_id):
        sql = ("INSERT INTO tb_user(user_email, user_password, role_id) VALUES (%s, %s, %s)" % email, password, role_id) # Ainda é necessário a implementação de uma janela com a opção de seleção de cargos.
        self.cursor.execute(sql)
        self.cnx.commit()

    def get_password_from_database(self, email):
        sql = ("SELECT user_password FROM tb_user WHERE user_email='%s'" % email)
        self.cursor.execute(sql)
        self.cnx.commit()
        password = self.cursor.fetchone()[0]
        return password