from ingredient import Ingredient

#сам рецепт блюда
class Recipe:
    def __init__(self, title, ingredients):
        self.title = title
        if ingredients is not None:
            self._ingredients = ingredients
        else:
            self._ingredients = []
    
    @property
    def ingredients(self):
        return self._ingredients.copy()
    
    def add_ingredient(self, ingredient) -> None:
        for ingred in self._ingredients:
            if ingred == ingredient:
                ingred.quantity += ingredient.quantity
                return
        self._ingredients.append(ingredient)
    
    @staticmethod
    def is_ratio_valid(ratio):
        try:
            return (float(ratio) > 0)
        except(TypeError, ValueError):
            return False
    
    def scale(self, ratio):
        if not self.is_ratio_valid(ratio):
            raise ValueError("коэффициент должен быть положительным числом")
        scaled = []
        for ingred in self._ingredients:
            new_quantity = ingred.quantity * ratio
            new_ingredient = Ingredient(ingred.name, new_quantity, ingred.unit)
            scaled.append(new_ingredient)
        return Recipe(self.title, scaled)
    
    #для количества
    def __len__(self):
        return len(self._ingredients)
    
    def __str__(self) :
        s = "\n".join(f"  - {ingred}" for ingred in self._ingredients)
        return f"{self.title}:\n{s}"
