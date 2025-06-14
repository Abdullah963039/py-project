import tkinter as tk
from tkinter import ttk


class WelcomePage(tk.Frame):
    def __init__(self, parent, controller):
        from gui.questions.category import CategoryPage

        tk.Frame.__init__(self, parent)
        self.controller = controller

        container = tk.Frame(self)
        container.place(relx=0.5, rely=0.5, anchor="center")

        label = tk.Label(
            container,
            text="Welcome to the Recipe Recommendation System!",
            font=("Arial", 18, "bold"),
        )
        label.pack(pady=20)

        desc = tk.Label(
            container,
            text="This system will help you find the perfect recipes based on your preferences.",
            wraplength=600,
            justify="center",
            font=("Arial", 11)
        )
        desc.pack(pady=10)

        start_btn = ttk.Button(
            container,
            text="Start",
            command=lambda: controller.show_frame(CategoryPage),
            width=32,
            cursor="hand2",
        )
        start_btn.pack(ipady=8, pady=20)
