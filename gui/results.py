import tkinter as tk
from tkinter import ttk

from gui.welcome import WelcomePage


class ResultsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Configure style for cards (same as before)
        style = ttk.Style()
        style.configure(
            "Card.TFrame", background="white", borderwidth=1, relief="solid"
        )
        style.configure(
            "Title.TLabel",
            font=("Arial", 12, "bold"),
            borderwidth=0,
            background="white",
        )
        style.configure(
            "Label.TLabel",
            font=("Arial", 10, "bold"),
            borderwidth=0,
            background="white",
        )
        style.configure(
            "Value.TLabel", font=("Arial", 10), borderwidth=0, background="white"
        )
        style.configure(
            "Tag.TLabel",
            font=("Arial", 8),
            borderwidth=0,
            background="white",
            padding=2,
        )
        style.configure("Details.TFrame", background="white", borderwidth=0, padding=2)

        # Create canvas and scrollbar
        self.canvas = tk.Canvas(self, bg="#f0f0f0")
        self.scrollbar = ttk.Scrollbar(
            self, orient="vertical", command=self.canvas.yview
        )
        self.scrollable_frame = ttk.Frame(self.canvas)

        # Configure canvas scrolling
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        self.canvas.create_window(
            (0, 0),
            window=self.scrollable_frame,
            anchor="nw",
            width=self.winfo_screenwidth(),
        )
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Bind mousewheel to canvas
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # Get all recommendations with score > 0
        self.recommendations = [
            r
            for r in controller.recommender.recommend(controller.user_prefs)
            if r[1] > 0
        ]

        # Display results
        self.display_results()

        # Centered restart button
        restart_frame = ttk.Frame(self.scrollable_frame)
        restart_frame.pack(pady=20)

        restart_btn = ttk.Button(
            restart_frame,
            text="Start Over",
            command=lambda: controller.show_frame(WelcomePage),
        )
        restart_btn.pack()

    def _on_mousewheel(self, event):
        # For Windows and MacOS (with mouse support)
        if event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units")

    def __create_detail_row(self, container, title, value):
        details_frame = ttk.Frame(container, style="Details.TFrame")
        details_frame.pack(fill="both", pady=5)

        ttk.Label(details_frame, text=title, style="Label.TLabel").pack(
            anchor="w", padx=5
        )
        ttk.Label(details_frame, text=value, style="Value.TLabel").pack(
            anchor="w", padx=15
        )

    def __create_card(self, container, recipe, score):
        card = ttk.Frame(container, style="Card.TFrame", padding=15)
        card.pack(fill="x", pady=10, ipadx=10, ipady=10)

        # Header with name and score
        header_frame = ttk.Frame(card, style="Details.TFrame")
        header_frame.pack(fill="x", pady=(0, 10))

        ttk.Label(header_frame, text=f"{recipe['name']}", style="Title.TLabel").pack(
            side="left"
        )

        ttk.Label(
            header_frame, text=f"Score: {score:.1f}/10", style="Label.TLabel"
        ).pack(side="right")

        # Details grid
        details_frame = ttk.Frame(card)
        details_frame.pack(fill="x", pady=5)

        self.__create_detail_row(card, "Cuisine:", recipe["cuisine"])
        self.__create_detail_row(card, "Cook Time:", recipe["cook_time"])

        nutrition = recipe["nutrition"]
        self.__create_detail_row(
            card,
            "Nutrition:",
            f"{nutrition['calories']} cal | {nutrition['protein']}g protein | {nutrition['carbs']}g carbs | {nutrition['fat']}g fat",
        )

        if "cost_rating" in recipe:
            self.__create_detail_row(card, "Cost Rating:", f"{recipe['cost_rating']}/5")

        if recipe.get("meal_prep_friendly", False):
            self.__create_detail_row(card, "Meal Prep:", "✓ Friendly")

        # Dietary tags
        tags_frame = ttk.Frame(card)
        tags_frame.pack(fill="x", pady=(10, 0))

        self.__create_detail_row(card, "Dietary Tags:", ", ".join(recipe["diet_tags"]))

        self.__create_detail_row(card, "Ingredients:", ", ".join(recipe["ingredients"]))

    def display_results(self):
        if not self.recommendations:
            no_results = ttk.Label(
                self.scrollable_frame,
                text="No recipes found matching your criteria",
                style="Title.TLabel",
            )
            no_results.pack(pady=20)
            return

        # Centered title container
        title_frame = ttk.Frame(self.scrollable_frame)
        title_frame.pack(fill="x", pady=20)

        title = ttk.Label(
            title_frame,
            text="Your Recipe Recommendations",
            font=("Arial", 18, "bold"),
        )
        title.pack()

        category = (
            self.controller.user_prefs.get("category", "high_protein")
            .replace("_", " ")
            .title()
        )
        sub_title = ttk.Label(
            title_frame,
            text=f"Based on: {category} preferences",
            font=("Arial", 11, "bold"),
        )
        sub_title.pack(pady=5)

        # Center all cards using a container frame
        cards_container = ttk.Frame(self.scrollable_frame)
        cards_container.pack(fill="x", padx=50)

        # Display all recommendations
        for recipe, score in self.recommendations:
            # Card frame with white background
            self.__create_card(cards_container, recipe, score)
