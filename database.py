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
        sql = ("SELECT tb_user.user_email, role_name FROM tb_role INNER JOIN tb_user ON tb_user.role_id = tb_role.role_id WHERE role_name != 'Admin'")
        self.cursor.execute(sql)
        users = self.cursor.fetchall()
        self.cnx.commit()
        return users
        
    def add_user(self, email, password, role):
        sql = ("INSERT INTO tb_user (user_email, user_password, role_id) SELECT '%s', '%s', role_id FROM tb_role WHERE tb_role.role_name = '%s'" % (email, password, role))
        self.cursor.execute(sql)
        self.cnx.commit()

    def update_user(self, email, password, role):
        if (email and password and role):
            sql = ("UPDATE tb_user JOIN tb_role ON tb_role.role_name = '%s' SET tb_user.user_email = '%s', tb_user.user_password = '%s', tb_user.role_id = tb_role.role_id WHERE tb_user.user_email = '%s'" % (role, email, password, email))
            self.cursor.execute(sql)
            self.cnx.commit()
        elif (email and role):
            sql = ("UPDATE tb_user JOIN tb_role ON tb_role.role_name = '%s' SET tb_user.user_email = '%s', tb_user.role_id = tb_role.role_id WHERE tb_user.user_email = '%s'" % (role, email, email))
            self.cursor.execute(sql)
            self.cnx.commit()  

    def delete_user(self, email):
        sql = ("DELETE FROM tb_user WHERE user_email = '%s'" % email)
        self.cursor.execute(sql)
        self.cnx.commit()

    def get_all_questions_json(self):
        sql = ("""
            SELECT JSON_OBJECT(
                'question', tb_question.question_text,
                'answers', JSON_ARRAYAGG(JSON_OBJECT('text', tb_answer.answer_text, 'is_true', tb_answer.is_true))
            ) AS questions
            FROM tb_question
            JOIN tb_answer ON tb_question.question_id = tb_answer.question_id
            GROUP BY tb_question.question_id
        """)
        self.cursor.execute(sql)
        questions = self.cursor.fetchall()
        self.cnx.commit()
        return questions
    
    def add_question(self, question, alter1, alter2, alter3, answer):
        self.cursor.execute("INSERT INTO tb_question (question_text) SELECT '%s'" % (question))
        question_id = self.cursor.lastrowid
        self.cursor.executemany("INSERT INTO tb_answer (answer_text, is_true, question_id) VALUES (%s, %s, %s)", [(alter1, 0, question_id), (alter2, 0, question_id), (alter3, 0, question_id), (answer, 1, question_id)])
        self.cnx.commit()
        print("Questão adicionada!")

    def update_question(self, question_id, question, alter1, alter2, alter3, answer):
        self.cursor.execute("START TRANSACTION")

        sql1 = ("UPDATE tb_question SET question_text = '%s' WHERE question_id = %s" % (question, question_id))
        self.cursor.execute(sql1)

        # Atualiza cada alternativa individualmente
        sql2 = ("""
            UPDATE tb_answer
            JOIN (
                SELECT 
                    question_id, answer_id, answer_text,
                    ROW_NUMBER() OVER (PARTITION BY question_id ORDER BY is_true ASC) AS rn
                FROM tb_answer
                WHERE question_id = %s
            ) AS subquery
            ON tb_answer.answer_id = subquery.answer_id
            SET tb_answer.answer_text = 
                CASE 
                    WHEN subquery.rn = 1 THEN '%s'
                    WHEN subquery.rn = 2 THEN '%s'
                    WHEN subquery.rn = 3 THEN '%s'
                    WHEN subquery.rn = 4 THEN '%s'
                END
        """ % (question_id, alter1, alter2, alter3, answer))
        self.cursor.execute(sql2)
        self.cnx.commit()

    def delete_question(self, question_id):
        sql = ("DELETE FROM tb_question WHERE question_id = '%s'" % (question_id))
        self.cursor.execute(sql)
        self.cnx.commit()

    def get_all_questions(self):
        sql = ("""
            SELECT tb_question.question_id, tb_question.question_text AS pergunta,
                (SELECT answer_text FROM tb_answer WHERE question_id = tb_question.question_id ORDER BY is_true ASC LIMIT 1 OFFSET 0) AS alternativa,
                (SELECT answer_text FROM tb_answer WHERE question_id = tb_question.question_id ORDER BY is_true ASC LIMIT 1 OFFSET 1) AS alternativa,
                (SELECT answer_text FROM tb_answer WHERE question_id = tb_question.question_id ORDER BY is_true ASC LIMIT 1 OFFSET 2) AS alternativa,
                (SELECT answer_text FROM tb_answer WHERE question_id = tb_question.question_id ORDER BY is_true ASC LIMIT 1 OFFSET 3) AS resposta
            FROM tb_question
        """)
        self.cursor.execute(sql)
        questions = self.cursor.fetchall()
        self.cnx.commit()
        return questions