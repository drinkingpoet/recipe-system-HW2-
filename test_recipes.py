import pytest
from ingredient import Ingredient
from recipe import Recipe
from shopping_list import ShoppingList
from dietary_recipe import DietaryRecipe

#НИЖЕ ТЕСТЫ ПОД КАЖДЫЙ КЛАСС С ПОХОЖИМИ НА ТЕ КЛАССЫ НАЗВАНИЯМИ



#ingredient
class test_ingredient:
    def test_creation(self):
        ingred = Ingredient("мука", 500.0, "г")
        assert ingred.name == "мука"
        assert ingred.quantity == 500.0
        assert ingred.unit == "г"
    
    def test_quantity(self):
        with pytest.raises(ValueError, match="количество должно быть положительным"):
            Ingredient("соль", -10, "г")
        
        with pytest.raises(ValueError, match="количество должно быть положительным"):
            Ingredient("сахар", 0, "г")
    
    def test_str(self):
        ingred = Ingredient("мука", 500.0, "г")
        assert str(ingred) == "мука: 500.0 г"
    
    def test_eq_quantity(self):
        ingred1 = Ingredient("мука", 500.0, "г")
        ingred2 = Ingredient("мука", 1000.0, "г")
        assert ingred1 == ingred2
    
    def test_eq_name(self):
        ingred1 = Ingredient("мука", 500.0, "г")
        ingred2 = Ingredient("сахар", 500.0, "г")
        assert ingred1 != ingred2
    
    def test_eq_unit(self):
        ingred1 = Ingredient("мука", 500.0, "г")
        ingred2 = Ingredient("мука", 500.0, "кг")
        assert ingred1 != ingred2


#recipe
class test_recipe:
    def test_creation(self):
        ingred = Ingredient("мука", 500.0, "г")
        recipe = Recipe("хлеб", [ingred])
        assert recipe.title == "хлеб"
        assert len(recipe.ingredients) == 1
        assert recipe.ingredients[0] == ingred
    
    def test_adding(self):
        recipe = Recipe("хлеб")
        ingred = Ingredient("мука", 500.0, "г")
        recipe.add_ingredient(ingred)
        assert len(recipe) == 1
        assert recipe.ingredients[0].quantity == 500.0
    
    def test_adding_same(self):
        recipe = Recipe("хлеб")
        ingred1 = Ingredient("мука", 500.0, "г")
        ingred2 = Ingredient("мука", 300.0, "г")
        recipe.add_ingredient(ingred1)
        recipe.add_ingredient(ingred2)
        assert len(recipe) == 1
        assert recipe.ingredients[0].quantity == 800.0
    
    def test_is_ratio_valid(self):
        assert Recipe.is_ratio_valid(1.5) is True
        assert Recipe.is_ratio_valid(6.7) is True
        assert Recipe.is_ratio_valid(0) is False
        assert Recipe.is_ratio_valid(-1) is False
        assert Recipe.is_ratio_valid("ЩПОЗРГШВГИВАЦВЛ") is False
    
    def test_scale(self):
        ingred = Ingredient("мука", 500.0, "г")
        recipe = Recipe("хлеб", [ingred])
        scaled = recipe.scale(2)
        assert scaled is not recipe
        assert scaled.title == recipe.title
        assert recipe.ingredients[0].quantity == 500.0
        assert scaled.ingredients[0].quantity == 1000.0
    
    def test_scale_ratio_bad(self):
        ingred = Ingredient("мука", 500.0, "г")
        recipe = Recipe("хлеб", [ingred])
        with pytest.raises(ValueError, match="коэффициент должен быть положительным числом"):
            recipe.scale(0)
        
        with pytest.raises(ValueError, match="коэффициент должен быть положительным числом"):
            recipe.scale(-6.7)
    
    def test_len(self):
        recipe = Recipe("хлеб")
        recipe.add_ingredient(Ingredient("мука", 500.0, "г"))
        recipe.add_ingredient(Ingredient("вода", 200.0, "г"))
        recipe.add_ingredient(Ingredient("чеснок из пятерочки", 10.0, "г"))
        assert len(recipe) == 3


#shopping
class test_shopping_list:
    def test_creation(self):
        self.bread = Recipe("хлеб", [Ingredient("мука", 500.0, "г"), Ingredient("вода", 200.0, "г"), Ingredient("чеснок из пятерочки", 10.0, "г")])
        self.pasta = Recipe("паста карбонара", [Ingredient("паста", 300.0, "г"), Ingredient("сыр", 100.0, "г"), Ingredient("бекон", 150.0, "г")])
    
    def test_add_recipe(self):
        shopping_list = ShoppingList()
        shopping_list.add_recipe(self.bread, 2)
        assert len(shopping_list) == 3
    
    def test_add_wrong_portions(self):
        shopping_list = ShoppingList()
        with pytest.raises(ValueError, match="количество порций должно быть положительным"):
            shopping_list.add_recipe(self.bread, 0)
        
        with pytest.raises(ValueError, match="количество порций должно быть положительным"):
            shopping_list.add_recipe(self.pasta, -5)
    
    def test_remove_recipe(self):
        shopping_list = ShoppingList()
        shopping_list.add_recipe(self.bread, 1)
        shopping_list.add_recipe(self.pasta, 1)
        assert len(shopping_list) == 6
        shopping_list.remove_recipe("хлеб")
        assert len(shopping_list) == 3
    
    def test_remove_non_existing(self):
        shopping_list = ShoppingList()
        shopping_list.add_recipe(self.bread, 1)
        shopping_list.remove_recipe("рандом рецепт")
        assert len(shopping_list) == 3
    
    def test_combine_ingredient(self):
        shopping_list = ShoppingList()
        shopping_list.add_recipe(self.bread, 1)
        shopping_list.add_recipe(self.pasta, 1)
        result = shopping_list.get_list()
        #тут много всего, но сыр должен сложиться
        sum_items = []
        for ingred in result:
            if ingred.name == "сыр":
                sum_items.append(ingred)
        assert len(sum_items) == 1
        assert sum_items[0].quantity == 300.0
        assert sum_items[0].unit == "г"
    
    def test_sort_list(self):
        shopping_list = ShoppingList()
        shopping_list.add_recipe(self.bread, 1)
        shopping_list.add_recipe(self.pasta, 1)
        result = shopping_list.get_list()
        names = []
        for ingred in result:
            names.append(ingred.name)
        assert names == sorted(names)
    
    def test_add(self):
        list1 = ShoppingList()
        list2 = ShoppingList()
        list1.add_recipe(self.bread, 1)
        list2.add_recipe(self.pasta, 1)
        combined = list1 + list2
        assert len(list1) == 3
        assert len(list2) == 3
        assert len(combined) == 6


#diet recipe
class test_diet_recipe:
    def test_creation(self):
        recipe = DietaryRecipe("паста веган", "веган", [Ingredient("мука", 500.0, "г"), Ingredient("тофу", 200.0, "г")])
        assert recipe.title == "паста веган"
        assert recipe.diet_type == "веган"
        assert len(recipe) == 2
    
    def test_scale_diet(self):
        recipe = DietaryRecipe("паста веган", "веган", [Ingredient("мука", 500.0, "г")])
        scaled = recipe.scale(2)
        assert isinstance(scaled, DietaryRecipe)
        assert scaled.diet_type == "веган"
        assert scaled.ingredients[0].quantity == 1000.0
    
    def test_str(self):
        recipe = DietaryRecipe("паста веган", "веган", [Ingredient("мука", 500.0, "г")])
        assert "[веган]" in str(recipe)
