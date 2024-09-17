import random
from typing import Generator

class DataStreamSimulator:
    def __init__ (self, base_value: float = 100, noise_level: float = 10, seasonal_factor: float = 20):
        self.base_value = base_value
        self.noise_level = noise_level
        self.seasonal_factor = seasonal_factor

    def generate_data_stream(self) -> Generator[float, None, None]:
        time = 0
        while True:
            season = self.seasonal_factor * (1 + 0.1 * random.random())
            noise = self.noise_level * random.random()
            yield self.base_value + season + noise
            time += 1