import tkinter as tk
from tkinter import ttk

from data.constants import DIETARY_TAGS


class DietaryPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        container = tk.Frame(self)
        container.place(relx=0.5, rely=0.5, anchor="center")

        label = tk.Label(
            container,
            text="Any dietary restrictions or preferences?",
            font=("Arial", 14),
        )
        label.pack(pady=20)

        self.diet_vars = {}

        for diet in DIETARY_TAGS:
            var = tk.IntVar()
            cb = ttk.Checkbutton(container, text=diet, variable=var)
            cb.pack(anchor="w", padx=50, pady=5)
            self.diet_vars[diet] = var

        nav_frame = tk.Frame(container)
        nav_frame.pack(side="bottom", pady=20)

        prev_btn = ttk.Button(
            nav_frame,
            text="Back",
            command=lambda: controller.show_frame(
                controller.get_prev_frame(DietaryPage)
            ),
            cursor="hand2",
        )
        prev_btn.pack(side="left", padx=10, ipady=6)

        next_btn = ttk.Button(
            nav_frame, text="Next", command=self.next_page, cursor="hand2"
        )
        next_btn.pack(side="right", padx=10, ipady=6)

    def next_page(self):
        selected_diets = [diet for diet, var in self.diet_vars.items() if var.get()]
        if selected_diets:
            self.controller.update_prefs("dietary_restrictions", selected_diets)

        next_frame = self.controller.get_next_frame(DietaryPage)
        self.controller.show_frame(next_frame)
