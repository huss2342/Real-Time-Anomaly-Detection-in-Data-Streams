from abc import ABC, abstractmethod
import statistics


class AnomalyDetector(ABC):
    @abstractmethod
    def fit(self, data: list[float]) -> None:
        pass

    @abstractmethod
    def detect(self, value: float) -> bool:
        pass


class AdaptiveRollingAverageDetector(AnomalyDetector):
    def __init__(self, window_size: int = 100, initial_threshold: float = 3.0, adaptation_rate: float = 0.1):
        self.window_size = window_size
        self.threshold = initial_threshold
        self.adaptation_rate = adaptation_rate
        self.window = []
        self.mean = 0
        self.std = 0

    def fit(self, data: list[float]) -> None:
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
            is_anomaly = abs(value - self.mean) > self.threshold * self.std

            # Adapt threshold
            if not is_anomaly:
                error = abs(value - self.mean) / self.std
                self.threshold = (1 - self.adaptation_rate) * self.threshold + self.adaptation_rate * error

            return is_anomaly

    def _update_stats(self) -> None:
        self.mean = statistics.mean(self.window)
        self.std = statistics.stdev(self.window) if len(self.window) > 1 else 0

class RollingAverageDetector(AnomalyDetector):
    def __init__(self, window_size: int = 100, threshold_std: float = 3.0):
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
    def __init__(self, window_size: int = 100, threshold: float = 3.0):
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
