"""Coffee Shop Checkout System - Main Program"""

import tkinter as tk
from tkinter import ttk
from app.admin import menu_manager
from app.admin import AdminPanel
from app.admin import COLORS
from app.checkout import CoffeeShopGUI
from app.reports import ReportsTab

root = tk.Tk()

# Create reports tab instance first
reports_tab = ReportsTab(menu_manager=menu_manager, tax_rate=0.18)

# Pass reports_tab to CoffeeShopGUI
app = CoffeeShopGUI(root, menu_manager=menu_manager, admin_panel_class=AdminPanel, colors=COLORS, reports_tab=reports_tab)

# Find notebook and add reports tab
notebook_widget = None
for child in root.winfo_children():
    if isinstance(child, ttk.Notebook):
        notebook_widget = child
        break

if notebook_widget:
    reports_tab.create_reports_tab(notebook_widget)

root.mainloop()
