from abc import ABC, abstractmethod

class AnomalyDetector(ABC):
    @abstractmethod
    def detect(self, value: float):
        pass

    # do i need a fit method here?


class RollingAverageDetector(AnomalyDetector):
    def __init__(self, window_size: int = 100, threshold: float = 2.0):
        self.window_size = window_size
        self.threshold = threshold
        self.window = []

    def detect(self, value: float) -> bool:
        if len(self.window) < self.window_size:
            self.window.append(value)
            return False
        else:
            self.window.pop(0)
            self.window.append(value)
            average = sum(self.window) / self.window_size
            return abs(value - average) > self.threshold
