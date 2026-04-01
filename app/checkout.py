"""Checkout Module - Business Logic for Shopping Cart"""

TAX_RATE = 0.18


class ShoppingCart:
    def __init__(self, menu_manager):
        self.items = []
        self.menu_manager = menu_manager

    def add_item(self, name, qty=1):
        name = name.lower()
        if name not in self.menu_manager.menu:
            return False, f"Item '{name}' not found"
        price = self.menu_manager.menu[name]["price"]
        self.items.append({"name": name, "quantity": qty, "price": price})
        return True, f"Added {qty} {name}(s)"

    def remove_item(self, name):
        name = name.lower()
        self.items = [i for i in self.items if i["name"] != name]
        return True, f"Removed {name}"

    def get_subtotal(self):
        return sum(i["price"] * i["quantity"] for i in self.items)

    def get_tax(self):
        return self.get_subtotal() * TAX_RATE

    def get_total(self):
        return self.get_subtotal() + self.get_tax()

    def clear_cart(self):
        self.items = []
        return True, "Cart cleared"
