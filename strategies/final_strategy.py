from .base_strategy import BaseStrategy

class FinalRecommendationStrategy(BaseStrategy):
    def __init__(self):
        super().__init__("FinalRecommendation")
        self.weights = {
            "TrendStrategy": 0.30,
            "StabilityStrategy": 0.20,
            "MomentumStrategy": 0.20,
            "ConsistencyStrategy": 0.15,
            "CompositeStrategy": 0.15
        }

    def evaluate(self, day, week, month, year, all_scores: dict) -> float:
        total = 0
        weight_sum = 0

        for name, weight in self.weights.items():
            score = all_scores.get(name)
            if isinstance(score, (int, float)):
                total += score * weight
                weight_sum += weight

        if weight_sum == 0:
            return 0.0

        return round(total / weight_sum, 2)
