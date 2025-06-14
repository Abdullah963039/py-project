class EnhancedRecipeRecommender:
    def __init__(self, recipes):
        self.recipes = recipes

    def recommend(self, preferences):
        recommended = []

        for recipe in self.recipes:
            score = 0
            skip = False

            if not self._passes_base_rules(recipe, preferences):
                continue

            category = preferences.get("category", "high_protein")

            score += self.calc_score(category, recipe, preferences)

            if skip:
                continue

            score += self._score_additional_factors(recipe, preferences)

            if score > 0:
                recommended.append((recipe, score))

        recommended.sort(key=lambda x: x[1], reverse=True)
        return recommended

    def _passes_base_rules(self, recipe, preferences):
        if (
            "max_cook_time" in preferences
            and recipe["cook_time"] > preferences["max_cook_time"]
        ):
            return False

        if "dietary_restrictions" in preferences and any(
            tag in recipe["diet_tags"] for tag in preferences["dietary_restrictions"]
        ):
            return False

        if "ingredient_avoidances" in preferences:
            avoid_ingredients = set(
                i.lower() for i in preferences["ingredient_avoidances"]
            )
            recipe_ingredients = set(i.lower() for i in recipe["ingredients"])
            if avoid_ingredients.intersection(recipe_ingredients):
                return False

        if "ingredient_preferences" in preferences:
            available_ingredients = set(
                i.lower() for i in preferences["ingredient_preferences"]
            )
            recipe_ingredients = set(i.lower() for i in recipe["ingredients"])

            if not available_ingredients.intersection(recipe_ingredients):
                return False

        if "available_equipment" in preferences and hasattr(recipe, "equipment_needed"):
            missing_equipment = set(recipe["equipment_needed"]) - set(
                preferences["available_equipment"]
            )
            if missing_equipment:
                return False

        return True

    def _score_high_protein(self, recipe, preferences):
        score = 0
        protein = recipe["nutrition"]["protein"]
        calories = recipe["nutrition"]["calories"]
        protein_ratio = protein / calories

        if protein >= 45:
            score += 5
        elif protein >= 35:
            score += 4
        elif protein >= 25:
            score += 3

        if protein_ratio >= 0.2:
            score += 3
        elif protein_ratio >= 0.1:
            score += 2
        elif protein_ratio >= 0.75:
            score += 1

        if protein >= 35 and protein_ratio >= 0.1:
            score += 2

        return score

    def _score_quick_meal(self, recipe, preferences):
        score = 0

        if recipe["cook_time"] <= 10:
            score += 6
        elif recipe["cook_time"] <= 15:
            score += 5
        elif recipe["cook_time"] <= 20:
            score += 4

        if len(recipe["ingredients"]) <= 3:
            score += 3.5
        elif len(recipe["ingredients"]) <= 5:
            score += 2.5

        return score

    def _score_healthy(self, recipe, preferences):
        score = 0
        health_focus = preferences.get("health_focus", "balanced")
        nutrition = recipe["nutrition"]

        if "health_score" in recipe:
            score += min(3, recipe["health_score"])

        if health_focus == "balanced":
            if (
                20 <= nutrition["protein"] <= 40
                and 30 <= nutrition["carbs"] <= 50
                and 10 <= nutrition["fat"] <= 20
            ):
                score += 4
        elif health_focus == "low_carb" and nutrition["carbs"] <= 20:
            score += 4
        elif health_focus == "low_fat" and nutrition["fat"] <= 10:
            score += 4

        whole_foods = {"tomatoes", "carrots", "avocado", "broccoli", "bell peppers"}
        matches = sum(
            1
            for ing in recipe["ingredients"]
            if any(wf in ing.lower() for wf in whole_foods)
        )
        score += min(3, matches)

        return score

    def _score_budget(self, recipe, preferences):
        score = 0

        if recipe.get("cost_rating", 3) == 1:
            score += 5
        elif recipe["cost_rating"] == 2:
            score += 3

        common_ingredients = {"rice", "beans", "eggs", "potatoes", "pasta"}
        matches = sum(
            1
            for ing in recipe["ingredients"]
            if any(ci in ing.lower() for ci in common_ingredients)
        )
        score += min(3, matches)

        if len(recipe["ingredients"]) <= 5:
            score += 2

        return score

    def _score_meal_prep(self, recipe, preferences):
        score = 0

        if recipe.get("meal_prep_friendly", False):
            score += 4

        if recipe["cook_time"] >= 30:
            score += 2

        if recipe.get("freezer_friendly", False):
            score += 2

        if recipe.get("servings", 0) >= 4:
            score += 2

        return score

    def _score_additional_factors(self, recipe, preferences):
        """Score other preference factors"""
        score = 0

        if (
            "cuisine_pref" in preferences
            and recipe["cuisine"] in preferences["cuisine_pref"]
        ):
            score += 1
        return score

    def calc_score(self, category, recipe, preferences):
        match category:
            case "high_protein":
                return self._score_high_protein(recipe, preferences)

            case "quick_meal":
                return self._score_quick_meal(recipe, preferences)

            case "healthy":
                return self._score_healthy(recipe, preferences)

            case "budget":
                return self._score_budget(recipe, preferences)

            case "meal_prep":
                return self._score_meal_prep(recipe, preferences)

            case _:
                return 0
