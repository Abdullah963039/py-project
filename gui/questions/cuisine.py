import tkinter as tk
from tkinter import ttk

from data.constants import CUISINES


class CuisinePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        container = tk.Frame(self)
        container.place(relx=0.5, rely=0.5, anchor="center")

        label = tk.Label(
            container,
            text="Preferred cuisines (select all that apply)",
            font=("Arial", 14),
        )
        label.pack(pady=20)

        self.cuisine_vars = {}

        columns_frame = tk.Frame(container)
        columns_frame.pack(pady=10)

        num_columns = 3
        chunk_size = len(CUISINES) // num_columns + (
            1 if len(CUISINES) % num_columns else 0
        )
        chunks = [
            CUISINES[i : i + chunk_size] for i in range(0, len(CUISINES), chunk_size)
        ]

        for column in chunks:
            col_frame = tk.Frame(columns_frame)
            col_frame.pack(side="left", padx=20)

            for cuisine in column:
                var = tk.IntVar()
                cb = ttk.Checkbutton(col_frame, text=cuisine, variable=var)
                cb.pack(anchor="w", padx=5, pady=2)
                self.cuisine_vars[cuisine] = var

        nav_frame = tk.Frame(container)
        nav_frame.pack(pady=20)

        prev_btn = ttk.Button(
            nav_frame,
            text="Back",
            command=lambda: controller.show_frame(
                controller.get_prev_frame(CuisinePage)
            ),
        )
        prev_btn.pack(side="left", padx=10, ipady=6)

        next_btn = ttk.Button(nav_frame, text="Next", command=self.next_page)
        next_btn.pack(side="right", padx=10, ipady=6)

    def next_page(self):
        selected_cuisines = [
            cuisine.lower().strip()
            for cuisine, var in self.cuisine_vars.items()
            if var.get()
        ]
        if selected_cuisines:
            self.controller.update_prefs("cuisine_pref", selected_cuisines)

        next_frame = self.controller.get_next_frame(CuisinePage)
        self.controller.show_frame(next_frame)
