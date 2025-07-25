# strategies/stability_strategy.py
from .base_strategy import BaseStrategy

class StabilityStrategy(BaseStrategy):
    def __init__(self):
        super().__init__("StabilityStrategy")

    def evaluate(self, day, week, month, year) -> float:
        values = [
            day.GetRSquared(),
            week.GetRSquared(),
            month.GetRSquared(),
            year.GetRSquared()
        ]
        avg_r2 = sum(values) / len(values)
        return round(avg_r2 * 100, 2)
