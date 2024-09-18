from abc import ABC, abstractmethod
import statistics
import numpy as np


class AnomalyDetector(ABC):
    """
    Abstract base class for anomaly detectors.

    This class defines the interface for anomaly detectors, specifying
    that they must implement 'fit' and 'detect' methods.
    """

    @abstractmethod
    def fit(self, data: list[float]) -> None:
        """
        Fit the detector to historical data.

        Args:
            data (list[float]): Historical data to fit the detector.

        Returns:
            None
        """
        pass

    @abstractmethod
    def detect(self, value: float) -> bool:
        """
        Detect if a given value is an anomaly.

        Args:
            value (float): The value to check for anomaly.

        Returns:
            bool: True if the value is an anomaly, False otherwise.
        """
        pass


class AdaptiveRollingAverageDetector:
    """
    anomaly detector using an adaptive rolling average approach.

    this detector maintains a rolling window of recent values and adapts
    its threshold based on the observed data.

    Attributes:
        window_size (int): Size of the rolling window.
        threshold (float): Current threshold for anomaly detection.
        adaptation_rate (float): Rate at which the threshold adapts.
        window (list): Rolling window of recent values.
        mean (float): Current mean of the window.
        std (float): Current standard deviation of the window.
        sum (float): Sum of values in the window.
        sum_sq (float): Sum of squared values in the window.
        count (int): Total number of values processed.
    """

    def __init__(self, window_size: int = 100, initial_threshold: float = 3.2, adaptation_rate: float = 0.05):
        """
        initialize the AdaptiveRollingAverageDetector.

        Args:
            window_size (int): Size of the rolling window.
            default is 100.
            initial_threshold (float): Initial threshold for anomaly detection.
            default is 3.2.
            adaptation_rate (float): Rate at which the threshold adapts.
            default is 0.05.
        """
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
        """
        Detect if a given value is an anomaly and update the detector's state.

        Args:
            value (float): The value to check for anomaly.

        Returns:
            bool: True if the value is an anomaly, False otherwise.
        """
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

        # Adapt the threshold only for non-anomalous points
        if not is_anomaly:
            # Use a more conservative adaptation
            self.threshold = max(
                3.0,  # Minimum threshold
                (1 - self.adaptation_rate) * self.threshold + self.adaptation_rate * z_score
            )

        return is_anomaly

    def _update_stats(self) -> None:
        """
        Update the mean and standard deviation based on the current window.

        This method is called internally after each new value is processed.

        Returns:
            None
        """
        n = len(self.window)
        if n > 0:
            self.mean = self.sum / n
            self.std = max(0.1, np.sqrt((self.sum_sq / n) - (self.mean ** 2)))  # Avoid division by zero
        else:
            self.mean = 0
            self.std = 0.1  # Small non-zero value to avoid division by zero


class RollingAverageDetector(AnomalyDetector):
    """
    anomaly detector using a simple rolling average approach.

    this detector maintains a fixed-size window of recent values and
    uses the mean and standard deviation to detect anomalies.

    Attributes:
        window_size (int): Size of the rolling window.
        threshold_std (float): Number of standard deviations to use as threshold.
        window (list): Rolling window of recent values.
        mean (float): Current mean of the window.
        std (float): Current standard deviation of the window.
    """

    def __init__(self, window_size: int = 100, threshold_std: float = 3.5):
        """
        initialize the RollingAverageDetector.

        Args:
            window_size (int): Size of the rolling window.
            default is 100.
            threshold_std (float): Number of standard deviations to use as threshold.
            default is 3.5.
        """
        self.window_size = window_size
        self.threshold_std = threshold_std
        self.window = []
        self.mean = 0
        self.std = 0

    def fit(self, data: list[float]) -> None:
        """
        Initialize the detector with historical data.

        Args:
            data (list[float]): Historical data to initialize the detector.

        Returns:
            None
        """
        self.window = data[-self.window_size:]
        self._update_stats()

    def detect(self, value: float) -> bool:
        """
        Detect if a given value is an anomaly and update the detector's state.

        Args:
            value (float): The value to check for anomaly.

        Returns:
            bool: True if the value is an anomaly, False otherwise.
        """
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
        """
        Update the mean and standard deviation based on the current window.

        This method is called internally after each new value is processed.

        Returns:
            None
        """
        self.mean = statistics.mean(self.window)
        self.std = statistics.stdev(self.window) if len(self.window) > 1 else 0


class ZScoreDetector(AnomalyDetector):
    """
    anomaly detector using the Z-score method.

    this detector maintains a fixed-size window of recent values and
    uses the Z-score to detect anomalies.

    Attributes:
        window_size (int): Size of the rolling window.
        threshold (float): Z-score threshold for anomaly detection.
        window (list): Rolling window of recent values.
    """

    def __init__(self, window_size: int = 100, threshold: float = 3.5):
        """
        initialize the ZScoreDetector.

        Args:
            window_size (int): Size of the rolling window.
            default is 100.
            threshold (float): Z-score threshold for anomaly detection.
            default is 3.5.
        """
        self.window_size = window_size
        self.threshold = threshold
        self.window = []

    def fit(self, data: list[float]) -> None:
        """
        Initialize the detector with historical data.

        Args:
            data (list[float]): Historical data to initialize the detector.

        Returns:
            None
        """
        self.window = data[-self.window_size:]

    def detect(self, value: float) -> bool:
        """
        Detect if a given value is an anomaly and update the detector's state.

        Args:
            value (float): The value to check for anomaly.

        Returns:
            bool: True if the value is an anomaly, False otherwise.
        """
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
