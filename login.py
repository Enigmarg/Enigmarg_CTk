import customtkinter
import tkinter as tk
from tkinter import messagebox
from database import Database
from hashlib import sha256
from PIL import Image
import smtplib
import os

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
        
    def send_email(self): 
        if database.get_user_email(self.get_email()):
            sender_email = os.getenv("SENDER_EMAIL")
            rec_email = "vitoreiken@gmail.com"
            password = os.getenv("PASSWORD_EMAIL")
            message = f"{self.get_email()} esqueceu a senha!"

            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender_email, password)
            print("Login feito com sucesso!")
            server.sendmail(sender_email, rec_email, message)
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

        send_btn = customtkinter.CTkButton(self.screen, width=200, height=30, text="Enviar", fg_color="royal blue", hover=False, command=self.send_email, cursor="hand2")
        send_btn.place(relx=0.5, rely=0.6, anchor="center")

        return_btn = customtkinter.CTkButton(self.screen, width=0, height=0, text="Voltar", command=self.create_login_screen, text_color="white", fg_color="transparent", hover=False, cursor="hand2")
        return_btn.place(relx=0.5, rely=0.7, anchor="center")

        self.screen.mainloop()


if __name__ == "__main__":
    database = Database()
    database.connect()
    Login().create_login_screen()
    # Login().send_email()