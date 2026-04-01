"""GUI Module - All Tkinter GUI Components for Coffee Shop App"""

import tkinter as tk
from tkinter import ttk, messagebox
from app.admin import menu_manager, COLORS
from app.checkout import ShoppingCart
from app.reports import ReportsTab


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
        if index >= len(items):
            return
        
        item_name, details = items[index]
        self._fill_fields(item_name, details["price"], details["cost"])
        self.update_profit_display()
    
    def _fill_fields(self, name, price, cost):
        """Fill input fields with item data"""
        self.admin_name_entry.delete(0, tk.END)
        self.admin_name_entry.insert(0, name.title())
        self.admin_price_entry.delete(0, tk.END)
        self.admin_price_entry.insert(0, str(price))
        self.admin_cost_entry.delete(0, tk.END)
        self.admin_cost_entry.insert(0, str(cost))
    
    def update_profit_display(self):
        """Update profit margin display"""
        try:
            price = int(self.admin_price_entry.get() or 0)
            cost = int(self.admin_cost_entry.get() or 0)
            profit = price - cost
            margin = (profit / price * 100) if price > 0 else 0
            self.admin_profit_label.config(text=f"₹{profit} ({margin:.1f}%)")
        except ValueError:
            self.admin_profit_label.config(text="Invalid input")
    
    def _get_input_values(self):
        """Get and validate input values. Returns (values_tuple, error_message)"""
        name = self.admin_name_entry.get().strip()
        if not name:
            return None, "Item name required"
        
        try:
            price = int(self.admin_price_entry.get())
            cost = int(self.admin_cost_entry.get())
        except ValueError:
            return None, "Price and cost must be numbers"
        
        is_valid, error = menu_manager.validate_prices(price, cost)
        if not is_valid:
            return None, error
        
        return (name, price, cost), None
    
    def _complete_operation(self, success, message):
        """Handle successful operation"""
        if success:
            messagebox.showinfo("Success", message)
            self.admin_clear_fields()
            self.refresh_admin_list()
            if self.on_menu_update:
                self.on_menu_update()
        else:
            messagebox.showerror("Error", message)
    
    def admin_add_item(self):
        """Add new menu item"""
        values, error = self._get_input_values()
        if error:
            messagebox.showerror("Error", error)
            return
        name, price, cost = values
        success, message = menu_manager.add_item(name, price, cost)
        self._complete_operation(success, message)
    
    def admin_edit_item(self):
        """Edit existing menu item"""
        values, error = self._get_input_values()
        if error:
            messagebox.showerror("Error", error)
            return
        name, price, cost = values
        success, message = menu_manager.edit_item(name, price, cost)
        self._complete_operation(success, message)
    
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
        """Clear all input fields"""
        self.admin_name_entry.delete(0, tk.END)
        self.admin_price_entry.delete(0, tk.END)
        self.admin_cost_entry.delete(0, tk.END)
        self.admin_profit_label.config(text="₹0 (0%)")


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

        # Configure ttk style
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Title.TLabel", background=self.colors["primary"], foreground=self.colors["light_text"], font=("Segoe UI", 14, "bold"))
        style.configure("TFrame", background=self.colors["bg"])
        style.configure("TLabelFrame", background=self.colors["bg"], foreground=self.colors["text"])
        style.configure("TLabelFrame.Label", background=self.colors["bg"], foreground=self.colors["text"], font=("Segoe UI", 11, "bold"))
        style.configure("TButton", font=("Segoe UI", 10))
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create GUI widgets with tabs"""
        # Header
        header_frame = tk.Frame(self.root, bg=self.colors["primary"], height=60)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        
        title_label = tk.Label(header_frame, text="☕ DailyDrip ☕", 
                              font=("Segoe UI", 20, "bold"), bg=self.colors["primary"], fg=self.colors["light_text"])
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
        canvas = tk.Canvas(menu_frame, bg=self.colors["bg"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(menu_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set, bg=self.colors["bg"])
        
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
                                      font=("Consolas", 10), bg="#ffffff", fg=self.colors["text"],
                                      relief=tk.FLAT, borderwidth=0)
        self.cart_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_cart.config(command=self.cart_listbox.yview)
        
        # Total display with modern styling
        total_frame = tk.Frame(right_frame, bg=self.colors["primary"], relief=tk.FLAT, padx=12, pady=12)
        total_frame.pack(fill=tk.X, pady=8)
        
        self.total_label = tk.Label(total_frame, text="Subtotal: ₹0.00 | Tax: ₹0.00 | Total: ₹0.00", 
                                   font=("Segoe UI", 12, "bold"), fg=self.colors["light_text"],
                                   bg=self.colors["primary"])
        self.total_label.pack()
        
        # Buttons frame with modern buttons
        buttons_frame = tk.Frame(right_frame, bg=self.colors["bg"])
        buttons_frame.pack(fill=tk.X, pady=10)
        
        button_config = [
            ("Remove Selected", self.remove_from_cart, "#e67e22", "#d35400"),
            ("Clear Cart", self.clear_cart_action, "#95a5a6", "#7f8c8d"),
            ("Checkout", self.checkout, "#27ae60", "#229954"),
        ]
        for text, cmd, bg, hover_bg in button_config:
            tk.Button(buttons_frame, text=text, command=cmd, font=("Segoe UI", 10, "bold" if text == "Checkout" else ""),
                     bg=bg, fg=self.colors["light_text"], relief=tk.FLAT, padx=12, pady=8, cursor="hand2",
                     activebackground=hover_bg, activeforeground=self.colors["light_text"]).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
    
    def refresh_checkout_menu(self):
        """Refresh checkout menu from menu manager"""
        if not hasattr(self, "menu_scrollable_frame"):
            return
        for widget in self.menu_scrollable_frame.winfo_children():
            widget.destroy()

        for item, details in self.menu_manager.menu.items():
            price = details["price"]
            btn_text = f"{item.title():18} ₹{price:>4}"
            tk.Button(self.menu_scrollable_frame, text=btn_text, command=lambda i=item: self.add_item_dialog(i),
                     font=("Consolas", 10), bg=self.colors["button"], fg=self.colors["light_text"],
                     relief=tk.FLAT, padx=10, pady=8, cursor="hand2",
                     activebackground=self.colors["button_hover"], activeforeground=self.colors["light_text"]).pack(fill=tk.X, pady=4)

    def add_item_dialog(self, item_name):
        """Show dialog to select quantity and add item"""
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Add {item_name.title()}")
        dialog.geometry("280x160")
        dialog.resizable(False, False)
        dialog.configure(bg=self.colors["bg"])
        
        tk.Label(dialog, text=f"Add {item_name.title()}", font=("Segoe UI", 13, "bold"),
                bg=self.colors["bg"], fg=self.colors["primary"]).pack(pady=12)
        
        tk.Label(dialog, text="Select Quantity:", font=("Segoe UI", 10),
                bg=self.colors["bg"], fg=self.colors["text"]).pack(pady=5)
        
        qty_var = tk.IntVar(value=1)
        ttk.Spinbox(dialog, from_=1, to=100, textvariable=qty_var, width=10,
                   font=("Segoe UI", 11)).pack(pady=5)
        
        def add_with_qty():
            success, message = self.cart.add_item(item_name, qty_var.get())
            if success:
                self.update_cart_display()
                dialog.destroy()
            else:
                messagebox.showerror("Error", message)
        
        tk.Button(dialog, text="Add to Cart", command=add_with_qty,
                 font=("Segoe UI", 11, "bold"), bg=self.colors["button"], fg=self.colors["light_text"],
                 relief=tk.FLAT, padx=20, pady=8, cursor="hand2",
                 activebackground=self.colors["button_hover"]).pack(pady=10)
    
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
    
    def _generate_receipt(self):
        """Generate receipt text for display"""
        subtotal = self.cart.get_subtotal()
        tax = self.cart.get_tax()
        total = self.cart.get_total()
        
        lines = [
            "RECEIPT",
            "=" * 45,
        ]
        
        # Add each item
        for item in self.cart.items:
            item_total = item["price"] * item["quantity"]
            lines.append(f"{item['name'].title():20} x{item['quantity']:2} ₹{item_total:>7.0f}")
        
        # Add totals section
        lines.extend([
            "-" * 45,
            f"Subtotal: {'':<20} ₹{subtotal:>8.0f}",
            f"Tax (18% GST): {'':<14} ₹{tax:>8.0f}",
            "-" * 45,
            f"TOTAL: {'':<24} ₹{total:>8.0f}",
            "=" * 45,
            "   Thank you for your purchase!   "
        ])
        
        return "\n".join(lines)
    
    def checkout(self):
        """Process checkout and record sale"""
        if not self.cart.items:
            messagebox.showwarning("Warning", "Cart is empty!")
            return
        
        receipt = self._generate_receipt()
        messagebox.showinfo("Receipt", receipt)
        
        # Record sale in reports if available
        if self.reports_tab:
            self.reports_tab.record_sale(self.cart.items)
        
        self.cart.clear_cart()
        self.update_cart_display()


class ReportsTabGUI:
    """GUI wrapper for ReportsTab business logic"""
    
    def __init__(self, reports_tab, parent, colors):
        self.reports_tab = reports_tab
        self.parent = parent
        self.colors = colors
        self.frame = None
        self.tree = None
        self.summary_label = None
        self._item_var = None
        self._qty_var = None
    
    def create_reports_tab(self, notebook):
        """Create reports tab GUI"""
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="📊 REPORTS")
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=0)
        self.frame.rowconfigure(1, weight=1)
        self._show_login_view()
    
    def _clear_frame(self):
        """Clear current frame"""
        for widget in self.frame.winfo_children():
            widget.destroy()
    
    def _show_login_view(self):
        """Show login view"""
        self._clear_frame()

        login_frame = ttk.Frame(self.frame, padding=18)
        login_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(login_frame, text="Weekly Profit Report Login",
                  font=("Segoe UI", 14, "bold")).pack(pady=8)

        # Login section
        ttk.Label(login_frame, text="Enter access code to view reports:", font=("Segoe UI", 10)).pack(pady=2)

        self.login_var = tk.StringVar()
        ttk.Entry(login_frame, textvariable=self.login_var, show="*", width=30).pack(pady=4)

        unlock_btn = ttk.Button(login_frame, text="Unlock Reports", command=self._attempt_login)
        unlock_btn.pack(pady=10)

        # Separator
        ttk.Separator(login_frame, orient="horizontal").pack(fill=tk.X, pady=15)

        # Change password section
        ttk.Label(login_frame, text="Change Login Code", font=("Segoe UI", 11, "bold")).pack(pady=8)
        ttk.Label(login_frame, text="Enter current code:", font=("Segoe UI", 9)).pack(pady=2)

        self.curr_code_var = tk.StringVar()
        ttk.Entry(login_frame, textvariable=self.curr_code_var, show="*", width=30).pack(pady=2)

        ttk.Label(login_frame, text="Enter new code:", font=("Segoe UI", 9)).pack(pady=(8, 2))

        self.new_code_var = tk.StringVar()
        ttk.Entry(login_frame, textvariable=self.new_code_var, show="*", width=30).pack(pady=2)

        change_btn = ttk.Button(login_frame, text="Change Code", command=self._inline_change_code)
        change_btn.pack(pady=10)

        ttk.Label(login_frame, text="Default code is 1234.", font=("Segoe UI", 9), foreground="#666").pack(pady=6)
    
    def _attempt_login(self):
        """Attempt login"""
        success, message = self.reports_tab.authenticate(self.login_var.get())
        if success:
            self._show_reports_view()
        else:
            messagebox.showerror("Access Denied", message)
    
    def _inline_change_code(self):
        """Change access code"""
        success, message = self.reports_tab.change_access_code(
            self.curr_code_var.get(), self.new_code_var.get()
        )
        if success:
            self.curr_code_var.set("")
            self.new_code_var.set("")
            messagebox.showinfo("Code Changed", message)
        else:
            messagebox.showerror("Error", message)
    
    def _show_reports_view(self):
        """Show reports view"""
        self._clear_frame()

        top_bar = ttk.Frame(self.frame)
        top_bar.grid(sticky="ew", padx=10, pady=8)
        top_bar.columnconfigure(0, weight=1)

        ttk.Label(top_bar, text="Weekly Profit Reports", font=("Segoe UI", 15, "bold")).grid(row=0, column=0, sticky="w")

        ttk.Button(top_bar, text="Reset Weekly Data", command=self._reset_weekly_data).grid(row=0, column=1, padx=6)

        report_frame = ttk.Frame(self.frame, padding=10)
        report_frame.grid(row=1, column=0, sticky="nsew")

        columns = ("item", "qty", "sales", "cost", "tax", "profit")
        self.tree = ttk.Treeview(report_frame, columns=columns, show="headings", height=12)
        self.tree.heading("item", text="Item")
        self.tree.heading("qty", text="Qty")
        self.tree.heading("sales", text="Sales (₹)")
        self.tree.heading("cost", text="Cost (₹)")
        self.tree.heading("tax", text="Tax (₹)")
        self.tree.heading("profit", text="Profit (₹)")

        self.tree.column("item", width=180)
        self.tree.column("qty", width=50, anchor="center")
        self.tree.column("sales", width=90, anchor="e")
        self.tree.column("cost", width=90, anchor="e")
        self.tree.column("tax", width=90, anchor="e")
        self.tree.column("profit", width=90, anchor="e")

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(report_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        control_row = ttk.Frame(self.frame, padding=(10, 5))
        control_row.grid(row=2, column=0, sticky="ew")
        control_row.columnconfigure(3, weight=1)

        ttk.Label(control_row, text="Select Item:").grid(row=0, column=0, padx=3)
        self._item_var = tk.StringVar(value=next(iter(self.reports_tab.menu_manager.menu), ""))
        ttk.Combobox(control_row, textvariable=self._item_var, values=list(self.reports_tab.menu_manager.menu.keys()), state="readonly").grid(row=0, column=1, padx=3)

        ttk.Label(control_row, text="Qty:").grid(row=0, column=2, padx=3)
        self._qty_var = tk.IntVar(value=1)
        ttk.Spinbox(control_row, from_=0, to=1000, textvariable=self._qty_var, width=6).grid(row=0, column=3, padx=3)

        ttk.Button(control_row, text="Update Qty", command=self._update_item_qty).grid(row=0, column=4, padx=3)
        ttk.Button(control_row, text="Recalculate", command=self._refresh_report_table).grid(row=0, column=5, padx=3)

        summary_frame = ttk.Frame(self.frame, padding=10)
        summary_frame.grid(row=3, column=0, sticky="ew")

        self.summary_label = ttk.Label(summary_frame, text="", font=("Segoe UI", 11, "bold"))
        self.summary_label.pack(anchor="w")

        self._refresh_report_table()
    
    def _refresh_report_table(self):
        """Refresh report table"""
        if not self.reports_tab.authenticated:
            return

        for row in self.tree.get_children():
            self.tree.delete(row)

        rows, totals = self.reports_tab.compute_report_data()

        for row in rows:
            self.tree.insert("", tk.END, values=(
                row["item"],
                row["qty"],
                f"{row['sales']:.2f}",
                f"{row['cost']:.2f}",
                f"{row['tax']:.2f}",
                f"{row['profit']:.2f}"
            ))

        # Add totals summary
        s = totals  # Simplify variable access
        summary = f"Sales: ₹{s['sales']:.2f} | Cost: ₹{s['cost']:.2f} | Tax: ₹{s['tax']:.2f} | Profit: ₹{s['profit']:.2f}"
        self.summary_label.config(text=summary)
    
    def _update_item_qty(self):
        """Update item quantity"""
        success, message = self.reports_tab.update_item_quantity(
            self._item_var.get(), self._qty_var.get()
        )
        if not success:
            messagebox.showerror("Error", message)
        else:
            self._refresh_report_table()
    
    def _reset_weekly_data(self):
        """Reset weekly data"""
        success, message = self.reports_tab.reset_weekly_data()
        if success:
            self._refresh_report_table()
