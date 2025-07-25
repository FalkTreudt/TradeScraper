# gui/data_collection_view.py
import tkinter as tk

class DataCollectionView(tk.Frame):
    def __init__(self, parent, manager, controller):
        super().__init__(parent, bg="#1e1e2f")
        self.manager = manager
        self.controller = controller

        tk.Label(self, text="📥 Daten sammeln", font=("Segoe UI", 18), bg="#1e1e2f", fg="white").pack(pady=20)

        buttons = [
            ("🔄 Engine starten", controller.start_engine),
            ("📅 Tagesdaten sammeln", controller.collect_day_data),
            ("📈 Wochendaten sammeln", controller.collect_week_data),
            ("🗓️ Monatsdaten sammeln", controller.collect_month_data),
            ("📊 Jahresdaten sammeln", controller.collect_year_data),
            ("🔙 Zurück", lambda: self.manager.show_view(controller.start_view_class, controller))
        ]

        for text, command in buttons:
            tk.Button(self, text=text, command=command).pack(fill="x", padx=50, pady=5)
