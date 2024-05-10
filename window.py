import customtkinter
from tkinter import messagebox
from database import Database
from hashlib import sha256

database = Database()
database.connect()

blue_link_color = "#0066CC"
blue_link_hover_color = "#0059B3"

class Login():

    def __init__(self):
        self.width = 380
        self.height = 450
        self.screen = customtkinter.CTk()
        customtkinter.set_appearance_mode("dark")
        self.screen.resizable(False, False)

        # Centers the window
        screen_width = self.screen.winfo_screenwidth()
        screen_height = self.screen.winfo_screenheight()
        x = (screen_width / 2) - (self.width / 2)
        y = (screen_height / 2) -  ( self.height / 2)

        self.screen.geometry("%dx%d+%d+%d" % (self.width, self.height, x, y))

    def clear_window(self):
        for widget in self.screen.winfo_children():
            widget.destroy()

    def create_login_screen(self):
        self.clear_window()
        self.screen.title("Login")

        self.email_input = customtkinter.CTkEntry(self.screen, width=200, height=30, placeholder_text="E-mail")
        self.email_input.place(x = self.width/2, y = self.height/2-40, anchor="center")

        self.password_input = customtkinter.CTkEntry(self.screen, width=200, height=30, placeholder_text="Senha", show="*")
        self.password_input.place(x = self.width/2, y = self.height/2, anchor="center")

        login_button = customtkinter.CTkButton(self.screen, width=200, height=30, text="Login", fg_color=blue_link_color, hover_color=blue_link_hover_color, command=self.check_user)
        login_button.place(x = self.width/2, y = self.height/2 + 40, anchor="center")

        link_forgot_password = customtkinter.CTkButton(self.screen, width=0, height=0, text="Esqueceu a senha?", command=self.create_forgot_password_screen, text_color=blue_link_color, fg_color="transparent", hover=False, cursor="hand2")
        link_forgot_password.place(x = self.width/2, y = self.height/2 + 80, anchor="center")

        self.screen.mainloop()

    def create_forgot_password_screen(self):
        self.clear_window()
        self.screen.title("Login")

        self.email_input = customtkinter.CTkEntry(self.screen, width=200, height=30, placeholder_text="E-mail")
        self.email_input.place(x = self.width/2, y = self.height/2-20, anchor="center")

        send_button = customtkinter.CTkButton(self.screen, width=200, height=30, text="Enviar", fg_color=blue_link_color, hover_color=blue_link_hover_color, command=None)
        send_button.place(x = self.width/2, y = self.height/2 + 20, anchor="center")

        link_return = customtkinter.CTkButton(self.screen, width=0, height=0, text="Voltar", command=self.create_login_screen, text_color=blue_link_color, fg_color="transparent", hover=False, cursor="hand2")
        link_return.place(x = self.width/2, y = self.height/2 + 60, anchor="center")

        self.screen.mainloop()

    def get_email(self):
        email = self.email_input.get()
        return email

    def get_password(self):
        password = self.password_input.get()
        return sha256(password.encode("utf-8")).hexdigest()
    
    def check_user(self):
        if self.get_password() == database.get_password_from_database(self.get_email()):
            print("Login feito com sucesso!")
            self.screen.destroy()
        else:
            print("Email ou senha incorretos!")
            messagebox.showerror("Erro", "Email ou senha incorretos")

class Manager():

    def __init__(self):
        self.width = 800
        self.height = 600
        self.screen = customtkinter.CTk()
        customtkinter.set_appearance_mode("dark")
        self.screen.resizable(False, False)

        # Centers the window
        screen_width = self.screen.winfo_screenwidth()
        screen_height = self.screen.winfo_screenheight()
        x = (screen_width / 2) - (self.width / 2)
        y = (screen_height / 2) -  ( self.height / 2)

        self.screen.geometry("%dx%d+%d+%d" % (self.width, self.height, x, y))

if __name__ == "__main__":
    Login().create_login_screen()