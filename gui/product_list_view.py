import tkinter as tk
from tkinter import ttk
import threading
from concurrent.futures import ThreadPoolExecutor

class ProductListView(tk.Frame):
    def __init__(self, master, manager, controller):
        super().__init__(master)
        self.manager = manager
        self.controller = controller
        self.products_loaded = False
        self.product_data = []
        self.product_ids = []  # IDs separat speichern für spätere Prüfung

        self.pack(fill="both", expand=True)

        title = tk.Label(self, text="📦 Produktliste", font=("Segoe UI", 20))
        title.pack(pady=10)

        # Container für Scrollbar + Treeview
        container = tk.Frame(self)
        container.pack(fill="both", expand=True, padx=20, pady=10)

        # Scrollbar
        scrollbar = tk.Scrollbar(container)
        scrollbar.pack(side="right", fill="y")

        # Treeview
        self.tree = ttk.Treeview(container, yscrollcommand=scrollbar.set, columns=("ID", "Name", "URL", "Bemerkung"), show="headings")
        self.tree.pack(fill="both", expand=True)

        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("URL", text="URL")
        self.tree.heading("Bemerkung", text="Bemerkung")

        scrollbar.config(command=self.tree.yview)

        # Buttons
        ttk.Button(self, text="Zurück", command=self._go_back).pack(pady=10)
        ttk.Button(self, text="Produkte auf Fehler überprüfen", command=self.check_data_completeness).pack(pady=10)
        ttk.Button(self, text="🛠️ Repariere fehlende Daten", command=self.repair_missing_data_threaded).pack(pady=10)


        self.load_products()

    def load_products(self):
        if not self.products_loaded:
            print("🔄 Lade Produkte aus DB...")
            self.product_data = self.controller.engine.DBConector.GetProducts()
            ids, names, urls = self.product_data
            self.product_ids = ids  # Für spätere Nutzung in Prüfung

            for i in range(len(ids)):
                self.tree.insert("", "end", values=(ids[i], names[i], urls[i], ""))


            self.products_loaded = True

    def _go_back(self):
        from gui.main_view import StartView
        self.manager.show_view(StartView, self.controller)

    def check_data_completeness(self):
        print("🔍 Prüfe Vollständigkeit der Produktdaten...")
        ids = self.product_ids
        fehlende = self.controller.engine.DBConector.check_missing_ids_in_tables(ids)

        for i, aktie_id in enumerate(ids):
            fehlende_tabs = [t for t, s in fehlende.items() if aktie_id in s]
            is_complete = len(fehlende_tabs) == 0
            bemerkung = ", ".join(f"Keine Daten in {t}" for t in fehlende_tabs)

            tag = f"row{i}"
            color = "#c8f7c5" if is_complete else "#f7c5c5"

            self.tree.tag_configure(tag, background=color)

            # Werte aktualisieren
            item_id = self.tree.get_children()[i]
            current_values = list(self.tree.item(item_id, "values"))
            current_values[3] = bemerkung
            self.tree.item(item_id, values=current_values, tags=(tag,))

    def update_result(self, aktie_id, is_complete, missing_tables):
        i = self.product_ids.index(aktie_id)
        tag = f"row{i}"
        color = "#c8f7c5" if is_complete else "#f7c5c5"
        bemerkung = ", ".join(f"Keine Daten in {tbl}" for tbl in missing_tables) if missing_tables else ""

        self.tree.tag_configure(tag, background=color)

        # Bestehende Werte holen
        item_id = self.tree.get_children()[i]
        current_values = list(self.tree.item(item_id, "values"))
        current_values[3] = bemerkung  # Spalte "Bemerkung"

        self.tree.item(item_id, values=current_values, tags=(tag,))

    def repair_missing_data_threaded(self):
        threading.Thread(target=self.repair_missing_data, daemon=True).start()

    def repair_missing_data(self):
        self.controller.repair_missing_data()
        self.after(100, self.check_data_completeness)

