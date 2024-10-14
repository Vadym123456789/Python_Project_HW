class Item:
    def __init__(self, name, price, description, dimensions):
        self.name = name
        self.price = price
        self.description = description
        self.dimensions = dimensions

    def __str__(self):
        return f"{self.name}, price: {self.price}"


class User:
    def __init__(self, name, surname, numberphone):
        self.name = name
        self.surname = surname
        self.numberphone = numberphone

    def __str__(self):
        return f"{self.name} {self.surname}"


class Purchase:
    def __init__(self, user):
        self.products = {}
        self.user = user
        self.total = 0

    def add_item(self, item, cnt):
        if item in self.products:
            self.products[item] = cnt
        else:
            self.products[item] = cnt
        self._calculate_total()

    def __str__(self):
        result = f"User: {self.user}\nItems:\n"
        for item, count in self.products.items():
            result += f"{item.name}: {count} pcs.\n"
        return result.strip()

    def get_total(self):
        return self.total

    def _calculate_total(self):
        self.total = sum(item.price * count for item, count in self.products.items())


# Test the implementation
lemon = Item('lemon', 5, "yellow", "small")
apple = Item('apple', 2, "red", "middle")
print(lemon)  # lemon, price: 5

buyer = User("Ivan", "Ivanov", "02628162")
print(buyer)  # Ivan Ivanov

cart = Purchase(buyer)
cart.add_item(lemon, 4)
cart.add_item(apple, 20)
print(cart)

assert isinstance(cart.user, User) is True, 'Екземпляр класу User'
assert cart.get_total() == 60, "Всього 60"
assert cart.get_total() == 60, 'Повинно залишатися 60!'

cart.add_item(apple, 10)
print(cart)

assert cart.get_total() == 40, "Всього має бути 40"

print("All tests passed successfully!")