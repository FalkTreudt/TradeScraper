# strategies/stability_strategy.py
from .base_strategy import BaseStrategy

class StabilityStrategy(BaseStrategy):
    def __init__(self):
        super().__init__("StabilityStrategy")

    def evaluate(self, day, week, month, year) -> float:

        try:
            d = day.GetRSquared()

        except Exception as e:
            print(f"  ❌ Fehler bei day.GetRSquared(): {e}")
            d = 0

        try:
            w = week.GetRSquared()

        except Exception as e:
            print(f"  ❌ Fehler bei week.GetRSquared(): {e}")
            w = 0

        try:
            m = month.GetRSquared()

        except Exception as e:
            print(f"  ❌ Fehler bei month.GetRSquared(): {e}")
            m = 0

        try:
            y = year.GetRSquared()

        except Exception as e:
            print(f"  ❌ Fehler bei year.GetRSquared(): {e}")
            y = 0

        values = [d, w, m, y]
        avg_r2 = sum(values) / len(values)
        return round(avg_r2 * 100, 2)

