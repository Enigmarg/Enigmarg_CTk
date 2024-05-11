import customtkinter
from tkinter import messagebox
from database import Database
from hashlib import sha256

database = Database()
database.connect()

LIGHT_BLUE = "#0066CC"
DARK_BLUE = "#0059B3"
LIGHT_GRAY = "#2A2A2A"
DARK_GRAY = "#212121"

class Window():

    def clear_screen(window):
        for widget in window.screen.winfo_children():
            widget.destroy()

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

    def create_login_screen(self):
        Window.clear_screen(self)
        self.screen.title("Login")

        self.email_input = customtkinter.CTkEntry(self.screen, width=200, height=30, placeholder_text="E-mail")
        self.email_input.place(x=self.width/2, y=self.height/2 - 40, anchor="center")

        self.password_input = customtkinter.CTkEntry(self.screen, width=200, height=30, placeholder_text="Senha", show="*")
        self.password_input.place(x=self.width/2, y=self.height/2, anchor="center")

        login_btn = customtkinter.CTkButton(self.screen, width=200, height=30, text="Entrar", fg_color=LIGHT_BLUE, hover_color=DARK_BLUE, command=lambda: self.check_user())
        login_btn.place(x=self.width/2, y=self.height/2 + 40, anchor="center")

        forgot_password_btn = customtkinter.CTkButton(self.screen, width=0, height=0, text="Esqueceu a senha?", command=lambda: self.create_forgot_password_screen(), text_color=LIGHT_BLUE, fg_color="transparent", hover=False, cursor="hand2")
        forgot_password_btn.place(x=self.width/2, y=self.height/2 + 80, anchor="center")

        self.screen.mainloop()

    def create_forgot_password_screen(self):
        Window.clear_screen(self)
        self.screen.title("Login")

        self.email_input = customtkinter.CTkEntry(self.screen, width=200, height=30, placeholder_text="E-mail")
        self.email_input.place(x=self.width/2, y=self.height/2 - 20, anchor="center")

        send_btn = customtkinter.CTkButton(self.screen, width=200, height=30, text="Enviar", fg_color=LIGHT_BLUE, hover_color=DARK_BLUE, command=None)
        send_btn.place(x=self.width/2, y=self.height/2 + 20, anchor="center")

        return_btn = customtkinter.CTkButton(self.screen, width=0, height=0, text="Voltar", command=lambda: self.create_login_screen(), text_color=LIGHT_BLUE, fg_color="transparent", hover=False, cursor="hand2")
        return_btn.place(x=self.width/2, y=self.height/2 + 60, anchor="center")

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
        self.screen.title("Gerenciador")
        customtkinter.set_appearance_mode("dark")
        self.screen.resizable(False, False)

        # Centers the window
        screen_width = self.screen.winfo_screenwidth()
        screen_height = self.screen.winfo_screenheight()
        x = (screen_width / 2) - (self.width / 2)
        y = (screen_height / 2) -  ( self.height / 2)

        self.screen.geometry("%dx%d+%d+%d" % (self.width, self.height, x, y))


    def create_manager_user_screen(self):
        Window.clear_screen(self)

        options_frame = customtkinter.CTkFrame(self.screen, width=800, height=40, fg_color=DARK_GRAY, corner_radius=0)
        options_frame.pack(side=customtkinter.TOP)
        options_frame.pack_propagate(False)

        users_btn = customtkinter.CTkButton(options_frame, width=150, height=40, text="Usuários", font=("Arial", 15, "bold"), fg_color=LIGHT_GRAY, hover=False, cursor="hand2", corner_radius=0)
        users_btn.place(x=75, y=20, anchor="center")
        
        questions_btn = customtkinter.CTkButton(options_frame, width=150, height=40, text="Questões", font=("Arial", 15, "bold"), command=lambda: self.create_manager_question_screen(), fg_color=DARK_GRAY, hover=False, cursor="hand2", corner_radius=0)
        questions_btn.place(x=225, y=20, anchor="center") 

        
        main_frame = customtkinter.CTkFrame(self.screen, width=self.width, height=self.height, fg_color=LIGHT_GRAY)
        main_frame.pack()
        main_frame.pack_propagate(False)

        entrys_frame = customtkinter.CTkFrame(main_frame, width=self.width/2 - 20, height=self.height - 150, fg_color=DARK_GRAY)
        entrys_frame.place(x=200, y=240, anchor="center")

        table_frame = customtkinter.CTkFrame(main_frame, width=self.width/2 - 10, height=self.height - 150, fg_color=DARK_GRAY)
        table_frame.place(x=595, y=240, anchor="center")

        buttons_frame = customtkinter.CTkFrame(main_frame, width=self.width - 20, height=self.height/8, fg_color=DARK_GRAY)
        buttons_frame.place(x=400, y=510, anchor="center")

        self.screen.mainloop()

    def create_manager_question_screen(self):
        Window.clear_screen(self)

        options_frame = customtkinter.CTkFrame(self.screen, width=800, height=40, fg_color=DARK_GRAY, corner_radius=0)
        options_frame.pack(side=customtkinter.TOP)
        options_frame.pack_propagate(False)

        users_btn = customtkinter.CTkButton(options_frame, text="Usuários", width=150, height=40, font=("Arial", 15, "bold"), command=lambda: self.create_manager_user_screen(), fg_color=DARK_GRAY, hover=False, cursor="hand2", corner_radius=0)
        users_btn.place(x=75, y=20, anchor="center")

        main_frame = customtkinter.CTkFrame(self.screen, width=self.width, height=self.height, fg_color=LIGHT_GRAY)
        main_frame.pack()
        main_frame.pack_propagate(False)

        
        questions_btn = customtkinter.CTkButton(options_frame, text="Questões", width=150, height=40, font=("Arial", 15, "bold"), fg_color=LIGHT_GRAY, hover=False, cursor="hand2", corner_radius=0)
        questions_btn.place(x=225, y=20, anchor="center") 

        self.screen.mainloop()

if __name__ == "__main__":
    # Login().create_login_screen()
    Manager().create_manager_user_screen()