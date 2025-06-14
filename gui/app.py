import tkinter as tk

from data.constants import RECIPES
from engine.inferance import EnhancedRecipeRecommender


from gui.results import ResultsPage
from gui.welcome import WelcomePage

from gui.questions.avoid_ingredients import AvoidIngredientsPage
from gui.questions.category import CategoryPage
from gui.questions.cook_time import CookTimePage
from gui.questions.cuisine import CuisinePage
from gui.questions.dietary import DietaryPage
from gui.questions.equipment import EquipmentPage
from gui.questions.include_ingredients import IncludeIngredientsPage
from gui.questions.budget import BudgetPage
from gui.questions.healthy import HealthyPage


class RecipeRecommenderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Recipe Recommendation System")
        self.root.geometry("800x600")

        # Initialize recommender with recipes data
        self.recommender = EnhancedRecipeRecommender(RECIPES)
        self.user_prefs = {}

        # Create container frame
        self.container = tk.Frame(root)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Create all frames
        self.frames = {}

        for F in (
            WelcomePage,
            CategoryPage,
            CookTimePage,
            CuisinePage,
            DietaryPage,
            AvoidIngredientsPage,
            IncludeIngredientsPage,
            EquipmentPage,
            BudgetPage,
            HealthyPage,
            ResultsPage,
        ):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(WelcomePage)

    def show_frame(self, cont):
        frame = self.frames[cont]

        if isinstance(frame, EquipmentPage):
            is_next = self.user_prefs["category"] in ["healthy", "budget"]
            frame.update_btn_txt(is_next)

        if isinstance(frame, ResultsPage):
            frame.update_prefs(self.get_user_prefs())
            frame.display_results()

        frame.tkraise()

    def get_next_frame(self, current_frame):
        category = self.user_prefs["category"]

        frame_orders = {
            "healthy": [
                WelcomePage,
                CategoryPage,
                CookTimePage,
                CuisinePage,
                DietaryPage,
                AvoidIngredientsPage,
                IncludeIngredientsPage,
                EquipmentPage,
                HealthyPage,
                ResultsPage,
            ],
            "budget": [
                WelcomePage,
                CategoryPage,
                CookTimePage,
                CuisinePage,
                DietaryPage,
                AvoidIngredientsPage,
                IncludeIngredientsPage,
                EquipmentPage,
                BudgetPage,
                ResultsPage,
            ],
        }

        frame_order = frame_orders.get(
            category,
            [
                WelcomePage,
                CategoryPage,
                CookTimePage,
                CuisinePage,
                DietaryPage,
                AvoidIngredientsPage,
                IncludeIngredientsPage,
                EquipmentPage,
                ResultsPage,
            ],
        )

        current_index = frame_order.index(current_frame)
        if current_index < len(frame_order) - 1:
            return frame_order[current_index + 1]
        return None

    def get_prev_frame(self, current_frame):
        frame_order = [
            WelcomePage,
            CategoryPage,
            CookTimePage,
            CuisinePage,
            DietaryPage,
            AvoidIngredientsPage,
            IncludeIngredientsPage,
            EquipmentPage,
            ResultsPage,
        ]
        current_index = frame_order.index(current_frame)
        if current_index > 0:
            return frame_order[current_index - 1]
        return None

    def update_prefs(self, key, value):
        self.user_prefs[key] = value

        print(self.user_prefs)

    def get_user_prefs(self):
        return self.user_prefs

    def get_recommender(self):
        return self.recommender
