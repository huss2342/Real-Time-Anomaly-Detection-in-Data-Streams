import unittest
import statistics
import random
from data_stream import DataStreamSimulator

# ANSI COLORS
GREEN = '\033[92m'
YELLOW = '\033[93m'
RESET = '\033[0m'


class TestDataStreamSimulator(unittest.TestCase):
    print(f"{YELLOW}[!]{RESET} Running data_stream tests...")

    def setUp(self):
        random.seed(42)  # Setting a fixed seed to make it reproducible
        self.simulator = DataStreamSimulator(
            base_value=100,
            noise_level=10,
            seasonal_factor=20,
            trend_factor=0.01,
            cycle_period=1000
        )

    def test_stream_generation(self):
        """Test if the generator produces values"""
        stream = self.simulator.generate_stream()
        for _ in range(100):
            value = next(stream)
            self.assertIsInstance(value, float)
        print(f"{GREEN}[✔]{RESET} test_stream_generation passed!")

    def test_base_value_and_trend(self):
        """Test if the average of many values follows the expected trend"""
        stream = self.simulator.generate_stream()
        values = [next(stream) for _ in range(10000)]
        avg = statistics.mean(values)
        expected_avg = self.simulator.base_value + (self.simulator.trend_factor * 5000)  # Average time is 5000
        self.assertAlmostEqual(avg, expected_avg, delta=15)
        print(f"{GREEN}[✔]{RESET} test_base_value_and_trend passed!")

    def test_noise_level(self):
        """Test if the noise level is within expected range"""
        stream = self.simulator.generate_stream()
        values = [next(stream) for _ in range(10000)]
        detrended_values = [v - (self.simulator.trend_factor * i) for i, v in enumerate(values)]
        std_dev = statistics.stdev(detrended_values)
        expected_std_dev = (self.simulator.noise_level ** 2 + (self.simulator.seasonal_factor ** 2) / 2) ** 0.5
        self.assertAlmostEqual(std_dev, expected_std_dev, delta=5)
        print(f"{GREEN}[✔]{RESET} test_noise_level passed!")

    def test_trend(self):
        """Test if there's an upward trend in the data"""
        stream = self.simulator.generate_stream()
        first_1000 = [next(stream) for _ in range(1000)]
        second_1000 = [next(stream) for _ in range(1000)]
        self.assertGreater(statistics.mean(second_1000), statistics.mean(first_1000))
        print(f"{GREEN}[✔]{RESET} test_trend passed")

    def test_seasonality(self):
        """Test if there's a repeating pattern in the data"""
        stream = self.simulator.generate_stream()
        values = [next(stream) for _ in range(self.simulator.cycle_period * 2)]
        first_cycle = values[:self.simulator.cycle_period]
        second_cycle = values[self.simulator.cycle_period:]
        correlation = statistics.correlation(first_cycle, second_cycle)
        self.assertGreater(correlation, 0.9)
        print(f"{GREEN}[✔]{RESET} test_seasonality passed!")


if __name__ == '__main__':
    unittest.main()
