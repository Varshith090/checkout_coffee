"""Reports module for Coffee Shop Checkout System"""

import json
import os
import tkinter as tk
from tkinter import ttk, messagebox

# Default tax rate for reports
DEFAULT_TAX_RATE = 0.18

class ReportsTab:
    """Add a secured weekly profit report tab to the main notebook."""

    STORAGE_FILE = "reports_auth.json"

    def __init__(self, menu_manager, tax_rate=DEFAULT_TAX_RATE):
        self.menu_manager = menu_manager
        self.tax_rate = tax_rate
        self.access_code = "1234"
        self.authenticated = False
        self.weekly_sales = {item: 0 for item in self.menu_manager.menu}
        self.frame = None

        self._load_access_code_from_file()

    def _load_access_code_from_file(self):
        if os.path.exists(self.STORAGE_FILE):
            try:
                with open(self.STORAGE_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.access_code = data.get("access_code", self.access_code)
            except Exception:
                pass

    def _save_access_code_to_file(self):
        try:
            with open(self.STORAGE_FILE, "w", encoding="utf-8") as f:
                json.dump({"access_code": self.access_code}, f)
        except Exception:
            pass

    def create_reports_tab(self, notebook):
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="📊 REPORTS")
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=0)
        self.frame.rowconfigure(1, weight=1)
        self._show_login_view()

    def _clear_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    def _show_login_view(self):
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
        if self.login_var.get().strip() == self.access_code:
            self.authenticated = True
            self._show_reports_view()
        else:
            messagebox.showerror("Access Denied", "Invalid access code. Please try again.")

    def _inline_change_code(self):
        """Change login code directly from login view"""
        curr = self.curr_code_var.get().strip()
        new = self.new_code_var.get().strip()

        if not curr or not new:
            messagebox.showwarning("Invalid Input", "Both fields must be filled.")
            return

        if curr != self.access_code:
            messagebox.showerror("Incorrect Code", "Current code is incorrect.")
            return

        self.access_code = new
        self._save_access_code_to_file()
        self.curr_code_var.delete(0, tk.END)
        self.new_code_var.delete(0, tk.END)
        messagebox.showinfo("Code Changed", f"Login code updated to: {new}")

    def _show_reports_view(self):
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
        self._item_var = tk.StringVar(value=next(iter(self.menu_manager.menu), ""))
        ttk.Combobox(control_row, textvariable=self._item_var, values=list(self.menu_manager.menu.keys()), state="readonly").grid(row=0, column=1, padx=3)

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

    def _compute_report_rows(self):
        rows = []
        total_sales = total_cost = total_tax = total_profit = 0.0

        for item_name, details in self.menu_manager.menu.items():
            qty = self.weekly_sales.get(item_name, 0)
            price = float(details.get("price", 0.0))
            cost = float(details.get("cost", price * 0.6))

            sales = price * qty
            cost_total = cost * qty
            tax_total = sales * self.tax_rate
            profit = sales - cost_total - tax_total

            total_sales += sales
            total_cost += cost_total
            total_tax += tax_total
            total_profit += profit

            rows.append({
                "item": item_name.title(),
                "qty": qty,
                "sales": sales,
                "cost": cost_total,
                "tax": tax_total,
                "profit": profit,
            })

        totals = {
            "sales": total_sales,
            "cost": total_cost,
            "tax": total_tax,
            "profit": total_profit,
        }
        return rows, totals

    def _refresh_report_table(self):
        if not self.authenticated:
            return

        for row in self.tree.get_children():
            self.tree.delete(row)

        rows, totals = self._compute_report_rows()

        for row in rows:
            self.tree.insert("", tk.END, values=(
                row["item"],
                row["qty"],
                f"{row['sales']:.2f}",
                f"{row['cost']:.2f}",
                f"{row['tax']:.2f}",
                f"{row['profit']:.2f}"
            ))

        summary_text = (f"Weekly Profit Summary → Sales: ₹{totals['sales']:.2f}, "
                        f"Cost: ₹{totals['cost']:.2f}, Tax: ₹{totals['tax']:.2f}, "
                        f"Profit: ₹{totals['profit']:.2f}")
        self.summary_label.config(text=summary_text)

    def _update_item_qty(self):
        item = self._item_var.get().strip().lower()
        qty = max(0, int(self._qty_var.get()))
        if item not in self.menu_manager.menu:
            messagebox.showerror("Invalid item", "Please select a valid item from the menu.")
            return
        self.weekly_sales[item] = qty
        self._refresh_report_table()

    def _reset_weekly_data(self):
        self.weekly_sales = {item: 0 for item in self.menu_manager.menu}
        self._refresh_report_table()

    def record_sale(self, cart_items):
        """Record sale from checkout. Called when user completes a transaction."""
        for item in cart_items:
            item_name = item["name"].lower()
            if item_name in self.weekly_sales:
                self.weekly_sales[item_name] += item["quantity"]
        
        # Refresh the report if already viewing it
        if self.authenticated and self.frame:
            self._refresh_report_table()
