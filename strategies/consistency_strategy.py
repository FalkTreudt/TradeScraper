# strategies/consistency_strategy.py
from .base_strategy import BaseStrategy

class ConsistencyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__("ConsistencyStrategy")

    def evaluate(self, day, week, month, year):
        scores = [
            day.GetSlope() > 0,
            week.GetSlope() > 0,
            month.GetSlope() > 0,
            year.GetSlope() > 0
        ]
        return scores.count(True) * 25  # 0–100
