from ingredient import Ingredient
from recipe import Recipe


#список покупок
class ShoppingList:
    #подсказка что тут кортеж
    def __init__(self):
        self._items: list[tuple[Ingredient, str]] = []
    
    def add_recipe(self, recipe, portions) -> None:
        if portions <= 0:
            raise ValueError("количество порций должно быть положительным")
        scaled = recipe.scale(portions)
        for ingred in scaled.ingredients:
            self._items.append((ingred, recipe.title))
    
    def remove_recipe(self, title) -> None:
        new_items = []
        for item in self.items:
            if item[1] != title:
                new_items.append(item)
        self.items = new_items
    
    def get_list(self):
        quantities: dict[tuple[str, str], float] = {}
        for ingred, _ in self.items:
            key = (ingred.name, ingred.unit)
            quantities[key] = quantities.get(key, 0) + ingred.quantity
        result = []
        for (name, unit), quan in quantities.items():
            ingred = Ingredient(name, quan, unit)
            result.append(ingred)
        #сорт по названию
        result.sort(key=lambda x: x.name)
        return result
    
    def __add__(self, other):
        new_list = ShoppingList()
        new_list._items = self.items.copy() + other.items.copy()
        return new_list
    
    #снова для количества
    def __len__(self):
        return len(self.items)
