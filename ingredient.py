#класс под ингредиент

class Ingredient:
    def __init__(self, name, quantity, unit):
        self.name = name
        self._quantity = None
        self.quantity = quantity
        self.unit = unit

    @property
    def quantity(self):
        return self._quantity
    
    @quantity.setter
    def quantity(self, value) -> None:
        try:
            value = float(value)
        except(TypeError, ValueError):
            raise ValueError("количество должно быть числом")
        if value <= 0:
            raise ValueError("количество должно быть положительным")
        self._quantity = value

    def __str__(self):
        return f"{self.name}: {self.quantity} {self.unit}"
    
    def __repr__(self):
        return f"ingredient('{self.name}', {self.quantity}, '{self.unit}')"
    
    def __eq__(self, other):
        if not isinstance(other, Ingredient):
            return NotImplemented
        return self.name == other.name and self.unit == other.unit
    #для работы со словарем
    def __hash__(self):
        return hash((self.name, self.unit))