import customtkinter
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from database import Database
from hashlib import sha256

database = Database()
database.connect()

BOLD_FONT = ("Arial", 15, "bold")
NORMAL_FONT = ("Arial", 15, "normal")

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

        login_btn = customtkinter.CTkButton(self.screen, width=200, height=30, text="Entrar", fg_color="royal blue", hover=False, command=lambda: self.check_user())
        login_btn.place(x=self.width/2, y=self.height/2 + 40, anchor="center")

        forgot_password_btn = customtkinter.CTkButton(self.screen, width=0, height=0, text="Esqueceu a senha?", command=lambda: self.create_forgot_password_screen(), text_color="royal blue", fg_color="transparent", hover=False, cursor="hand2")
        forgot_password_btn.place(x=self.width/2, y=self.height/2 + 80, anchor="center")

        self.screen.mainloop()

    def create_forgot_password_screen(self):
        Window.clear_screen(self)
        self.screen.title("Login")

        self.email_input = customtkinter.CTkEntry(self.screen, width=200, height=30, placeholder_text="E-mail")
        self.email_input.place(x=self.width/2, y=self.height/2 - 20, anchor="center")

        send_btn = customtkinter.CTkButton(self.screen, width=200, height=30, text="Enviar", fg_color="royal blue", hover=False, command=None, cursor="hand2")
        send_btn.place(x=self.width/2, y=self.height/2 + 20, anchor="center")

        return_btn = customtkinter.CTkButton(self.screen, width=0, height=0, text="Voltar", command=lambda: self.create_login_screen(), text_color="royal blue", fg_color="transparent", hover=False, cursor="hand2")
        return_btn.place(x=self.width/2, y=self.height/2 + 60, anchor="center")

        self.screen.mainloop()

    def get_email(self):
        email = self.email_input.get()
        return email

    def get_password(self):
        password = self.password_input.get()
        return sha256(password.encode("utf-8")).hexdigest()
    
    def check_user(self):
        if self.get_password() == database.get_user_password(self.get_email()):
            print("Login feito com sucesso!")
            self.screen.destroy()
        else:
            print("Email ou senha incorretos!")
            messagebox.showerror("Erro", "Email ou senha incorretos")

class Manager():

    def __init__(self):
        self.width = 800
        self.height = 500
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

    def add_to_treeview(self):
        users = database.get_all_users()
        self.tree.delete(*self.tree.get_children())
        for user in users:
            self.tree.insert("", "end", values=user)

    def create_manager_screen(self):

        # TabView
        tabView = customtkinter.CTkTabview(self.screen, width=self.width - 70, height=self.height - 20)
        tabView.pack()
        tabView.add("Usuários")
        tabView.add("Questões")

        # Entrys
        email_label = customtkinter.CTkLabel(tabView.tab("Usuários"), text="E-mail:", font=NORMAL_FONT)
        email_label.place(x=45, y=30)
        email_entry = customtkinter.CTkEntry(tabView.tab("Usuários"), width=300, height=40)
        email_entry.place(x=190, y=80, anchor="center")

        password_label = customtkinter.CTkLabel(tabView.tab("Usuários"), text="Senha:", font=NORMAL_FONT)
        password_label.place(x=45, y=120)
        password_entry = customtkinter.CTkEntry(tabView.tab("Usuários"), width=300, height=40, show="*")
        password_entry.place(x=190, y=170, anchor="center")

        role_label = customtkinter.CTkLabel(tabView.tab("Usuários"), text="Cargo:", font=NORMAL_FONT)
        role_label.place(x=45, y=210)
        role_option = customtkinter.CTkOptionMenu(tabView.tab("Usuários"), values=["Aluno", "Professor"], width=300, height=40, fg_color="gray30", button_color="gray23", hover=False)
        role_option.place(x=190, y=260, anchor="center")

        add_btn = customtkinter.CTkButton(tabView.tab("Usuários"), text="Adicionar", width=90, height=40, corner_radius=50, fg_color="steel blue", hover=False, command=self.add_to_treeview, cursor="hand2")
        add_btn.place(x=90, y=370, anchor="center")

        update_btn = customtkinter.CTkButton(tabView.tab("Usuários"), text="Atualizar", width=90, height=40, corner_radius=50, fg_color="steel blue", hover=False, cursor="hand2")
        update_btn.place(x=192, y=370, anchor="center")

        delete_btn = customtkinter.CTkButton(tabView.tab("Usuários"), text="Deletar", width=90, height=40, corner_radius=50, fg_color="steel blue", hover=False, cursor="hand2")
        delete_btn.place(x=290, y=370, anchor="center")

        # TreeView
        self.tree = ttk.Treeview(tabView.tab("Usuários"), height=17)
        self.tree["column"] = ("Email", "Cargo")

        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("Email", anchor=tk.CENTER, width=150)
        self.tree.column("Cargo", anchor=tk.CENTER, width=150)

        self.tree.heading("Email", text="Email")
        self.tree.heading("Cargo", text="Cargo")

        self.tree.place(x=380, y=30)

        self.add_to_treeview()
        self.screen.mainloop()

if __name__ == "__main__":
    # Login().create_login_screen()
    Manager().create_manager_screen()