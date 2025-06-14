import tkinter as tk
from tkinter import ttk

from gui.questions.healthy import HealthyPage
from gui.results import ResultsPage


class EquipmentPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.btn_txt = "Get Recommendations"

        self.container = tk.Frame(self)
        self.container.place(relx=0.5, rely=0.5, anchor="center")

        label = tk.Label(
            self.container,
            text="What cooking equipment do you have available? (comma separated)",
            font=("Arial", 14),
        )
        label.pack(pady=20)

        self.equipment_entry = ttk.Entry(self.container, width=40, font=("Arial", 13))
        self.equipment_entry.pack(pady=10, ipady=6)

        sublabel = tk.Label(
            self.container,
            text="Common options: oven, stove, blender, food processor, grill, slow cooker",
            font=("Arial", 11),
            fg="#504D4D",
        )
        sublabel.pack(pady=5)

    def next_action(self):
        equipment_text = self.equipment_entry.get().strip()
        if equipment_text:
            equipment_list = [eq.strip() for eq in equipment_text.split(",")]
            self.controller.update_prefs("available_equipment", equipment_list)

        category = self.controller.get_user_prefs().get("category")

        match category:
            case "healthy":
                self.controller.show_frame(HealthyPage)

            case _:
                self.controller.show_frame(ResultsPage)

    def show_btns(self):
        nav_frame = tk.Frame(self.container)
        nav_frame.pack(side="bottom", pady=20)

        prev_btn = ttk.Button(
            nav_frame,
            text="Back",
            command=lambda: self.controller.show_frame(
                self.controller.get_prev_frame(EquipmentPage)
            ),
        )
        prev_btn.pack(side="left", padx=10, ipady=6)

        next_btn = ttk.Button(
            nav_frame,
            text=self.btn_txt,
            command=self.next_action,
            cursor="hand2",
        )
        next_btn.pack(side="right", padx=10, ipady=6, ipadx=16)

    def update_btn_txt(self, is_next=False):
        self.btn_txt = "Next" if is_next else "Get Recommendations"

        self.show_btns()
