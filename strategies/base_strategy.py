# strategies/base_strategy.py
from abc import ABC, abstractmethod

class BaseStrategy(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def evaluate(self, day, week, month, year) -> float:
        """
        Gibt einen Score zwischen 0 und 100 zurück
        """
        pass
