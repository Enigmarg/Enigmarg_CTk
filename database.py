from dotenv import load_dotenv
import os
import mysql.connector
from mysql.connector.constants import ClientFlag

load_dotenv()

class Database():
    def __init__(self):
        self.host = os.getenv("HOST")
        self.user = os.getenv("USER")
        self.password = os.getenv("PASSWORD")
        self.database = os.getenv("DATABASE")
        # self.port = os.getenv("PORT")

    def connect(self):
        try:
            self.cnx = mysql.connector.connect(
                user = self.user,
                password = self.password,
                host = self.host,
                database = self.database,
                # port = self.port,
                # client_flags = [ClientFlag.SSL],
                # "ssl_ca": "/opt/mysql/ssl/ca.pem",
                # "ssl_cert": "/opt/mysql/ssl/client-cert.pem",
                # "ssl_key": "/opt/mysql/ssl/client-key.pem",
            )
            print("Conexão bem sucedida!")
            self.cursor = self.cnx.cursor(buffered=True)
            return self.cnx
        except mysql.connector.Error as err:
            print(f"Falha na conexão! {err}")
            return None
        
    def get_user_password(self, email):
        try:
            sql = ("SELECT user_password FROM tb_user WHERE user_email='%s'" % email)
            self.cursor.execute(sql)
            self.cnx.commit()
            password = self.cursor.fetchone()[0]
            return password
        except Exception as e:
            print(e)
            
    def get_all_users(self):
        sql = ("SELECT tb_user.user_email, role_name FROM tb_role INNER JOIN tb_user ON tb_user.role_id = tb_role.role_id")
        self.cursor.execute(sql)
        users = self.cursor.fetchall()
        return users
        
    def add_user(self, email, password, role):
        sql = ("INSERT INTO tb_user (user_email, user_password, role_id) SELECT '%s', '%s', role_id FROM tb_role WHERE tb_role.role_name = '%s'" % (email, password, role))
        self.cursor.execute(sql)
        self.cnx.commit()