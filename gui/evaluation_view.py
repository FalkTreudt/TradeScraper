import tkinter as tk
from tkinter import ttk
from threading import Thread
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from datetime import datetime

class EvaluationView(tk.Frame):
    def __init__(self, master, manager, controller):
        super().__init__(master)
        self.manager = manager
        self.controller = controller
        self.configure(bg="#1e1e2f")
        self.pack(fill="both", expand=True)

        title = tk.Label(self, text="📊 Datenauswertung", font=("Segoe UI", 24), bg="#1e1e2f", fg="white")
        title.pack(pady=20)

        # Scrollbarer Frame
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container, bg="#1e1e2f", highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        self.chart_frame = tk.Frame(canvas, bg="#1e1e2f")

        self.chart_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.chart_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Zurück-Button
        ttk.Button(self, text="🔙 Zurück", command=lambda: manager.show_view(controller.start_view_class, controller)).pack(pady=10)

        # Ladeindikator
        self.loading_label = tk.Label(self.chart_frame, text="🔄 Analyse läuft...", font=("Segoe UI", 14), bg="#1e1e2f", fg="white")
        self.loading_label.pack(pady=10)

        # Starte Hintergrundanalyse
        Thread(target=self.run_analysis, daemon=True).start()

    def run_analysis(self):
        from StrategyEngine import StrategyEngine
        engine = StrategyEngine()
        results = engine.analyze_all(top_n=10)
        self.after(0, lambda: self.display_results(results))

    def display_results(self, results):
        self.loading_label.destroy()
        for result in results:
            self._create_chart(result)

    def _create_chart(self, result):
        name = result["name"]
        scores = result["scores"]

        strategy_names = [k for k in scores if k != "FinalRecommendation"]
        values = [scores[k] if isinstance(scores[k], (int, float)) else 0 for k in strategy_names]

        frame = tk.Frame(self.chart_frame, bg="#2a2a3d", padx=10, pady=10)
        frame.pack(padx=20, pady=10, fill="x")

        # Titel
        tk.Label(frame, text=name, font=("Segoe UI", 16, "bold"), bg="#2a2a3d", fg="white").pack(anchor="w")

        # Diagramm
        fig, ax = plt.subplots(figsize=(6, 2.5))
        ax.barh(strategy_names, values)
        ax.set_xlim(0, 100)
        ax.set_title(f"Scores", fontsize=10)

        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

        # Button zur Kaufsimulation
        ttk.Button(frame, text="💰 Kaufsimulation starten", command=lambda r=result: self.simulate_purchase_dialog(r)).pack(pady=5)

    def simulate_purchase_dialog(self, result):
        dialog = tk.Toplevel(self)
        dialog.title("Kaufsimulation")
        dialog.configure(bg="#2e2e3f")

        tk.Label(dialog, text="💸 Investitionsbetrag (€):", bg="#2e2e3f", fg="white", font=("Segoe UI", 12)).pack(pady=10)
        entry = ttk.Entry(dialog)
        entry.pack(pady=5)

        def confirm():
            try:
                amount = float(entry.get())
                self.controller.db.insert_simulated_purchase(result, amount)
                dialog.destroy()
            except Exception as e:
                tk.Label(dialog, text=f"❌ Fehler: {e}", fg="red", bg="#2e2e3f").pack()
                print(f"❌ Fehler: {e}", fg="red", bg="#2e2e3f")

        ttk.Button(dialog, text="✅ Kauf bestätigen", command=confirm).pack(pady=10)
        ttk.Button(dialog, text="❌ Abbrechen", command=dialog.destroy).pack()
