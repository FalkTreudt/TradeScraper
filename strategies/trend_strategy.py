# strategies/trend_strategy.py
from .base_strategy import BaseStrategy

class TrendStrategy(BaseStrategy):
    def __init__(self):
        super().__init__("TrendStrategy")

    def normalize(self, slope, max_val):
        norm = min(max(slope / max_val, -1), 1)
        return round(max(0, norm * 100))

    def evaluate(self, day, week, month, year):
        weights = [1, 2, 3, 4]  # z. B. Jahr zählt mehr
        scores = [
            self.normalize(day.GetSlope(), 0.05),
            self.normalize(week.GetSlope(), 0.03),
            self.normalize(month.GetSlope(), 0.02),
            self.normalize(year.GetSlope(), 0.01)
        ]
        weighted_sum = sum(s * w for s, w in zip(scores, weights))
        weight_total = sum(weights)
        return round(weighted_sum / weight_total)
