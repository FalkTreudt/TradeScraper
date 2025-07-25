import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from threading import Thread

class PortfolioView(tk.Frame):
    def __init__(self, master, manager, controller):
        super().__init__(master)
        self.manager = manager
        self.controller = controller
        self.engine = controller.engine

        self.configure(bg="#1e1e2f")
        self.pack(fill="both", expand=True)

        tk.Label(self, text="📈 Portfolio Übersicht", font=("Segoe UI", 24), bg="#1e1e2f", fg="white").pack(pady=20)
        ttk.Button(self, text="🔙 Zurück", command=lambda: manager.show_view(controller.start_view_class, controller)).pack(pady=10)

        self.loading_label = tk.Label(self, text="⏳ Lade Portfolio...", bg="#1e1e2f", fg="white", font=("Segoe UI", 14))
        self.loading_label.pack(pady=20)

        Thread(target=self.load_portfolio_async, daemon=True).start()

    def load_portfolio_async(self):
        self.engine.start(self.engine.create_driver())
        db = self.engine.DBConector
        db.Startconnection()
        entries = db.get_portfolio_entries()

        if not entries:
            self.after(0, lambda: self.loading_label.config(text="⚠️ Kein Portfolio gefunden."))
            return

        names, diffs, colors = [], [], []
        total_diff = 0

        for entry in entries:
            name = entry["name"]
            buyin = float(entry["buyin"])
            shares = float(entry["shares"])

            last_price = self.get_current_price(name)
            current_value = shares * last_price
            diff = round(current_value - buyin, 2)
            color = 'green' if diff >= 0 else 'red'

            names.append(name)
            diffs.append(diff)
            colors.append(color)
            total_diff += diff

        # Gewinne/Verluste zusammenfassen
        names.append("Gesamt")
        diffs.append(round(total_diff, 2))
        colors.append("green" if total_diff >= 0 else "red")

        self.after(0, lambda: self.display_chart(names, diffs, colors))

    def display_chart(self, names, diffs, colors):
        self.loading_label.destroy()

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(names, diffs, color=colors)
        ax.set_title("📊 Gewinn/Verlust je Aktie")
        ax.set_ylabel("€")
        ax.axhline(0, color='black', linewidth=0.8)

        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10)

    def get_current_price(self, aktienname):
        products = self.engine.DBConector.GetProducts()
        for i, name in enumerate(products[1]):
            if name.lower() == aktienname.lower():
                url = products[2][i]
                self.engine.TradeRepublic.GetDataFromURI(url)
                prices = self.engine.TradeRepublic.GetPrices(None)
                return float(prices[-1]) if prices else 0
        return 0
