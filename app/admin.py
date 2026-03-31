"""Admin Panel for Coffee Shop Management"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json
import os

# Menu file for persistence
MENU_FILE = "menu_items.json"

# Default menu with prices and cost in INR
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

# Modern color scheme
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
    """Manage menu items with persistence"""
    
    def __init__(self):
        self.menu = DEFAULT_MENU.copy() if not os.path.exists(MENU_FILE) else self.load_menu()
    
    def load_menu(self):
        """Load menu from file"""
        try:
            with open(MENU_FILE, 'r') as f:
                return json.load(f)
        except:
            return DEFAULT_MENU.copy()
    
    def save_menu(self):
        """Save menu to file"""
        with open(MENU_FILE, 'w') as f:
            json.dump(self.menu, f, indent=2)
    
    def add_item(self, name, price, cost):
        """Add new menu item"""
        name_lower = name.lower()
        if name_lower in self.menu:
            return False, "Item already exists"
        self.menu[name_lower] = {"price": price, "cost": cost}
        self.save_menu()
        return True, f"Added {name}"
    
    def edit_item(self, name, price, cost):
        """Edit menu item"""
        name_lower = name.lower()
        if name_lower not in self.menu:
            return False, "Item not found"
        self.menu[name_lower] = {"price": price, "cost": cost}
        self.save_menu()
        return True, f"Updated {name}"
    
    def remove_item(self, name):
        """Remove menu item"""
        name_lower = name.lower()
        if name_lower not in self.menu:
            return False, "Item not found"
        del self.menu[name_lower]
        self.save_menu()
        return True, f"Removed {name}"
    
    def get_price(self, item_name):
        """Get item price"""
        return self.menu.get(item_name.lower(), {}).get("price", 0)


# Global menu manager
menu_manager = MenuManager()


class AdminPanel:
    """Admin panel for managing menu items"""
    
    def __init__(self, parent, colors=COLORS, on_menu_update=None):
        self.parent = parent
        self.colors = colors
        self.on_menu_update = on_menu_update
        self.admin_listbox = None
        self.admin_name_entry = None
        self.admin_price_entry = None
        self.admin_cost_entry = None
        self.admin_profit_label = None
    
    def create_admin_tab(self, parent):
        """Create admin panel tab"""
        admin_frame = ttk.Frame(parent)
        admin_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Left side - Menu items list
        list_frame = ttk.LabelFrame(admin_frame, text="📋 MENU ITEMS", padding=12)
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.admin_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, height=20,
                                       font=("Consolas", 10), bg="#ffffff", fg=self.colors["text"])
        self.admin_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.admin_listbox.bind("<<ListboxSelect>>", self.on_item_select)
        scrollbar.config(command=self.admin_listbox.yview)
        
        self.refresh_admin_list()
        
        # Right side - Edit panel
        edit_frame = ttk.LabelFrame(admin_frame, text="✏️ MANAGE ITEMS", padding=12)
        edit_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=8)
        
        # Item name input
        ttk.Label(edit_frame, text="Item Name:").pack(anchor="w", pady=5)
        self.admin_name_entry = ttk.Entry(edit_frame, font=("Segoe UI", 10))
        self.admin_name_entry.pack(fill=tk.X, pady=5)
        
        # Price input
        ttk.Label(edit_frame, text="Selling Price (₹):").pack(anchor="w", pady=5)
        self.admin_price_entry = ttk.Entry(edit_frame, font=("Segoe UI", 10))
        self.admin_price_entry.pack(fill=tk.X, pady=5)
        
        # Cost input
        ttk.Label(edit_frame, text="Cost Price (₹):").pack(anchor="w", pady=5)
        self.admin_cost_entry = ttk.Entry(edit_frame, font=("Segoe UI", 10))
        self.admin_cost_entry.pack(fill=tk.X, pady=5)
        
        # Profit display
        ttk.Label(edit_frame, text="Profit Margin:").pack(anchor="w", pady=5)
        self.admin_profit_label = tk.Label(edit_frame, text="₹0 (0%)", font=("Segoe UI", 10, "bold"), 
                                          fg="#27ae60", bg=self.colors["bg"])
        self.admin_profit_label.pack(fill=tk.X, pady=5)
        
        # Bind price and cost changes to update profit
        self.admin_price_entry.bind("<KeyRelease>", lambda e: self.update_profit_display())
        self.admin_cost_entry.bind("<KeyRelease>", lambda e: self.update_profit_display())
        
        # Buttons
        btn_frame = tk.Frame(edit_frame, bg=self.colors["bg"])
        btn_frame.pack(fill=tk.X, pady=15)
        
        add_btn = tk.Button(btn_frame, text="Add Item", command=self.admin_add_item,
                          font=("Segoe UI", 10, "bold"), bg="#27ae60", fg=self.colors["light_text"],
                          relief=tk.FLAT, padx=12, pady=8, cursor="hand2")
        add_btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        edit_btn = tk.Button(btn_frame, text="Update Item", command=self.admin_edit_item,
                           font=("Segoe UI", 10, "bold"), bg=self.colors["button"], fg=self.colors["light_text"],
                           relief=tk.FLAT, padx=12, pady=8, cursor="hand2")
        edit_btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        delete_btn = tk.Button(btn_frame, text="Delete Item", command=self.admin_delete_item,
                             font=("Segoe UI", 10, "bold"), bg="#e74c3c", fg=self.colors["light_text"],
                             relief=tk.FLAT, padx=12, pady=8, cursor="hand2")
        delete_btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        clear_btn = tk.Button(btn_frame, text="Clear Fields", command=self.admin_clear_fields,
                            font=("Segoe UI", 10), bg="#95a5a6", fg=self.colors["light_text"],
                            relief=tk.FLAT, padx=12, pady=8, cursor="hand2")
        clear_btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
    
    def refresh_admin_list(self):
        """Refresh admin menu items list"""
        self.admin_listbox.delete(0, tk.END)
        for item, details in menu_manager.menu.items():
            price = details["price"]
            cost = details["cost"]
            profit = price - cost
            margin = (profit / price * 100) if price > 0 else 0
            display = f"{item.title():15} | ₹{price:>4} | Cost: ₹{cost:>3} | Profit: ₹{profit:>3} ({margin:.0f}%)"
            self.admin_listbox.insert(tk.END, display)
    
    def on_item_select(self, event):
        """Handle item selection in admin list"""
        selection = self.admin_listbox.curselection()
        if not selection:
            return
        
        index = selection[0]
        items = list(menu_manager.menu.items())
        if index < len(items):
            item_name, details = items[index]
            self.admin_name_entry.delete(0, tk.END)
            self.admin_name_entry.insert(0, item_name.title())
            self.admin_price_entry.delete(0, tk.END)
            self.admin_price_entry.insert(0, str(details["price"]))
            self.admin_cost_entry.delete(0, tk.END)
            self.admin_cost_entry.insert(0, str(details["cost"]))
            self.update_profit_display()
    
    def update_profit_display(self):
        """Update profit margin display"""
        try:
            price = int(self.admin_price_entry.get()) if self.admin_price_entry.get() else 0
            cost = int(self.admin_cost_entry.get()) if self.admin_cost_entry.get() else 0
            profit = price - cost
            margin = (profit / price * 100) if price > 0 else 0
            self.admin_profit_label.config(text=f"₹{profit} ({margin:.1f}%)")
        except:
            self.admin_profit_label.config(text="Invalid input")
    
    def admin_add_item(self):
        """Add new menu item"""
        name = self.admin_name_entry.get().strip()
        try:
            price = int(self.admin_price_entry.get().strip())
            cost = int(self.admin_cost_entry.get().strip())
            
            if not name:
                messagebox.showerror("Error", "Item name required")
                return
            if price <= 0 or cost < 0:
                messagebox.showerror("Error", "Invalid price or cost")
                return
            if cost >= price:
                messagebox.showwarning("Warning", "Cost price should be less than selling price")
                return
            
            success, message = menu_manager.add_item(name, price, cost)
            if success:
                messagebox.showinfo("Success", message)
                self.admin_clear_fields()
                self.refresh_admin_list()
                if self.on_menu_update:
                    self.on_menu_update()
            else:
                messagebox.showerror("Error", message)
        except ValueError:
            messagebox.showerror("Error", "Price and cost must be numbers")
    
    def admin_edit_item(self):
        """Edit existing menu item"""
        name = self.admin_name_entry.get().strip()
        try:
            price = int(self.admin_price_entry.get().strip())
            cost = int(self.admin_cost_entry.get().strip())
            
            if not name:
                messagebox.showerror("Error", "Item name required")
                return
            if price <= 0 or cost < 0:
                messagebox.showerror("Error", "Invalid price or cost")
                return
            if cost >= price:
                messagebox.showwarning("Warning", "Cost price should be less than selling price")
                return
            
            success, message = menu_manager.edit_item(name, price, cost)
            if success:
                messagebox.showinfo("Success", message)
                self.admin_clear_fields()
                self.refresh_admin_list()
                if self.on_menu_update:
                    self.on_menu_update()
            else:
                messagebox.showerror("Error", message)
        except ValueError:
            messagebox.showerror("Error", "Price and cost must be numbers")
    
    def admin_delete_item(self):
        """Delete menu item"""
        name = self.admin_name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Select an item to delete")
            return
        
        if messagebox.askyesno("Confirm", f"Delete {name}?"):
            success, message = menu_manager.remove_item(name)
            if success:
                messagebox.showinfo("Success", message)
                self.admin_clear_fields()
                self.refresh_admin_list()
                if self.on_menu_update:
                    self.on_menu_update()
            else:
                messagebox.showerror("Error", message)
    
    def admin_clear_fields(self):
        """Clear admin form fields"""
        self.admin_name_entry.delete(0, tk.END)
        self.admin_price_entry.delete(0, tk.END)
        self.admin_cost_entry.delete(0, tk.END)
        self.admin_profit_label.config(text="₹0 (0%)")
        self.admin_listbox.selection_clear(0, tk.END)
