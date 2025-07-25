from .base_strategy import BaseStrategy
from .trend_strategy import TrendStrategy
from .consistency_strategy import ConsistencyStrategy
from .stability_strategy import StabilityStrategy
from .momentum_strategy import MomentumStrategy
from .volatility_strategy import VolatilityStrategy

class CompositeStrategy(BaseStrategy):
    def __init__(self):
        super().__init__("CompositeStrategy")
        self.strategies = [
            TrendStrategy(),
            ConsistencyStrategy(),
            StabilityStrategy(),
            MomentumStrategy(),
            VolatilityStrategy()
        ]
        self.weights = [0.3, 0.2, 0.2, 0.2, 0.1]  # Summe = 1.0

    def evaluate(self, day, week, month, year) -> float:
        scores = [
            strat.evaluate(day, week, month, year)
            for strat in self.strategies
        ]
        weighted_sum = sum(score * weight for score, weight in zip(scores, self.weights))
        return round(weighted_sum, 2)
