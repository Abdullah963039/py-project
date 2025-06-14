import tkinter as tk
from tkinter import ttk


class IncludeIngredientsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        container = tk.Frame(self)
        container.place(relx=0.5, rely=0.5, anchor="center")

        label = tk.Label(
            container,
            text="Any ingredients you'd like to include? (comma separated)",
            font=("Arial", 14),
        )
        label.pack(pady=20)

        self.include_entry = ttk.Entry(container, width=40, font=("Arial", 13))
        self.include_entry.pack(pady=10, ipady=6)

        nav_frame = tk.Frame(container)
        nav_frame.pack(side="bottom", pady=20)

        prev_btn = ttk.Button(
            nav_frame,
            text="Back",
            command=lambda: controller.show_frame(
                controller.get_prev_frame(IncludeIngredientsPage)
            ),
            cursor="hand2",
        )
        prev_btn.pack(side="left", padx=10, ipady=6)

        next_btn = ttk.Button(
            nav_frame, text="Next", command=self.next_page, cursor="hand2"
        )
        next_btn.pack(side="right", padx=10, ipady=6)

    def next_page(self):
        include_text = self.include_entry.get().strip()
        if include_text:
            include_list = [ing.strip() for ing in include_text.split(",")]
            self.controller.update_prefs("ingredient_preferences", include_list)

        next_frame = self.controller.get_next_frame(IncludeIngredientsPage)
        self.controller.show_frame(next_frame)
