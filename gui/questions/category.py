import tkinter as tk
from tkinter import ttk, messagebox


class CategoryPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        container = tk.Frame(self)
        container.place(relx=0.5, rely=0.5, anchor="center")

        label = tk.Label(
            container,
            text="What type of recipes are you looking for?",
            font=("Arial", 14),
        )
        label.pack(pady=20)

        self.category_var = tk.StringVar()

        categories = [
            ("High Protein", "high_protein"),
            ("Quick Meals", "quick_meal"),
            ("Healthy Options", "healthy"),
            ("Budget-Friendly", "budget"),
            ("Meal Prep Friendly", "meal_prep"),
        ]

        rb_frame = tk.Frame(container)
        rb_frame.pack(pady=10)

        for text, value in categories:
            rb = ttk.Radiobutton(
                rb_frame,
                text=text,
                variable=self.category_var,
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
        if not self.category_var.get():
            messagebox.showwarning("Selection Required", "Please select a category")
            return

        self.controller.update_prefs("category", self.category_var.get())
        next_frame = self.controller.get_next_frame(CategoryPage)
        self.controller.show_frame(next_frame)
