"""Admin Module - Business Logic for Menu Management"""

import json
import os

MENU_FILE = "menu_items.json"

DEFAULT_MENU = {
    "espresso": {"price": 200, "cost": 80},
    "americano": {"price": 250, "cost": 100},
    "latte": {"price": 350, "cost": 130},
    "cappuccino": {"price": 350, "cost": 130},
    "macchiato": {"price": 300, "cost": 110},
    "mocha": {"price": 400, "cost": 150},
    "flat_white": {"price": 380, "cost": 140},
    "cold_brew": {"price": 300, "cost": 110},
    "iced_latte": {"price": 400, "cost": 150},
    "cortado": {"price": 280, "cost": 100},
    "croissant": {"price": 300, "cost": 100},
    "muffin": {"price": 250, "cost": 80},
    "brownie": {"price": 200, "cost": 70},
    "cookie": {"price": 150, "cost": 50},
}

COLORS = {
    "bg": "#f5f5f5",
    "primary": "#2c3e50",
    "secondary": "#3498db",
    "accent": "#e74c3c",
    "text": "#2c3e50",
    "light_text": "#ffffff",
    "button": "#3498db",
    "button_hover": "#2980b9",
}


class MenuManager:
    def __init__(self):
        self.menu = self.load_menu()

    def load_menu(self):
        try:
            with open(MENU_FILE) as f:
                return json.load(f)
        except:
            return DEFAULT_MENU.copy()

    def save_menu(self):
        with open(MENU_FILE, 'w') as f:
            json.dump(self.menu, f, indent=2)

    def validate_prices(self, price, cost):
        try:
            p, c = int(price), int(cost)
            if p <= 0 or c < 0 or c >= p:
                return False, "Invalid prices"
            return True, None
        except:
            return False, "Numbers required"

    def add_item(self, name, price, cost):
        name = name.lower()
        if name in self.menu:
            return False, "Item exists"
        valid, msg = self.validate_prices(price, cost)
        if not valid:
            return False, msg
        self.menu[name] = {"price": price, "cost": cost}
        self.save_menu()
        return True, f"Added {name}"

    def edit_item(self, name, price, cost):
        name = name.lower()
        if name not in self.menu:
            return False, "Item not found"
        valid, msg = self.validate_prices(price, cost)
        if not valid:
            return False, msg
        self.menu[name] = {"price": price, "cost": cost}
        self.save_menu()
        return True, f"Updated {name}"

    def remove_item(self, name):
        name = name.lower()
        if name not in self.menu:
            return False, "Item not found"
        del self.menu[name]
        self.save_menu()
        return True, f"Removed {name}"

    def get_price(self, name):
        return self.menu.get(name.lower(), {}).get("price", 0)


menu_manager = MenuManager()
