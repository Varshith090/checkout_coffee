"""Coffee Shop Checkout System with Tkinter GUI"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Tax rate (18% GST India)
TAX_RATE = 0.18

# Default colors (will be overridden by `colors` passed from main)
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


class ShoppingCart:
    """Shopping cart for coffee shop items"""
    
    def __init__(self, menu_manager):
        self.items = []
        self.menu_manager = menu_manager
    
    def add_item(self, item_name, quantity=1):
        """Add item to cart"""
        item_name = item_name.lower()
        if item_name not in self.menu_manager.menu:
            return False, f"Item '{item_name}' not found in menu"
        
        price = self.menu_manager.menu[item_name]["price"]
        self.items.append({
            "name": item_name,
            "quantity": quantity,
            "price": price
        })
        return True, f"Added {quantity} {item_name}(s) to cart"
    
    def remove_item(self, item_name):
        """Remove item from cart"""
        item_name = item_name.lower()
        self.items = [item for item in self.items if item["name"] != item_name]
        return True, f"Removed {item_name} from cart"
    
    def get_subtotal(self):
        """Calculate cart subtotal"""
        return sum(item["price"] * item["quantity"] for item in self.items)
    
    def get_tax(self):
        """Calculate tax on subtotal"""
        return self.get_subtotal() * TAX_RATE
    
    def get_total(self):
        """Calculate cart total with tax"""
        return self.get_subtotal() + self.get_tax()
    
    def clear_cart(self):
        """Clear all items from cart"""
        self.items = []
        return True, "Cart cleared"


class CoffeeShopGUI:
    """Tkinter GUI for Coffee Shop Checkout"""
    
    def __init__(self, root, menu_manager, admin_panel_class, colors, reports_tab=None):
        self.root = root
        self.root.title("☕ Coffee Shop Checkout")
        self.root.geometry("850x600")
        self.root.configure(bg=colors["bg"])
        self.menu_manager = menu_manager
        self.admin_panel_class = admin_panel_class
        self.colors = colors
        self.reports_tab = reports_tab
        self.cart = ShoppingCart(self.menu_manager)
        
        # Sync module-level COLORS for existing code references
        global COLORS
        COLORS = self.colors

        # Configure ttk style
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Title.TLabel", background=COLORS["primary"], foreground=COLORS["light_text"], font=("Segoe UI", 14, "bold"))
        style.configure("TFrame", background=COLORS["bg"])
        style.configure("TLabelFrame", background=COLORS["bg"], foreground=COLORS["text"])
        style.configure("TLabelFrame.Label", background=COLORS["bg"], foreground=COLORS["text"], font=("Segoe UI", 11, "bold"))
        style.configure("TButton", font=("Segoe UI", 10))
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create GUI widgets with tabs"""
        # Header
        header_frame = tk.Frame(self.root, bg=COLORS["primary"], height=60)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        
        title_label = tk.Label(header_frame, text="☕ DailyDrip ☕", 
                              font=("Segoe UI", 20, "bold"), bg=COLORS["primary"], fg=COLORS["light_text"])
        title_label.pack(pady=12)
        
        # Notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Checkout Tab
        checkout_tab = ttk.Frame(notebook)
        notebook.add(checkout_tab, text="🛒 CHECKOUT")
        self.create_checkout_tab(checkout_tab)
        
        # Admin Tab
        admin_tab = ttk.Frame(notebook)
        notebook.add(admin_tab, text="⚙️ ADMIN")
        if self.admin_panel_class:
            self.admin_panel = self.admin_panel_class(self.root, on_menu_update=self.refresh_checkout_menu)
            self.admin_panel.create_admin_tab(admin_tab)
    
    def create_checkout_tab(self, parent):
        """Create checkout tab"""
        main_frame = ttk.Frame(parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Left side - Menu buttons
        menu_frame = ttk.LabelFrame(main_frame, text="☕ MENU", padding=12)
        menu_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8)
        
        # Create scrollable menu with buttons
        canvas = tk.Canvas(menu_frame, bg=COLORS["bg"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(menu_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set, bg=COLORS["bg"])
        
        # Save for refresh updates
        self.menu_scrollable_frame = scrollable_frame

        # Populate menu buttons with modern style
        self.refresh_checkout_menu()
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Right side - Cart and Controls
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=8)
        
        # Cart display
        cart_frame = ttk.LabelFrame(right_frame, text="🛒 SHOPPING CART", padding=12)
        cart_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        scrollbar_cart = ttk.Scrollbar(cart_frame)
        scrollbar_cart.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.cart_listbox = tk.Listbox(cart_frame, yscrollcommand=scrollbar_cart.set, height=12,
                                      font=("Consolas", 10), bg="#ffffff", fg=COLORS["text"],
                                      relief=tk.FLAT, borderwidth=0)
        self.cart_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_cart.config(command=self.cart_listbox.yview)
        
        # Total display with modern styling
        total_frame = tk.Frame(right_frame, bg=COLORS["primary"], relief=tk.FLAT, padx=12, pady=12)
        total_frame.pack(fill=tk.X, pady=8)
        
        self.total_label = tk.Label(total_frame, text="Subtotal: ₹0.00 | Tax: ₹0.00 | Total: ₹0.00", 
                                   font=("Segoe UI", 12, "bold"), fg=COLORS["light_text"],
                                   bg=COLORS["primary"])
        self.total_label.pack()
        
        # Buttons frame with modern buttons
        buttons_frame = tk.Frame(right_frame, bg=COLORS["bg"])
        buttons_frame.pack(fill=tk.X, pady=10)
        
        remove_btn = tk.Button(buttons_frame, text="Remove Selected", command=self.remove_from_cart,
                             font=("Segoe UI", 10), bg="#e67e22", fg=COLORS["light_text"],
                             relief=tk.FLAT, padx=12, pady=8, cursor="hand2",
                             activebackground="#d35400", activeforeground=COLORS["light_text"])
        remove_btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        clear_btn = tk.Button(buttons_frame, text="Clear Cart", command=self.clear_cart_action,
                            font=("Segoe UI", 10), bg="#95a5a6", fg=COLORS["light_text"],
                            relief=tk.FLAT, padx=12, pady=8, cursor="hand2",
                            activebackground="#7f8c8d", activeforeground=COLORS["light_text"])
        clear_btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        checkout_btn = tk.Button(buttons_frame, text="Checkout", command=self.checkout,
                               font=("Segoe UI", 10, "bold"), bg="#27ae60", fg=COLORS["light_text"],
                               relief=tk.FLAT, padx=12, pady=8, cursor="hand2",
                               activebackground="#229954", activeforeground=COLORS["light_text"])
        checkout_btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
    
    def refresh_checkout_menu(self):
        """Refresh checkout menu from menu manager"""
        if not hasattr(self, "menu_scrollable_frame"):
            return
        for widget in self.menu_scrollable_frame.winfo_children():
            widget.destroy()

        for item, details in self.menu_manager.menu.items():
            price = details["price"]
            btn_text = f"{item.title():18} ₹{price:>4}"
            btn = tk.Button(self.menu_scrollable_frame, text=btn_text,
                           command=lambda i=item: self.add_item_dialog(i),
                           font=("Consolas", 10), bg=COLORS["button"], fg=COLORS["light_text"],
                           relief=tk.FLAT, padx=10, pady=8, cursor="hand2",
                           activebackground=COLORS["button_hover"], activeforeground=COLORS["light_text"])
            btn.pack(fill=tk.X, pady=4)

    def add_item_dialog(self, item_name):
        """Show dialog to select quantity and add item"""
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Add {item_name.title()}")
        dialog.geometry("280x160")
        dialog.resizable(False, False)
        dialog.configure(bg=COLORS["bg"])
        
        header = tk.Label(dialog, text=f"Add {item_name.title()}", font=("Segoe UI", 13, "bold"),
                         bg=COLORS["bg"], fg=COLORS["primary"])
        header.pack(pady=12)
        
        qty_label = tk.Label(dialog, text="Select Quantity:", font=("Segoe UI", 10),
                            bg=COLORS["bg"], fg=COLORS["text"])
        qty_label.pack(pady=5)
        
        qty_var = tk.IntVar(value=1)
        qty_spinbox = ttk.Spinbox(dialog, from_=1, to=100, textvariable=qty_var, width=10,
                                 font=("Segoe UI", 11))
        qty_spinbox.pack(pady=5)
        
        def add_with_qty():
            quantity = qty_var.get()
            success, message = self.cart.add_item(item_name, quantity)
            if success:
                self.update_cart_display()
                dialog.destroy()
            else:
                messagebox.showerror("Error", message)
        
        add_btn = tk.Button(dialog, text="Add to Cart", command=add_with_qty,
                          font=("Segoe UI", 11, "bold"), bg=COLORS["button"], fg=COLORS["light_text"],
                          relief=tk.FLAT, padx=20, pady=8, cursor="hand2",
                          activebackground=COLORS["button_hover"])
        add_btn.pack(pady=10)
    
    def remove_from_cart(self):
        """Remove selected item from cart"""
        selection = self.cart_listbox.curselection()
        if selection:
            index = selection[0]
            if index < len(self.cart.items):
                item_name = self.cart.items[index]["name"]
                self.cart.remove_item(item_name)
                self.update_cart_display()
    
    def clear_cart_action(self):
        """Clear entire cart"""
        self.cart.clear_cart()
        self.update_cart_display()
    
    def update_cart_display(self):
        """Update cart display"""
        self.cart_listbox.delete(0, tk.END)
        for item in self.cart.items:
            subtotal = item["price"] * item["quantity"]
            display = f"{item['name'].title():15} x{item['quantity']} = ₹{subtotal:>6.0f}"
            self.cart_listbox.insert(tk.END, display)
        
        # Calculate and display totals
        subtotal = self.cart.get_subtotal()
        tax = self.cart.get_tax()
        total = self.cart.get_total()
        
        total_text = f"Subtotal: ₹{subtotal:.0f} | Tax: ₹{tax:.0f} | Total: ₹{total:.0f}"
        self.total_label.config(text=total_text)
    
    def checkout(self):
        """Process checkout"""
        if not self.cart.items:
            messagebox.showwarning("Warning", "Cart is empty!")
            return
        
        subtotal = self.cart.get_subtotal()
        tax = self.cart.get_tax()
        total = self.cart.get_total()
        receipt = "RECEIPT\n" + "=" * 45 + "\n"
        for item in self.cart.items:
            item_subtotal = item["price"] * item["quantity"]
            receipt += f"{item['name'].title():20} x{item['quantity']:2} ₹{item_subtotal:>7.0f}\n"
        receipt += "-" * 45 + "\n"
        receipt += f"Subtotal: {' ' * 20} ₹{subtotal:>8.0f}\n"
        receipt += f"Tax (18% GST): {' ' * 14} ₹{tax:>8.0f}\n"
        receipt += "-" * 45 + "\n"
        receipt += f"TOTAL: {' ' * 24} ₹{total:>8.0f}\n"
        receipt += "=" * 45 + "\n"
        receipt += "   Thank you for your purchase!   "
        
        messagebox.showinfo("Receipt", receipt)
        
        # Record sale in reports if available
        if self.reports_tab:
            self.reports_tab.record_sale(self.cart.items)
        
        self.cart.clear_cart()
        self.update_cart_display()
