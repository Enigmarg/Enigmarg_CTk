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

    def add_users_to_treeview(self):
        users = database.get_all_users()
        self.user_tree.delete(*self.user_tree.get_children())
        for user in users:
            self.user_tree.insert("", "end", values=user)

    def clear_user(self, *clicked):
        if clicked:
            self.user_tree.selection_remove(self.user_tree.focus())
        self.email_entry.delete(0, "end")
        self.password_entry.delete(0, "end")
        self.role_option.set("Aluno")

    def display_user(self, event):
        selected_items = self.user_tree.focus()
        if selected_items:
            row = self.user_tree.item(selected_items)["values"]
            self.clear_user()
            self.email_entry.insert(0, row[0])
            self.role_option.set(row[1])

    def add_user(self):
        email = self.get_email()
        password = self.get_password()
        role = self.get_role()
        
        if not (email and password and role):
            messagebox.showerror("Erro", "Preencha todos os campos.")
        else:
            database.add_user(email, password, role)
            self.add_users_to_treeview()
            self.clear_user()

    def delete_user(self):
        email = self.get_email()
        database.delete_user(email)
        self.add_users_to_treeview()
        self.clear_user()

    def update_user(self):
        email = self.get_email()
        password = self.get_password()
        role = self.get_role()
        if (email and password and role):
            database.update_user(email, password, role)
            self.add_users_to_treeview()
            self.clear_user()
        elif (email and role):
            database.update_user(email, None, role)
            self.add_users_to_treeview()
            self.clear_user()

    def add_questions_to_treeview(self):
        questions = database.get_all_questions()
        self.question_tree.delete(*self.question_tree.get_children())
        for question in questions:
            self.question_tree.insert("", "end", values=question)

    def clear_question(self, *clicked):
        if clicked:
            self.question_tree.selection_remove(self.question_tree.focus())
        self.question_text.delete(1.0, "end")
        self.alter1_entry.delete(1.0, "end")
        self.alter2_entry.delete(1.0, "end")
        self.alter3_entry.delete(1.0, "end")
        self.answer_entry.delete(1.0, "end")
        self.difficulty_option.set("Fácil")

    def display_question(self, event):
        selected_items = self.question_tree.focus()
        if selected_items:
            row = self.question_tree.item(selected_items)["values"]
            self.clear_question()
            self.question_text.insert(1.0, row[0])
            self.alter1_entry.insert(1.0, row[1])
            self.alter2_entry.insert(1.0, row[2])
            self.alter3_entry.insert(1.0, row[3])
            self.answer_entry.insert(1.0, row[4])

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

        add_user_btn = customtkinter.CTkButton(tabView.tab("Usuários"), text="Adicionar", width=90, height=40, corner_radius=50, font=BOLD_FONT, text_color="royal blue", fg_color="transparent", border_width=1, border_color="royal blue", hover=False, command=self.add_user, cursor="hand2")
        add_user_btn.place(x=90, y=370, anchor="center")

        update_user_btn = customtkinter.CTkButton(tabView.tab("Usuários"), text="Atualizar", width=90, height=40, corner_radius=50, font=BOLD_FONT, text_color="royal blue", fg_color="transparent", border_width=1, border_color="royal blue", hover=False, command=self.update_user,  cursor="hand2")
        update_user_btn.place(x=192, y=370, anchor="center")

        delete_user_btn = customtkinter.CTkButton(tabView.tab("Usuários"), text="Deletar", width=90, height=40, corner_radius=50, font=BOLD_FONT, fg_color="royal blue", hover=False, command=self.delete_user,  cursor="hand2")
        delete_user_btn.place(x=290, y=370, anchor="center")

        # TreeView
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", font=("Arial", 13, "normal"), background="gray15", foreground="white", fieldbackground="gray15")
        style.map("Treeview", background=[("selected", "royal blue")])
        self.user_tree = ttk.Treeview(tabView.tab("Usuários"))
        self.user_tree["column"] = ("Email", "Cargo")

        self.user_tree.column("#0", width=0, stretch=tk.NO)
        self.user_tree.column("Email", anchor=tk.CENTER, width=150)
        self.user_tree.column("Cargo", anchor=tk.CENTER, width=150)

        self.user_tree.heading("Email", text="Email")
        self.user_tree.heading("Cargo", text="Cargo")

        self.user_tree.place(relx=0.53, rely=0.07, relwidth=0.45, relheight=0.79)

        # Entrys
        question_label = customtkinter.CTkLabel(tabView.tab("Questões"), text="Pergunta:")
        question_label.place(relx=0.02, rely=0.03)
        self.question_text = customtkinter.CTkTextbox(tabView.tab("Questões"), width=250, height=150, fg_color="gray25")
        self.question_text.place(relx=0.02, rely=0.1)

        answer_label = customtkinter.CTkLabel(tabView.tab("Questões"), text="Alternativas:")
        answer_label.place(relx=0.35, rely=0.03)

        self.alter1_entry = customtkinter.CTkTextbox(tabView.tab("Questões"), width=230, height=45, fg_color="gray25", border_width=0)
        self.alter1_entry.place(relx=0.35, rely=0.1)

        self.alter2_entry = customtkinter.CTkTextbox(tabView.tab("Questões"), width=230, height=45, fg_color="gray25", border_width=0)
        self.alter2_entry.place(relx=0.35, rely=0.217)

        self.alter3_entry = customtkinter.CTkTextbox(tabView.tab("Questões"), width=230, height=45, fg_color="gray25", border_width=0)
        self.alter3_entry.place(relx=0.35, rely=0.335)

        answer_label = customtkinter.CTkLabel(tabView.tab("Questões"), text="Resposta:")
        answer_label.place(relx=0.66, rely=0.265)
        self.answer_entry = customtkinter.CTkTextbox(tabView.tab("Questões"), width=230, height=45, fg_color="gray25", border_width=0)
        self.answer_entry.place(relx=0.66, rely=0.335)

        difficulty_label = customtkinter.CTkLabel(tabView.tab("Questões"), text="Dificuldade:")
        difficulty_label.place(relx=0.66, rely=0.03)
        self.difficulty_option = customtkinter.CTkOptionMenu(tabView.tab("Questões"), values=["Fácil", "Médio", "Difícil"], width=50, height=45, fg_color="gray25", button_color="gray25", hover=False)
        self.difficulty_option.place(relx=0.66, rely=0.1)

        add_question_btn = customtkinter.CTkButton(tabView.tab("Questões"), text="Adicionar", width=165, height=35, corner_radius=50, font=BOLD_FONT, fg_color="royal blue", hover=False, command=None, cursor="hand2")
        add_question_btn.place(relx=0.15, rely=0.47)

        update_question_btn = customtkinter.CTkButton(tabView.tab("Questões"), text="Atualizar", width=165, height=35, corner_radius=50, font=BOLD_FONT, fg_color="royal blue", hover=False, command=None,  cursor="hand2")
        update_question_btn.place(relx=0.4, rely=0.47)

        delete_question_btn = customtkinter.CTkButton(tabView.tab("Questões"), text="Deletar", width=165, height=35, corner_radius=50, font=BOLD_FONT, fg_color="royal blue", hover=False, command=None,  cursor="hand2")
        delete_question_btn.place(relx=0.65, rely=0.47)

        clear_question_btn = customtkinter.CTkButton(tabView.tab("Questões"), text="Limpar", width=120, height=40, corner_radius=50, font=BOLD_FONT, text_color="royal blue", fg_color="transparent", border_width=1, border_color="royal blue", hover=False, command=self.clear_question,cursor="hand2")
        clear_question_btn.place(relx=0.8, rely=0.1)

        # TreeView
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", font=("Arial", 13, "normal"), background="gray15", foreground="white", fieldbackground="gray15")
        style.map("Treeview", background=[("selected", "royal blue")])
        self.question_tree = ttk.Treeview(tabView.tab("Questões"))
        self.question_tree["column"] = ("Pergunta", "Alternativa1", "Alternativa2", "Alternativa3", "Resposta")

        self.question_tree.column("#0", width=0, stretch=tk.NO)
        self.question_tree.column("Pergunta", anchor=tk.CENTER, width=60)
        self.question_tree.column("Alternativa1", anchor=tk.CENTER, width=60)
        self.question_tree.column("Alternativa2", anchor=tk.CENTER, width=60)
        self.question_tree.column("Alternativa3", anchor=tk.CENTER, width=60)
        self.question_tree.column("Resposta", anchor=tk.CENTER, width=60)

        self.question_tree.heading("Pergunta", text="Pergunta")
        self.question_tree.heading("Alternativa1", text="Alternativa")
        self.question_tree.heading("Alternativa2", text="Alternativa")
        self.question_tree.heading("Alternativa3", text="Alternativa")
        self.question_tree.heading("Resposta", text="Resposta")

        self.question_tree.place(relx=0, rely=0.6, relwidth=1, relheight=0.4)


        self.user_tree.bind("<ButtonRelease>", self.display_user)
        self.question_tree.bind("<ButtonRelease>", self.display_question)
        self.add_users_to_treeview()
        self.add_questions_to_treeview()
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