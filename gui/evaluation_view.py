# gui/evaluation_view.py
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


class EvaluationView(tk.Frame):
    def __init__(self, master, manager, controller):
        super().__init__(master)
        self.manager = manager
        self.controller = controller
        self.configure(bg="#1e1e2f")
        self.pack(fill="both", expand=True)

        title = tk.Label(self, text="📊 Datenauswertung", font=("Segoe UI", 24), bg="#1e1e2f", fg="white")
        title.pack(pady=20)

        # Scrollable Frame
        canvas = tk.Canvas(self, bg="#1e1e2f", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg="#1e1e2f")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Zurück Button
        ttk.Button(self, text="🔙 Zurück", command=lambda: manager.show_view(controller.start_view_class, controller)).pack(pady=10)

        self.render_top_10()

    def render_top_10(self):
        from StrategyEngine import StrategyEngine
        engine = StrategyEngine()
        results = engine.analyze_all(top_n=10)

        for result in results:
            self._create_chart(result)

    def _create_chart(self, result):
        name = result["name"]
        scores = result["scores"]

        strategy_names = [k for k in scores if k != "FinalRecommendation"]
        values = [scores[k] if isinstance(scores[k], (int, float)) else 0 for k in strategy_names]

        fig, ax = plt.subplots(figsize=(6, 2))
        ax.barh(strategy_names, values)
        ax.set_xlim(0, 100)
        ax.set_title(f"{name} – Score", fontsize=10)

        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.scrollable_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10)
