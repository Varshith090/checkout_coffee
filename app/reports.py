"""Reports Module - Business Logic for Sales Tracking"""

import json
import os

DEFAULT_TAX_RATE = 0.18


class ReportsTab:
    STORAGE_FILE = "reports_auth.json"

    def __init__(self, menu_manager, tax_rate=DEFAULT_TAX_RATE):
        self.menu_manager = menu_manager
        self.tax_rate = tax_rate
        self.access_code = "1234"
        self.authenticated = False
        self.weekly_sales = {item: 0 for item in self.menu_manager.menu}
        self.load_code()

    def load_code(self):
        try:
            with open(self.STORAGE_FILE) as f:
                data = json.load(f)
                self.access_code = data.get("access_code", self.access_code)
        except:
            pass

    def save_code(self):
        try:
            with open(self.STORAGE_FILE, 'w') as f:
                json.dump({"access_code": self.access_code}, f)
        except:
            pass

    def authenticate(self, code):
        if code.strip() == self.access_code:
            self.authenticated = True
            return True, "Access granted"
        return False, "Invalid code"

    def change_access_code(self, current, new):
        if current.strip() != self.access_code:
            return False, "Wrong current code"
        if not new.strip():
            return False, "New code required"
        self.access_code = new.strip()
        self.save_code()
        return True, f"Code changed to {new}"

    def compute_report_data(self):
        rows = []
        totals = {"sales": 0, "cost": 0, "tax": 0, "profit": 0}

        for name, details in self.menu_manager.menu.items():
            qty = self.weekly_sales.get(name, 0)
            price = float(details.get("price", 0))
            cost = float(details.get("cost", price * 0.6))

            sales = price * qty
            cost_total = cost * qty
            tax = sales * self.tax_rate
            profit = sales - cost_total - tax

            totals["sales"] += sales
            totals["cost"] += cost_total
            totals["tax"] += tax
            totals["profit"] += profit

            rows.append({
                "item": name.title(),
                "qty": qty,
                "sales": sales,
                "cost": cost_total,
                "tax": tax,
                "profit": profit,
            })

        return rows, totals

    def update_item_quantity(self, name, qty):
        name = name.lower()
        if name not in self.menu_manager.menu:
            return False, "Item not found"
        self.weekly_sales[name] = max(0, int(qty))
        return True, f"Updated {name} to {qty}"

    def reset_weekly_data(self):
        self.weekly_sales = {item: 0 for item in self.menu_manager.menu}
        return True, "Data reset"

    def record_sale(self, cart_items):
        for item in cart_items:
            name = item["name"].lower()
            qty = item["quantity"]
            if name in self.weekly_sales:
                self.weekly_sales[name] += qty
