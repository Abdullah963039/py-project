class EnhancedRecipeRecommender:
    def __init__(self, recipes):
        self.recipes = recipes
        self.health_indicators = {
            "balanced": {
                "protein_range": (20, 40),
                "carb_range": (30, 50),
                "fat_range": (10, 20),
            },
            "low_carb": {"max_carbs": 25},
            "low_fat": {"max_fat": 15},
        }

    def recommend(self, preferences):
        """
        Enhanced recommender with multiple dietary categories

        Args:
            preferences (dict): May include:
                - category: 'high_protein', 'quick_meal', 'healthy', 'budget', 'meal_prep'
                - max_cook_time: int (minutes)
                - cuisine_pref: list of cuisines
                - dietary_restrictions: list
                - avoid_tags: list
                - min_protein: int
                - max_calories: int
                - ingredient_preferences: list
                - ingredient_avoidances: list
                - budget_level: int (1-5)
                - health_focus: 'balanced', 'low_carb', 'low_fat'
                - available_equipment: list
        """
        recommended = []

        for recipe in self.recipes:
            score = 0
            skip = False

            # Base rules applicable to all categories
            if not self._passes_base_rules(recipe, preferences):
                continue

            # Category-specific rules
            category = preferences.get("category", "high_protein")

            score += self.calc_score(category, recipe, preferences)

            # Skip if category-specific requirements aren't met
            if skip:
                continue

            # Additional scoring
            score += self._score_additional_factors(recipe, preferences)

            if score > 0:
                recommended.append((recipe, score))

        # Sort by score and return
        recommended.sort(key=lambda x: x[1], reverse=True)
        return recommended

    def _passes_base_rules(self, recipe, preferences):
        """Check mandatory requirements"""
        # Cook time
        if (
            "max_cook_time" in preferences
            and recipe["cook_time"] > preferences["max_cook_time"]
        ):
            return False

        # Avoid tags
        if "avoid_tags" in preferences and any(
            tag in recipe["diet_tags"] for tag in preferences["avoid_tags"]
        ):
            return False

        # Ingredient avoidances
        if "ingredient_avoidances" in preferences:
            avoid_ingredients = set(
                i.lower() for i in preferences["ingredient_avoidances"]
            )
            recipe_ingredients = set(i.lower() for i in recipe["ingredients"])
            if avoid_ingredients.intersection(recipe_ingredients):
                return False

        # Equipment check
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

        # Protein content (max 5 points)
        if protein >= 45:
            score += 5
        elif protein >= 35:
            score += 4
        elif protein >= 25:
            score += 3

            # Protein ratio (max 3 points)
        if protein_ratio >= 0.3:
            score += 3
        elif protein_ratio >= 0.2:
            score += 2
        elif protein_ratio >= 0.15:
            score += 1

        # Bonus for high protein + high ratio (max 2 points)
        if protein >= 35 and protein_ratio >= 0.2:
            score += 2

        return score  # Max: 10 points

    def _score_quick_meal(self, recipe, preferences):
        score = 0

        # Cook time (max 5 points)
        if recipe["cook_time"] <= 10:
            score += 5
        elif recipe["cook_time"] <= 15:
            score += 4
        elif recipe["cook_time"] <= 20:
            score += 3

        # Few ingredients (max 3 points)
        if len(recipe["ingredients"]) <= 3:
            score += 3
        elif len(recipe["ingredients"]) <= 5:
            score += 2

        # Minimal prep bonus (max 2 points)
        if "no_cook" in recipe.get("tags", []):
            score += 2

        return score  # Max: 10 points

    def _score_healthy(self, recipe, preferences):
        score = 0
        health_focus = preferences.get("health_focus", "balanced")
        nutrition = recipe["nutrition"]

        # Health score (max 3 points)
        if "health_score" in recipe:
            score += min(3, recipe["health_score"])

        # Focus-specific (max 4 points)
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

        # Whole foods bonus (max 3 points)
        whole_foods = {"vegetables", "fruits", "lean protein", "whole grains"}
        matches = sum(
            1
            for ing in recipe["ingredients"]
            if any(wf in ing.lower() for wf in whole_foods)
        )
        score += min(3, matches)

        return score  # Max: 10 points

    def _score_budget(self, recipe, preferences):
        score = 0

        # Cost rating (max 5 points)
        if recipe.get("cost_rating", 3) == 1:
            score += 5
        elif recipe["cost_rating"] == 2:
            score += 3

        # Common ingredients (max 3 points)
        common_ingredients = {"rice", "beans", "eggs", "potatoes", "pasta"}
        matches = sum(
            1
            for ing in recipe["ingredients"]
            if any(ci in ing.lower() for ci in common_ingredients)
        )
        score += min(3, matches)

        # Few ingredients (max 2 points)
        if len(recipe["ingredients"]) <= 5:
            score += 2

        return score  # Max: 10 points

    def _score_meal_prep(self, recipe, preferences):
        score = 0

        # Explicit meal prep tag (max 4 points)
        if recipe.get("meal_prep_friendly", False):
            score += 4

        # Cook time (max 2 points)
        if recipe["cook_time"] >= 30:
            score += 2  # Worth prepping

        # Freezer-friendly (max 2 points)
        if "freezer_friendly" in recipe.get("tags", []):
            score += 2

        # Serves many (max 2 points)
        if recipe.get("serves", 0) >= 4:
            score += 2

        return score  # Max: 10 points

    def _score_additional_factors(self, recipe, preferences):
        """Score other preference factors"""
        score = 0

        # Cuisine preference
        if (
            "cuisine_pref" in preferences
            and recipe["cuisine"] in preferences["cuisine_pref"]
        ):
            score += 2

        # Dietary restrictions
        if "dietary_restrictions" in preferences:
            match_count = sum(
                1
                for tag in preferences["dietary_restrictions"]
                if tag in recipe["diet_tags"]
            )
            score += match_count * 1.5

        # Ingredient preferences
        if "ingredient_preferences" in preferences:
            pref_ingredients = set(
                i.lower() for i in preferences["ingredient_preferences"]
            )
            recipe_ingredients = set(i.lower() for i in recipe["ingredients"])
            matches = pref_ingredients.intersection(recipe_ingredients)
            score += len(matches) * 0.5

        return score

    def explain_recommendation(self, recipe, score, preferences):
        """Generate detailed explanation for recommendation"""
        category = preferences.get("category", "high_protein")
        explanations = [
            f"Recipe: {recipe['name']}",
            f"Category: {category.replace('_', ' ').title()}",
            f"Match Score: {score:.1f}/10",
            f"Cuisine: {recipe['cuisine']}",
            f"Cook Time: {recipe['cook_time']} minutes",
            f"Nutrition: {recipe['nutrition']['protein']}g protein, "
            + f"{recipe['nutrition']['carbs']}g carbs, {recipe['nutrition']['fat']}g fat, "
            + f"{recipe['nutrition']['calories']} calories",
            f"Diet Tags: {', '.join(recipe['diet_tags'])}",
            f"Ingredients: {', '.join(recipe['ingredients'])}",
        ]

        # Category-specific explanations
        if category == "high_protein":
            protein_ratio = (
                recipe["nutrition"]["protein"] / recipe["nutrition"]["calories"]
            )
            explanations.append(
                f"Protein Quality: {protein_ratio:.2f} protein/calorie ratio "
                + "(excellent > 0.3, good > 0.2)"
            )
        elif category == "quick_meal":
            explanations.append(
                f"Quick Meal Factors: {recipe['cook_time']}min cook time, "
                + f"{len(recipe['ingredients'])} ingredients"
            )
        elif category == "healthy":
            health_focus = preferences.get("health_focus", "balanced")
            explanations.append(
                f"Health Focus: Optimized for {health_focus} nutrition profile"
            )
        elif category == "budget":
            if "cost_rating" in recipe:
                explanations.append(
                    f"Cost Rating: {recipe['cost_rating']}/5 "
                    + "(1=very affordable, 5=expensive)"
                )
        elif category == "meal_prep":
            explanations.append(
                f"Meal Prep Features: {'Meal prep friendly' if recipe.get('meal_prep_friendly', False) else 'Potential for meal prep'}"
            )

        return "\n".join(explanations)

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
