import random
import math
from typing import Generator


class DataStreamSimulator:
    def __init__(self, base_value: float = 100, noise_level: float = 10,
                 seasonal_factor: float = 20, trend_factor: float = 0.01,
                 cycle_period: int = 1000):
        self.base_value = base_value
        self.noise_level = noise_level
        self.seasonal_factor = seasonal_factor
        self.trend_factor = trend_factor
        self.cycle_period = cycle_period

    def generate_stream(self) -> Generator[float, None, None]:
        time = 0
        while True:
            value = self.base_value
            trend = self.trend_factor * time
            season = self.seasonal_factor * math.sin(2 * math.pi * time / self.cycle_period)
            noise = self.noise_level * (random.random() - 0.5)
            result = value + trend + season + noise

            if random.random() < 0.1:  # 0.1% chance of anomaly
                result += random.choice([-1, 1]) * random.uniform(1, 3) * self.noise_level

            yield result
            time += 1
