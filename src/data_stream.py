import random
import math
from typing import Generator


class DataStreamSimulator:
    """
    a class to simulate a data stream with configurable parameters.

    this simulator generates a continuous stream of data points that include
    a base value, trend, seasonal pattern, random noise, and occasional anomalies.

    Attributes:
        base_value (float): The starting point (central tendency) for the data stream.
        noise_level (float): The magnitude of random noise in the data.
        seasonal_factor (float): The amplitude of the seasonal (cyclical) pattern.
        trend_factor (float): The rate of the overall trend in the data over time.
        cycle_period (int): The number of time steps in one complete seasonal cycle.
        anomaly_probability (float): The probability of generating an anomaly at each step.
    """

    def __init__(self, base_value: float = 100, noise_level: float = 10,
                 seasonal_factor: float = 20, trend_factor: float = 0.01,
                 cycle_period: int = 1000, anomaly_probability: float = 0.01):
        """
        initialize the DataStreamSimulator with the given parameters.
        """

        self.base_value = base_value
        self.noise_level = noise_level
        self.seasonal_factor = seasonal_factor
        self.trend_factor = trend_factor
        self.cycle_period = cycle_period
        self.anomaly_probability = anomaly_probability

    def generate_stream(self) -> Generator[float, None, None]:
        """
        Generate a continuous stream of data points.

        This method yields an infinite stream of data points, each composed of:
        - A base value
        - A linear trend
        - A seasonal pattern
        - Random noise
        - Occasional anomalies

        Returns:
            Generator[float, None, None]: A generator that yields float values representing data points.
        """
        time = 0
        while True:
            value = self.base_value
            trend = self.trend_factor * time
            season = self.seasonal_factor * math.sin(2 * math.pi * time / self.cycle_period)
            noise = self.noise_level * (random.random() - 0.5)
            result = value + trend + season + noise

            if random.random() < self.anomaly_probability:  # Configurable chance of anomaly
                result += random.choice([-1, 1]) * random.uniform(1, 3) * self.noise_level

            yield result
            time += 1
