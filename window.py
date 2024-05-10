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

    def clear_window(self):
        for widget in self.screen.winfo_children():
            widget.destroy()

    def create_login_screen(self):
        self.clear_window()
        self.screen.title("Login")

        self.email_input = customtkinter.CTkEntry(self.screen, width=200, height=30, placeholder_text="E-mail")
        self.email_input.place(x = WIDTH/2, y = HEIGHT/2-40, anchor="center")

        self.password_input = customtkinter.CTkEntry(self.screen, width=200, height=30, placeholder_text="Senha", show="*")
        self.password_input.place(x=WIDTH/2, y=HEIGHT/2, anchor="center")

        login_button = customtkinter.CTkButton(self.screen, width=200, height=30, text="Login", fg_color=blue_link_color, hover_color=blue_link_hover_color, command=None)
        login_button.place(x=WIDTH/2, y=HEIGHT/2 + 40, anchor="center")

        login_link_button = customtkinter.CTkButton(self.screen, width=0, height=0, text="Esqueceu a senha?", command=None, text_color=blue_link_color, fg_color="transparent", hover=False, cursor="hand2")
        login_link_button.place(x=WIDTH/2, y=HEIGHT/2 + 80, anchor="center")

        self.screen.mainloop()

    def create_forgot_password_screen(self):
        self.clear_window()
        self.screen.title("Login")

        self.email_input = customtkinter.CTkEntry(self.screen, width=200, height=30, placeholder_text="E-mail")
        self.email_input.place(x = WIDTH/2, y = HEIGHT/2-20, anchor="center")

        login_button = customtkinter.CTkButton(self.screen, width=200, height=30, text="Enviar", fg_color=blue_link_color, hover_color=blue_link_hover_color, command=None)
        login_button.place(x=WIDTH/2, y=HEIGHT/2 + 20, anchor="center")

        login_link_button = customtkinter.CTkButton(self.screen, width=0, height=0, text="Voltar", command=None, text_color=blue_link_color, fg_color="transparent", hover=False, cursor="hand2")
        login_link_button.place(x=WIDTH/2, y=HEIGHT/2 + 60, anchor="center")

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

if __name__ == "__main__":
    Window().create_forgot_password_screen()