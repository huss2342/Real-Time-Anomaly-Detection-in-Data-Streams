import unittest
import random
from src.anomaly_detector import RollingAverageDetector, ZScoreDetector

# ANSI COLORS
GREEN = '\033[92m'
YELLOW = '\033[93m'
RESET = '\033[0m'


class TestAnomalyDetector(unittest.TestCase):
    print(f"{YELLOW}[!]{RESET} Running anomaly_detector tests...")

    def setUp(self):
        random.seed(42)  # Setting a fixed seed to make it reproducible
        self.normal_data = [random.gauss(100, 10) for _ in range(1000)]
        self.anomalous_data = self.normal_data + [200, 0, 300, -50]  # Adding some obvious anomalies

    def test_rolling_average_detector_initialization(self):
        """Test if RollingAverageDetector initializes correctly"""
        detector = RollingAverageDetector(window_size=100, threshold_std=3.0)
        self.assertEqual(detector.window_size, 100)
        self.assertEqual(detector.threshold_std, 3.0)
        print(f"{GREEN}[✔]{RESET} test_rolling_average_detector_initialization passed!")

    def test_rolling_average_detector_fit(self):
        f"""{RESET}Test if RollingAverageDetector fits data correctly"""
        detector = RollingAverageDetector(window_size=100)
        detector.fit(self.normal_data)
        self.assertEqual(len(detector.window), 100)
        self.assertAlmostEqual(detector.mean, sum(self.normal_data[-100:]) / 100, delta=1)
        print(f"{GREEN}[✔]{RESET} test_rolling_average_detector_fit passed!")

    def test_rolling_average_detector_detect(self):
        """Test if RollingAverageDetector detects anomalies correctly"""
        detector = RollingAverageDetector(window_size=100, threshold_std=3.0)
        detector.fit(self.normal_data)
        for value in self.normal_data[-100:]:
            self.assertFalse(detector.detect(value))
        self.assertTrue(detector.detect(200))
        self.assertTrue(detector.detect(0))
        print(f"{GREEN}[✔]{RESET} test_rolling_average_detector_detect passed!")

    def test_zscore_detector_initialization(self):
        """Test if ZScoreDetector initializes correctly"""
        detector = ZScoreDetector(window_size=100, threshold=3.0)
        self.assertEqual(detector.window_size, 100)
        self.assertEqual(detector.threshold, 3.0)
        print(f"{GREEN}[✔]{RESET} test_zscore_detector_initialization passed!")

    def test_zscore_detector_fit(self):
        """Test if ZScoreDetector fits data correctly"""
        detector = ZScoreDetector(window_size=100)
        detector.fit(self.normal_data)
        self.assertEqual(len(detector.window), 100)
        print(f"{GREEN}[✔]{RESET} test_zscore_detector_fit passed!")

    def test_zscore_detector_detect(self):
        """Test if ZScoreDetector detects anomalies correctly"""
        detector = ZScoreDetector(window_size=100, threshold=3.0)
        detector.fit(self.normal_data)
        for value in self.normal_data[-100:]:
            self.assertFalse(detector.detect(value))
        self.assertTrue(detector.detect(200))
        self.assertTrue(detector.detect(0))
        print(f"{GREEN}[✔]{RESET} test_zscore_detector_detect passed!")


if __name__ == '__main__':
    unittest.main()
