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
            self.cursor = self.cnx.cursor()
            return self.cnx
        except mysql.connector.Error as err:
            print(f"Falha na conexão! {err}")
            return None
        
    def add_user_to_database(self, email, password):
        sql = "INSERT INTO tb_user(user_email, user_password, role_id) VALUES (%s, %s, 1)" # O role_id 1 é apenas para testes, pois ainda não temos uma janela com a opção de seleção de cargos.
        self.cursor.execute(sql, (email, password))
        self.cnx.commit()