import tkinter as tk
from tkinter import ttk, messagebox


class CookTimePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        container = tk.Frame(self)
        container.place(relx=0.5, rely=0.5, anchor="center")

        label = tk.Label(
            container,
            text="Maximum cook time in minutes",
            font=("Arial", 16),
        )
        label.pack(pady=20)

        self.cook_time_entry = ttk.Entry(container, width=40, font=("Arial", 13), justify="center")
        self.cook_time_entry.pack(pady=10, ipady=6)

        desc = tk.Label(
            container, text="leave blank for no limit", font=("Arial", 11), fg="#504D4D"
        )
        desc.pack(pady=10)

        # Navigation buttons
        nav_frame = tk.Frame(container)
        nav_frame.pack(side="bottom", pady=20)

        prev_btn = ttk.Button(
            nav_frame,
            text="Back",
            command=lambda: controller.show_frame(
                controller.get_prev_frame(CookTimePage)
            ),
        )
        prev_btn.pack(side="left", padx=10, ipady=8)

        next_btn = ttk.Button(nav_frame, text="Next", command=self.next_page)
        next_btn.pack(side="right", padx=10, ipady=8)

    def next_page(self):
        cook_time = self.cook_time_entry.get()
        if cook_time:
            try:
                cook_time = int(cook_time)
                if cook_time <= 0:
                    raise ValueError
                self.controller.user_prefs["max_cook_time"] = cook_time
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a positive number")
                return

        next_frame = self.controller.get_next_frame(CookTimePage)
        self.controller.show_frame(next_frame)
