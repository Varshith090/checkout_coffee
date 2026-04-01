"""Coffee Shop Checkout System"""

import tkinter as tk
from app.admin import menu_manager, COLORS
from app.reports import ReportsTab
from app.gui import CoffeeShopGUI, AdminPanel, ReportsTabGUI

root = tk.Tk()

# Create business logic
reports = ReportsTab(menu_manager, 0.18)

# Create GUI
app = CoffeeShopGUI(root, menu_manager, AdminPanel, COLORS, reports)

# Setup reports tab
notebook = next((c for c in root.winfo_children() if hasattr(c, 'tabs')), None)
if notebook:
    gui_reports = ReportsTabGUI(reports, root, COLORS)
    gui_reports.create_reports_tab(notebook)

root.mainloop()
