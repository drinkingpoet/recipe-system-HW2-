from ingredient import Ingredient
from recipe import Recipe

#диетический рецепт как наследник простого рецепта
class DietaryRecipe(Recipe):
    def __init__(self, title, diet_type, ingredients = None):
        super().__init__(title, ingredients)
        self.diet_type = diet_type
    
    def scale(self, ratio):
        if not self.is_ratio_valid(ratio):
            raise ValueError("коэффициент должен быть положительным числом")
        scaled = super().scale(ratio)
        return DietaryRecipe(scaled.title, self.diet_type, scaled.ingredients)
    
    def __str__(self):
        return f"[{self.diet_type}] {self.title}:\n" + "\n".join(f"  - {ingred}" for ingred in self.ingredients)
