from .base_strategy import BaseStrategy
import statistics

class VolatilityStrategy(BaseStrategy):
    def __init__(self):
        super().__init__("VolatilityStrategy")

    def calc_volatility(self, prices):
        if len(prices) < 2:
            return 0.0
        try:
            mean = sum(prices) / len(prices)
            squared_diffs = [(p - mean) ** 2 for p in prices]
            variance = sum(squared_diffs) / len(prices)
            stddev = variance ** 0.5
            return stddev / mean if mean != 0 else 0.0
        except Exception as e:
            print(f"[Volatility Calc Error] {e}")
            return 0.0

    def evaluate(self, day, week, month, year):
        vols = []
        for timeframe in [day, week, month, year]:
            if timeframe.prices:
                vols.append(self.calc_volatility(timeframe.prices))
            else:
                vols.append(0.0)

        # Skaliere auf 0–100, niedrigere Volatilität = besser
        avg_vol = sum(vols) / len(vols)
        score = max(0, 100 - (avg_vol * 1000))  # justierbarer Faktor
        return round(min(score, 100), 2)
