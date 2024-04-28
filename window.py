import customtkinter

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

    def create_username_input(self):
        self.username_input = customtkinter.CTkEntry(self.screen, width=200, height=30, placeholder_text="Nome de usuário")
        self.username_input.place(x=WIDTH/2, y=HEIGHT/2 - 40, anchor="center")

    def create_password_input(self):
        self.password_input = customtkinter.CTkEntry(self.screen, width=200, height=30, placeholder_text="Senha", show="*")
        self.password_input.place(x=WIDTH/2, y=HEIGHT/2, anchor="center")

    def create_email_input(self):
        self.email_input = customtkinter.CTkEntry(self.screen, width=200, height=30, placeholder_text="E-mail")
        self.email_input.place(x=WIDTH/2, y=HEIGHT/2 - 80, anchor="center")

    def create_button(self, text):
        login_button = customtkinter.CTkButton(self.screen, width=200, height=30, text=text, fg_color=blue_link_color, hover_color=blue_link_hover_color)
        login_button.place(x=WIDTH/2, y=HEIGHT/2 + 40, anchor="center")

    def create_login_link(self):
        login_link_label = customtkinter.CTkLabel(self.screen, text="Já tem um conta?")
        login_link_label.place(x=WIDTH/2 - 40, y=HEIGHT/2 + 80, anchor="center")
         
        login_link_button = customtkinter.CTkButton(self.screen, width=0, height=0, text="Fazer login", command=self.create_login_widgets, text_color=blue_link_color, fg_color="transparent", hover=False, cursor="hand2")
        login_link_button.place(x=WIDTH/2 + 50, y=HEIGHT/2 + 80, anchor="center")

    def create_register_link(self):
        register_link_label = customtkinter.CTkLabel(self.screen, text="Não tem uma conta?")
        register_link_label.place(x=WIDTH/2 - 35, y=HEIGHT/2 + 80, anchor="center")

        register_link_button = customtkinter.CTkButton(self.screen, width=0, height=0, text="Criar conta", command=self.create_register_widgets, text_color=blue_link_color, fg_color="transparent", hover=False, cursor="hand2")
        register_link_button.place(x=WIDTH/2 + 60, y=HEIGHT/2 + 80, anchor="center")            

    def clear_window(self):
        for widget in self.screen.winfo_children():
            widget.destroy()

    def create_login_widgets(self):
        self.clear_window()
        self.screen.title("Login")

        self.create_username_input()
        self.create_password_input()
        self.create_button("Login")
        self.create_register_link()

    def create_register_widgets(self):
        self.clear_window()
        self.screen.title("Registro")

        self.create_email_input()
        self.create_username_input()
        self.create_password_input()
        self.create_button("Registrar")
        self.create_login_link()

    def create_main_screen(self):
        self.create_login_widgets()
        self.screen.mainloop()

if __name__ == "__main__":
    Window().create_main_screen()