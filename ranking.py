import customtkinter
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from database import Database

database = Database()
database.connect()
BOLD_FONT = ("Arial", 12, "bold")

class Ranking():

    def __init__(self):
        self.width = 800
        self.height = 600
        self.screen = customtkinter.CTk()
        self.screen.configure(fg_color="royal blue")
        self.screen.title("Ranking")
        customtkinter.set_appearance_mode("dark")
        self.screen.resizable(False, False)

        # Centers the window
        screen_width = self.screen.winfo_screenwidth()
        screen_height = self.screen.winfo_screenheight()
        x = (screen_width / 2) - (self.width / 2)
        y = (screen_height / 2) -  ( self.height / 2)

        self.screen.geometry("%dx%d+%d+%d" % (self.width, self.height, x, y))

        self.email_labels = []
        self.score_labels = []
    
    def add_email_in_label(self):
         for i, email in enumerate(database.get_email_ranking()):
                label = tk.Label(self.screen, text=email, font=BOLD_FONT, width=20, height=2, border=2, bg="white")
                label.place(x=350, y=60*i+10)
                self.email_labels.append(label)
    
    def add_score_in_label(self):
         for i, score in enumerate(database.get_score_ranking()):
                label = tk.Label(self.screen, text=score, font=BOLD_FONT, width=20, height=2, border=2, bg="white")
                label.place(x=550, y=60*i+10)
                self.score_labels.append(label)


    def create_ranking_screen(self):
        self.add_email_in_label()
        self.add_score_in_label()

        self.screen.mainloop()

Ranking().create_ranking_screen()