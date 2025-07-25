# strategies/momentum_strategy.py
from .base_strategy import BaseStrategy

class MomentumStrategy(BaseStrategy):
    def __init__(self):
        super().__init__("MomentumStrategy")

    def evaluate(self, day, week, month, year) -> float:
        values = [
            day.GetPercentChange(),
            week.GetPercentChange(),
            month.GetPercentChange(),
            year.GetPercentChange()
        ]
        # Nur positive Bewegungen berücksichtigen, negatives Momentum = 0
        positive_avg = sum([v for v in values if v > 0]) / 4
        return round(max(0, min(positive_avg * 100, 100)), 2)
