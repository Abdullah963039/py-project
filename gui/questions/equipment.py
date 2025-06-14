import tkinter as tk
from tkinter import ttk

from gui.results import ResultsPage


class EquipmentPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        container = tk.Frame(self)
        container.place(relx=0.5, rely=0.5, anchor="center")

        label = tk.Label(
            container,
            text="What cooking equipment do you have available? (comma separated)",
            font=("Arial", 14),
        )
        label.pack(pady=20)

        self.equipment_entry = ttk.Entry(container, width=40, font=("Arial", 13))
        self.equipment_entry.pack(pady=10, ipady=6)

        sublabel = tk.Label(
            container,
            text="Common options: oven, stove, blender, food processor, grill, slow cooker",
            font=("Arial", 11),
            fg="#504D4D",
        )
        sublabel.pack(pady=5)

        # Navigation buttons
        nav_frame = tk.Frame(container)
        nav_frame.pack(side="bottom", pady=20)

        prev_btn = ttk.Button(
            nav_frame,
            text="Back",
            command=lambda: controller.show_frame(
                controller.get_prev_frame(EquipmentPage)
            ),
        )
        prev_btn.pack(side="left", padx=10, ipady=6)

        next_btn = ttk.Button(
            nav_frame,
            text="Get Recommendations",
            command=self.get_recommendations,
            cursor="hand2",
        )
        next_btn.pack(side="right", padx=10, ipady=6, ipadx=16)

    def get_recommendations(self):
        equipment_text = self.equipment_entry.get().strip()
        if equipment_text:
            equipment_list = [eq.strip() for eq in equipment_text.split(",")]
            self.controller.update_prefs("available_equipment", equipment_list)

        self.controller.show_frame(ResultsPage)
