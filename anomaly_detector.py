from abc import ABC, abstractmethod
import statistics
import numpy as np


class AnomalyDetector(ABC):
    @abstractmethod
    def fit(self, data: list[float]) -> None:
        pass

    @abstractmethod
    def detect(self, value: float) -> bool:
        pass


class AdaptiveRollingAverageDetector:
    def __init__(self, window_size: int = 100, initial_threshold: float = 3.5, adaptation_rate: float = 0.05):
        self.window_size = window_size
        self.threshold = initial_threshold
        self.adaptation_rate = adaptation_rate
        self.window = []
        self.mean = 0
        self.std = 0
        self.sum = 0
        self.sum_sq = 0
        self.count = 0

    def detect(self, value: float) -> bool:
        self.count += 1
        self.sum += value
        self.sum_sq += value ** 2

        if len(self.window) >= self.window_size:
            old_value = self.window.pop(0)
            self.sum -= old_value
            self.sum_sq -= old_value ** 2

        self.window.append(value)

        self._update_stats()

        z_score = abs(value - self.mean) / self.std if self.std > 0 else 0
        is_anomaly = z_score > self.threshold

        # Adapt threshold only for non-anomalous points
        if not is_anomaly:
            # Use a more conservative adaptation
            self.threshold = max(
                3.0,  # Minimum threshold
                (1 - self.adaptation_rate) * self.threshold + self.adaptation_rate * z_score
            )

        return is_anomaly

    def _update_stats(self) -> None:
        n = len(self.window)
        if n > 0:
            self.mean = self.sum / n
            self.std = max(0.1, np.sqrt((self.sum_sq / n) - (self.mean ** 2)))  # Avoid division by zero
        else:
            self.mean = 0
            self.std = 0.1  # Small non-zero value to avoid division by zero

class RollingAverageDetector(AnomalyDetector):
    def __init__(self, window_size: int = 100, threshold_std: float = 3.5):
        self.window_size = window_size
        self.threshold_std = threshold_std
        self.window = []
        self.mean = 0
        self.std = 0

    def fit(self, data: list[float]) -> None:
        """Initialize the detector with historical data"""
        self.window = data[-self.window_size:]
        self._update_stats()

    def detect(self, value: float) -> bool:
        if len(self.window) < self.window_size:
            self.window.append(value)
            self._update_stats()
            return False
        else:
            self.window.pop(0)
            self.window.append(value)
            self._update_stats()
            return abs(value - self.mean) > self.threshold_std * self.std

    def _update_stats(self) -> None:
        self.mean = statistics.mean(self.window)
        self.std = statistics.stdev(self.window) if len(self.window) > 1 else 0


class ZScoreDetector(AnomalyDetector):
    def __init__(self, window_size: int = 100, threshold: float = 3.5):
        self.window_size = window_size
        self.threshold = threshold
        self.window = []

    def fit(self, data: list[float]) -> None:
        """Initialize the detector with historical data"""
        self.window = data[-self.window_size:]

    def detect(self, value: float) -> bool:
        if len(self.window) < self.window_size:
            self.window.append(value)
            return False
        else:
            self.window.pop(0)
            self.window.append(value)
            mean = statistics.mean(self.window)
            std = statistics.stdev(self.window)
            z_score = (value - mean) / std if std > 0 else 0
            return abs(z_score) > self.threshold
