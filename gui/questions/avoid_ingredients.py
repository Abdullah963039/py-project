import tkinter as tk
from tkinter import ttk


class AvoidIngredientsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        container = tk.Frame(self)
        container.place(relx=0.5, rely=0.5, anchor="center")

        label = tk.Label(
            container,
            text="Any ingredients to avoid? (comma separated)",
            font=("Arial", 14),
        )
        label.pack(pady=20)

        self.avoid_entry = ttk.Entry(container, width=40, font=("Arial", 13))
        self.avoid_entry.pack(pady=10, ipady=6)

        nav_frame = tk.Frame(container)
        nav_frame.pack(side="bottom", pady=20)

        prev_btn = ttk.Button(
            nav_frame,
            text="Back",
            command=lambda: controller.show_frame(
                controller.get_prev_frame(AvoidIngredientsPage)
            ),
            cursor="hand2",
        )
        prev_btn.pack(side="left", padx=10, ipady=6)

        next_btn = ttk.Button(
            nav_frame, text="Next", command=self.next_page, cursor="hand2"
        )
        next_btn.pack(side="right", padx=10, ipady=6)

    def next_page(self):
        avoid_text = self.avoid_entry.get().strip()
        if avoid_text:
            avoid_list = [ing.strip() for ing in avoid_text.split(",")]
            self.controller.update_prefs("ingredient_avoidances", avoid_list)

        next_frame = self.controller.get_next_frame(AvoidIngredientsPage)
        self.controller.show_frame(next_frame)
