import customtkinter
from tkinter import messagebox
from database import Database
from hashlib import sha256

database = Database()
database.connect()

WIDTH = 380
HEIGHT = 450

blue_link_color = "#0066CC"
blue_link_hover_color = "#0059B3"

class Window():
    def __init__(self):
        self.screen = customtkinter.CTk()
        customtkinter.set_appearance_mode("dark")
        self.screen.resizable(False, False)

        # Centers the window
        screen_width = self.screen.winfo_screenwidth()
        screen_height = self.screen.winfo_screenheight()
        x = (screen_width / 2) - (WIDTH / 2)
        y = (screen_height / 2) - (HEIGHT / 2)

        self.screen.geometry("%dx%d+%d+%d" % (WIDTH, HEIGHT, x, y))

    def create_email_input(self, x=0, y=0):
        self.email_input = customtkinter.CTkEntry(self.screen, width=200, height=30, placeholder_text="E-mail")
        self.email_input.place(x=x, y=y, anchor="center")

    def create_password_input(self):
        self.password_input = customtkinter.CTkEntry(self.screen, width=200, height=30, placeholder_text="Senha", show="*")
        self.password_input.place(x=WIDTH/2, y=HEIGHT/2, anchor="center")

    def create_button(self, text, command):
        login_button = customtkinter.CTkButton(self.screen, width=200, height=30, text=text, fg_color=blue_link_color, hover_color=blue_link_hover_color, command=command)
        login_button.place(x=WIDTH/2, y=HEIGHT/2 + 40, anchor="center")

    def link_forgot_password(self, command):
        login_link_button = customtkinter.CTkButton(self.screen, width=0, height=0, text="Esqueceu a senha?", command=command, text_color=blue_link_color, fg_color="transparent", hover=False, cursor="hand2")
        login_link_button.place(x=WIDTH/2, y=HEIGHT/2 + 80, anchor="center")

    def clear_window(self):
        for widget in self.screen.winfo_children():
            widget.destroy()

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

    def create_login_widgets(self):
        self.clear_window()
        self.screen.title("Login")

        self.create_email_input(x=WIDTH/2, y=HEIGHT/2-40)
        self.create_password_input()
        self.create_button("Login", self.check_user)
        self.link_forgot_password(None)
        self.screen.mainloop()

if __name__ == "__main__":
    Window().create_login_widgets()