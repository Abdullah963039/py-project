import tkinter as tk
from tkinter import ttk, messagebox


class HealthyPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        container = tk.Frame(self)
        container.place(relx=0.5, rely=0.5, anchor="center")

        label = tk.Label(
            container,
            text="Health focus?",
            font=("Arial", 14),
        )
        label.pack(pady=20)

        self.health_focus_var = tk.StringVar()

        health_focus = [
            ("Balanced nutrition", "balanced"),
            ("Low carb", "low_carb"),
            ("Low fat", "low_fat"),
        ]

        rb_frame = tk.Frame(container)
        rb_frame.pack(pady=10)

        for text, value in health_focus:
            rb = ttk.Radiobutton(
                rb_frame,
                text=text,
                variable=self.health_focus_var,
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
        if not self.health_focus_var.get():
            messagebox.showwarning(
                "Selection Required", "Please select your healthy focus"
            )
            return

        self.controller.update_prefs("health_focus", self.health_focus_var.get())
        next_frame = self.controller.get_next_frame(HealthyPage)
        self.controller.show_frame(next_frame)
