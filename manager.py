import customtkinter
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from database import Database
from hashlib import sha256

BOLD_FONT = ("Arial", 12, "bold")

class Manager():

    def __init__(self):
        self.width = 800
        self.height = 500
        self.screen = customtkinter.CTk()
        self.screen.configure(fg_color="gray15")
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

    def clear(self, *clicked):
        if clicked:
            self.tree.selection_remove(self.tree.focus())
        self.email_entry.delete(0, "end")
        self.password_entry.delete(0, "end")
        self.role_option.set("Aluno")

    def display_user(self, event):
        selected_items = self.tree.focus()
        if selected_items:
            row = self.tree.item(selected_items)["values"]
            self.clear()
            self.email_entry.insert(0, row[0])
            self.role_option.set(row[1])
        else:
            pass

    def add_user(self):
        email = self.get_email()
        password = self.get_password()
        role = self.get_role()
        
        if not (email and password and role):
            messagebox.showerror("Erro", "Preencha todos os campos.")
        else:
            database.add_user(email, password, role)
            self.add_to_treeview()
            self.clear()

    def delete_user(self):
        email = self.get_email()
        database.delete_user(email)
        self.add_to_treeview()
        self.clear()

    def update_user(self):
        email = self.get_email()
        password = self.get_password()
        role = self.get_role()
        if (email and password and role):
            database.update_user(email, password, role)
            self.add_to_treeview()
            self.clear()
        elif (email and role):
            database.update_user(email, None, role)
            self.add_to_treeview()
            self.clear()

    def create_manager_screen(self):

        # TabView
        tabView = customtkinter.CTkTabview(self.screen, width=self.width, height=self.height, fg_color="gray15", segmented_button_selected_color="royal blue", segmented_button_selected_hover_color="royal blue")
        tabView.pack()
        tabView.add("Usuários")
        tabView.add("Questões")

        # Entrys
        email_label = customtkinter.CTkLabel(tabView.tab("Usuários"), text="E-mail:")
        email_label.place(x=45, y=30)
        self.email_entry = customtkinter.CTkEntry(tabView.tab("Usuários"), width=300, height=40, fg_color="gray25", border_width=0)
        self.email_entry.place(x=190, y=80, anchor="center")

        password_label = customtkinter.CTkLabel(tabView.tab("Usuários"), text="Senha:")
        password_label.place(x=45, y=120)
        self.password_entry = customtkinter.CTkEntry(tabView.tab("Usuários"), width=300, height=40, show="*", fg_color="gray25", border_width=0)
        self.password_entry.place(x=190, y=170, anchor="center")

        role_label = customtkinter.CTkLabel(tabView.tab("Usuários"), text="Cargo:")
        role_label.place(x=45, y=210)
        self.role_option = customtkinter.CTkOptionMenu(tabView.tab("Usuários"), values=["Aluno", "Professor"], width=300, height=40, fg_color="gray25", button_color="gray25", hover=False)
        self.role_option.place(x=190, y=260, anchor="center")

        add_btn = customtkinter.CTkButton(tabView.tab("Usuários"), text="Adicionar", width=90, height=40, corner_radius=50, font=BOLD_FONT, text_color="royal blue", fg_color="transparent", border_width=1, border_color="royal blue", hover=False, command=self.add_user, cursor="hand2")
        add_btn.place(x=90, y=370, anchor="center")

        update_btn = customtkinter.CTkButton(tabView.tab("Usuários"), text="Atualizar", width=90, height=40, corner_radius=50, font=BOLD_FONT, text_color="royal blue", fg_color="transparent", border_width=1, border_color="royal blue", hover=False, command=self.update_user,  cursor="hand2")
        update_btn.place(x=192, y=370, anchor="center")

        delete_btn = customtkinter.CTkButton(tabView.tab("Usuários"), text="Deletar", width=90, height=40, corner_radius=50, font=BOLD_FONT, fg_color="royal blue", hover=False, command=self.delete_user,  cursor="hand2")
        delete_btn.place(x=290, y=370, anchor="center")

        # TreeView
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", font=("Arial", 13, "normal"), background="gray15", foreground="white", fieldbackground="gray15")
        style.map("Treeview", background=[("selected", "royal blue")])
        self.tree = ttk.Treeview(tabView.tab("Usuários"))
        self.tree["column"] = ("Email", "Cargo")

        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("Email", anchor=tk.CENTER, width=150)
        self.tree.column("Cargo", anchor=tk.CENTER, width=150)

        self.tree.heading("Email", text="Email")
        self.tree.heading("Cargo", text="Cargo")

        self.tree.place(relx=0.53, rely=0.07, relwidth=0.45, relheight=0.79)

        question_label = customtkinter.CTkLabel(tabView.tab("Questões"), text="Pergunta:")
        question_label.place(relx=0.02, rely=0.02)
        self.question_text = customtkinter.CTkTextbox(tabView.tab("Questões"), width=250, height=150, fg_color="gray25")
        self.question_text.place(relx=0.02, rely=0.1)

        answer_label = customtkinter.CTkLabel(tabView.tab("Questões"), text="Alternativas:")
        answer_label.place(relx=0.38, rely=0.02)

        answer1_label = customtkinter.CTkLabel(tabView.tab("Questões"), text="1.")
        answer1_label.place(relx=0.38, rely=0.14)
        self.answer1_entry = customtkinter.CTkTextbox(tabView.tab("Questões"), width=140, height=65, fg_color="gray25", border_width=0)
        self.answer1_entry.place(relx=0.4, rely=0.1)

        answer2_label = customtkinter.CTkLabel(tabView.tab("Questões"), text="2.")
        answer2_label.place(relx=0.62, rely=0.14)
        self.answer2_entry = customtkinter.CTkTextbox(tabView.tab("Questões"), width=140, height=65, fg_color="gray25", border_width=0)
        self.answer2_entry.place(relx=0.64, rely=0.1)

        answer3_label = customtkinter.CTkLabel(tabView.tab("Questões"), text="3.")
        answer3_label.place(relx=0.38, rely=0.33)
        self.answer3_entry = customtkinter.CTkTextbox(tabView.tab("Questões"), width=140, height=65, fg_color="gray25", border_width=0)
        self.answer3_entry.place(relx=0.4, rely=0.29)

        answer4_label = customtkinter.CTkLabel(tabView.tab("Questões"), text="4.")
        answer4_label.place(relx=0.62, rely=0.33)
        self.answer4_entry = customtkinter.CTkTextbox(tabView.tab("Questões"), width=140, height=65, fg_color="gray25", border_width=0)
        self.answer4_entry.place(relx=0.64, rely=0.29)

        answer_label = customtkinter.CTkLabel(tabView.tab("Questões"), text="Resposta:")
        answer_label.place(relx=0.85, rely=0.02)
        self.answer_option = customtkinter.CTkOptionMenu(tabView.tab("Questões"), values=["1", "2", "3", "4"], width=5, height=40, fg_color="gray25", button_color="gray25", hover=False)
        self.answer_option.place(relx=0.85, rely=0.1)


        self.tree.bind("<ButtonRelease>", self.display_user)
        self.add_to_treeview()
        self.screen.mainloop()

    def get_email(self):
        email = self.email_entry.get()
        return email
    
    def get_password(self):
        password = self.password_entry.get()
        if password == "":
            return password
        else:
           return sha256(password.encode("utf-8")).hexdigest() 
    
    def get_role(self):
        role = self.role_option.get()   
        return role
    
if __name__ == "__main__":
    database = Database()
    database.connect()
    Manager().create_manager_screen()