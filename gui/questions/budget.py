import tkinter as tk
from tkinter import ttk, messagebox


class BudgetPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        container = tk.Frame(self)
        container.place(relx=0.5, rely=0.5, anchor="center")

        label = tk.Label(
            container,
            text="Budget level:",
            font=("Arial", 14),
        )
        label.pack(pady=20)

        self.budget_level_var = tk.StringVar()

        budget_levels = [
            ("Very tight budget", "1"),
            ("Moderate budget", "2"),
            ("Flexible budget", "3"),
        ]

        rb_frame = tk.Frame(container)
        rb_frame.pack(pady=10)

        for text, value in budget_levels:
            rb = ttk.Radiobutton(
                rb_frame,
                text=text,
                variable=self.budget_level_var,
                value=value,
            )
            rb.pack(anchor="w", padx=10, pady=5)

        # Navigation buttons
        nav_frame = tk.Frame(container)
        nav_frame.pack(side="bottom", pady=20)

        next_btn = ttk.Button(
            nav_frame,
            text="Next",
            command=self.next_page,
            cursor="hand2",
        )
        next_btn.pack(side="right", padx=10, ipady=8)

    def next_page(self):
        if not self.budget_level_var.get():
            messagebox.showwarning(
                "Selection Required", "Please select your budget level"
            )
            return

        self.controller.update_prefs("budget_level", self.budget_level_var.get())
        next_frame = self.controller.get_next_frame(BudgetPage)
        self.controller.show_frame(next_frame)
