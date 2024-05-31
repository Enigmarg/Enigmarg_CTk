import customtkinter
import tkinter as tk
from tkinter import messagebox
from database import Database
from hashlib import sha256
from PIL import Image
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Login():

    def __init__(self):
        self.width = 380
        self.height = 450
        self.screen = customtkinter.CTk()
        self.screen.configure(fg_color="cornflower blue")
        customtkinter.set_appearance_mode("light")
        self.screen.resizable(False, False)

        # Centers the window
        screen_width = self.screen.winfo_screenwidth()
        screen_height = self.screen.winfo_screenheight()
        x = (screen_width / 2) - (self.width / 2)
        y = (screen_height / 2) -  ( self.height / 2)

        self.screen.geometry("%dx%d+%d+%d" % (self.width, self.height, x, y))

        self.enigmarg_logo = Image.open("resources/logo.png")
        self.view_icon = tk.PhotoImage(file="resources/view.png")
        self.hide_icon = tk.PhotoImage(file="resources/hide.png")

        self.smtp_server = os.getenv("SMTP_SERVER")
        self.smtp_port = os.getenv("SMTP_PORT")
        self.sender_email = os.getenv("SENDER_EMAIL")
        self.sender_password = os.getenv("SENDER_PASSWORD")
        self.receiver_email = os.getenv("RECEIVER_EMAIL")

    def clear_screen(self):
        for widget in self.screen.winfo_children():
            widget.destroy()

    def toggle_password(self):
        if self.password_input.cget("show") == "":
            self.password_input.configure(show="*")
            self.toggle_btn.configure(image=self.hide_icon)
        else:
            self.password_input.configure(show="")
            self.toggle_btn.configure(image=self.view_icon)
    
    def get_email(self):
        email = self.email_input.get()
        return email

    def get_password(self):
        password = self.password_input.get()
        return sha256(password.encode("utf-8")).hexdigest()
    
    def check_user(self):
        if database.get_user(self.get_email(), self.get_password()):
            print("Login feito com sucesso!")
            self.screen.destroy()
        else:
            print("Email ou senha inválidos.")
            messagebox.showerror("Erro", "Email ou senha inválidos.")
        
    def send_forgot_password_email(self): 
        if database.get_user_email(self.get_email()):
            msg = MIMEMultipart()
            msg["From"] = self.sender_email
            msg["To"] = self.receiver_email
            msg["Subject"] = "Recuperação de senha Enigmarg"
            message = f"""
                <h1>Recuperação de senha Enigmarg</h1>
                <p>Prezado(a) Professor(a),</p>
                <p>Um dos usuários do Enigmarg solicitou a redefinição de senha de acesso, e estamos aqui para tentar facilitar o processo.</p>
                <p>Aqui estão os detalhes do usuário e as instruções para ajudá-lo a recuperar sua senha:</p>
                <p><strong>E-mail do usuário:</strong> {self.get_email()}</p>
                <p>Para redefinição de senha do usuário, siga os seguintes passos:</p>
                <ol>
                    <li>Faça o login no Enigmarg com as credenciais de professor, para que possa visualizar o gerenciador de usuários.</li>
                    <li>Procure pelo e-mail do usuário que necessita recuperar a senha e selecione-o, ou simplesmente digite o e-mail do usuário no campo de e-mail.</li>
                    <li>Insira uma nova senha para esse usuário no campo de senha.</li>
                    <li>Garanta que todas as informações estejam corretas (email do usuário, senha e o cargo).</li>
                    <li>Aperte no botão de atualizar, e veja se não ocorreu nenhum erro.</li>
                </ol>
                <p>Após todo processo, você já poderá comunicar o usuário da melhor forma, informando suas novas credenciais.</p>
                <p>Agradecemos pela colaboração.</p>
                <p>Atenciosamente,<br>Equipe Enigmarg</p>
            """
            msg.attach(MIMEText(message, "html"))

            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            print("Login feito com sucesso!")
            server.sendmail(self.sender_email, self.receiver_email, msg.as_string())
            print("Email enviado com sucesso!")
        else:
            messagebox.showerror("Erro", "Email inválido.")

    def create_login_screen(self):
        self.clear_screen()
        self.screen.title("Login")

        enigmarg_logo = customtkinter.CTkImage(light_image=self.enigmarg_logo, dark_image=self.enigmarg_logo, size=(185, 145))
        logo_label = customtkinter.CTkLabel(self.screen, text="", image=enigmarg_logo)
        logo_label.pack(pady=45)

        self.email_input = customtkinter.CTkEntry(self.screen, width=200, height=30, placeholder_text="E-mail", border_width=0)
        self.email_input.place(relx=0.5, rely=0.5, anchor="center")

        self.password_input = customtkinter.CTkEntry(self.screen, width=200, height=30, placeholder_text="Senha", show="*", border_width=0)
        self.password_input.place(relx=0.5, rely=0.6, anchor="center")

        login_btn = customtkinter.CTkButton(self.screen, width=200, height=30, text="Entrar", fg_color="royal blue", hover=False, command=self.check_user)
        login_btn.place(relx=0.5, rely=0.7, anchor="center")

        self.toggle_btn = customtkinter.CTkButton(self.password_input, text="", width=0, height=0, image=self.hide_icon, fg_color="transparent", hover=False, command=self.toggle_password)
        self.toggle_btn.place(relx=0.9, rely=0.5, anchor="center")

        forgot_password_btn = customtkinter.CTkButton(self.screen, width=0, height=0, text="Esqueceu a senha?", command=self.create_forgot_password_screen, text_color="white", fg_color="transparent", hover=False, cursor="hand2")
        forgot_password_btn.place(relx=0.5, rely=0.8, anchor="center")

        self.screen.mainloop()

    def create_forgot_password_screen(self):
        self.clear_screen()
        self.screen.title("Login")

        enigmarg_logo = customtkinter.CTkImage(light_image=self.enigmarg_logo, dark_image=self.enigmarg_logo, size=(185, 145))
        logo_label = customtkinter.CTkLabel(self.screen,text="", image=enigmarg_logo)
        logo_label.pack(pady=45)

        self.email_input = customtkinter.CTkEntry(self.screen, width=200, height=30, placeholder_text="E-mail", border_width=0)
        self.email_input.place(relx=0.5, rely=0.5, anchor="center")

        send_btn = customtkinter.CTkButton(self.screen, width=200, height=30, text="Enviar", fg_color="royal blue", hover=False, command=self.send_forgot_password_email, cursor="hand2")
        send_btn.place(relx=0.5, rely=0.6, anchor="center")

        return_btn = customtkinter.CTkButton(self.screen, width=0, height=0, text="Voltar", command=self.create_login_screen, text_color="white", fg_color="transparent", hover=False, cursor="hand2")
        return_btn.place(relx=0.5, rely=0.7, anchor="center")

        self.screen.mainloop()


if __name__ == "__main__":
    database = Database()
    database.connect()
    Login().create_login_screen()