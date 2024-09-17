import unittest
import numpy as np
import matplotlib
matplotlib.use('Agg')
from visualizer import Visualizer

# ANSI COLORS
GREEN = '\033[92m'
YELLOW = '\033[93m'
RESET = '\033[0m'


class TestVisualizer(unittest.TestCase):
    print(f"{YELLOW}[!]{RESET} Running visualizer tests...")

    def setUp(self):
        self.visualizer = Visualizer(max_points=100)

    def test_initialization(self):
        """Test if Visualizer initializes correctly"""
        self.assertEqual(self.visualizer.max_points, 100)
        self.assertEqual(len(self.visualizer.values), 0)
        self.assertEqual(len(self.visualizer.anomalies), 0)
        self.assertEqual(len(self.visualizer.time), 0)
        print(f"{GREEN}[✔]{RESET} test_initialization passed!")

    def test_update_single_point(self):
        """Test if Visualizer updates correctly with a single point"""
        self.visualizer.update(10.0, False, 0)
        self.assertEqual(len(self.visualizer.values), 1)
        self.assertEqual(len(self.visualizer.anomalies), 1)
        self.assertEqual(len(self.visualizer.time), 1)
        self.assertEqual(self.visualizer.values[0], 10.0)
        self.assertEqual(self.visualizer.anomalies[0], False)
        self.assertEqual(self.visualizer.time[0], 0)
        print(f"{GREEN}[✔]{RESET} test_update_single_point passed!")

    def test_update_multiple_points(self):
        """Test if Visualizer updates correctly with multiple points"""
        for i in range(150):
            self.visualizer.update(float(i), i % 10 == 0, i)

        self.assertEqual(len(self.visualizer.values), 100)
        self.assertEqual(len(self.visualizer.anomalies), 100)
        self.assertEqual(len(self.visualizer.time), 100)
        np.testing.assert_array_equal(self.visualizer.values, np.arange(50, 150, dtype=float))
        np.testing.assert_array_equal(self.visualizer.anomalies, [(i % 10 == 0) for i in range(50, 150)])
        np.testing.assert_array_equal(self.visualizer.time, np.arange(50, 150))
        print(f"{GREEN}[✔]{RESET} test_update_multiple_points passed!")

    def test_animate_function(self):
        """Test if _animate function returns correct artists"""
        for i in range(50):
            self.visualizer.update(float(i), i % 10 == 0, i)

        artists = self.visualizer._animate(0)
        self.assertEqual(len(artists), 2)
        self.assertEqual(artists[0], self.visualizer.normal_line)
        self.assertEqual(artists[1], self.visualizer.anomaly_line)
        print(f"{GREEN}[✔]{RESET} test_animate_function passed!")


if __name__ == '__main__':
    unittest.main()