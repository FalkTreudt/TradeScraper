# gui/main.py
import tkinter as tk
from gui.controller import EngineController
from gui.view_manager import ViewManager
from gui.product_list_view import ProductListView
from gui.data_collection_view import DataCollectionView
from gui.evaluation_view import EvaluationView
from gui.portfolio_view import PortfolioView




class StartView(tk.Frame):
    def __init__(self, parent, manager, controller):
        super().__init__(parent, bg="#1e1e2f")
        self.manager = manager
        self.controller = controller

        tk.Label(self, text="📊 TradeScraper Dashboard", font=("Segoe UI", 18), bg="#1e1e2f", fg="white").pack(pady=20)

        buttons = [
            ("📦 Produkte anzeigen", lambda: manager.show_view(ProductListView, controller)),
            ("🛠️ Daten sammeln", lambda: manager.show_view(DataCollectionView, controller)),
            ("📊 Datenauswertung", lambda: manager.show_view(EvaluationView,controller)),
            ("📦 Portfolio", lambda: manager.show_view(PortfolioView, controller)),

        ]

        for text, command in buttons:
            tk.Button(self, text=text, command=command).pack(fill="x", padx=50, pady=5)

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("TradeScraper Dashboard")
        self.root.geometry("1000x700")
        self.root.configure(bg="#1e1e2f")

        self.manager = ViewManager(self.root)
        controller = EngineController()
        controller.start_view_class = StartView
        self.manager.show_view(StartView, controller)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
