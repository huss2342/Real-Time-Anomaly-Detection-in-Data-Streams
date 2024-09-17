import unittest
from unittest.mock import Mock, patch, AsyncMock
import asyncio
from stream_processor import StreamProcessor

# ANSI COLORS
GREEN = '\033[92m'
YELLOW = '\033[93m'
RESET = '\033[0m'


class TestStreamProcessor(unittest.TestCase):
    print(f"{YELLOW}[!]{RESET} Running stream_processor tests...")

    def setUp(self):
        self.mock_detector = Mock()
        self.mock_visualizer = Mock()
        self.mock_data_stream = Mock()
        self.mock_data_stream.generate_stream.return_value = iter([1, 2, 3])  # Mock iterator
        self.stream_processor = StreamProcessor(self.mock_detector, self.mock_visualizer, self.mock_data_stream)

    def test_initialization(self):
        """Test if StreamProcessor initializes correctly"""
        self.assertEqual(self.stream_processor.detector, self.mock_detector)
        self.assertEqual(self.stream_processor.visualizer, self.mock_visualizer)
        self.assertEqual(self.stream_processor.data_stream, self.mock_data_stream)
        self.assertEqual(self.stream_processor.time, 0)
        print(f"{GREEN}[✔]{RESET} test_initialization passed!")

    @patch('asyncio.sleep', new_callable=AsyncMock)
    def test_run_method(self, mock_sleep):
        """Test if run method calls run_async"""
        asyncio.run(self.stream_processor.run_async(num_points=3))

        self.assertEqual(self.stream_processor.time, 3)
        self.mock_detector.detect.assert_called()
        self.mock_visualizer.update.assert_called()
        mock_sleep.assert_called()
        print(f"{GREEN}[✔]{RESET} test_run_method passed!")

    @patch('asyncio.sleep', new_callable=AsyncMock)
    def test_run_method_keyboard_interrupt(self, mock_sleep):
        """Test if run method handles KeyboardInterrupt correctly"""
        mock_sleep.side_effect = KeyboardInterrupt

        with self.assertRaises(KeyboardInterrupt):
            asyncio.run(self.stream_processor.run_async(num_points=100))

        self.mock_visualizer.stop.assert_called_once()
        print(f"{GREEN}[✔]{RESET} test_run_method_keyboard_interrupt passed!")


if __name__ == '__main__':
    unittest.main()