import unittest
from unittest.mock import Mock, patch
import asyncio
from src.stream_processor import StreamProcessor
import sys

# ANSI COLORS
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

class CustomTestResult(unittest.TestResult):
    def addFailure(self, test, err):
        super().addFailure(test, err)
        print(f"{RED}[X]{RESET} {test._testMethodName} failed!")

    def addError(self, test, err):
        super().addError(test, err)
        print(f"{RED}[X]{RESET} {test._testMethodName} encountered an error!")

class TestStreamProcessor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print(f"{YELLOW}[!]{RESET} Running stream_processor tests...")

    def setUp(self):
        self.mock_detector = Mock()
        self.mock_visualizer = Mock()
        self.mock_data_stream = Mock()
        self.mock_data_stream.generate_stream.return_value = iter([1, 2, 3])  # Mock iterator
        self.mock_logger = Mock()
        self.stream_processor = StreamProcessor(self.mock_detector, self.mock_visualizer, self.mock_data_stream,
                                                debug=False)

    def test_initialization(self):
        """Test if StreamProcessor initializes correctly"""
        self.assertEqual(self.stream_processor.detector, self.mock_detector)
        self.assertEqual(self.stream_processor.visualizer, self.mock_visualizer)
        self.assertEqual(self.stream_processor.data_stream, self.mock_data_stream)
        self.assertEqual(self.stream_processor.time, 0)
        self.assertFalse(self.stream_processor.debug)
        print(f"{GREEN}[✔]{RESET} test_initialization passed!")

    def test_initialization_with_debug(self):
        """Test if StreamProcessor initializes correctly with debug mode"""
        stream_processor_debug = StreamProcessor(self.mock_detector, self.mock_visualizer, self.mock_data_stream,
                                                 debug=True)
        self.assertTrue(stream_processor_debug.debug)
        print(f"{GREEN}[✔]{RESET} test_initialization_with_debug passed!")

    @patch('asyncio.sleep', return_value=None)
    def test_process_stream(self, mock_sleep):
        """Test if process_stream method processes data correctly"""
        self.mock_visualizer.is_closed = False

        async def run_process_stream():
            await self.stream_processor.process_stream(self.mock_logger, num_points=3)

        asyncio.run(run_process_stream())

        self.assertEqual(self.stream_processor.time, 3)
        self.assertEqual(self.mock_detector.detect.call_count, 3)
        self.assertEqual(self.mock_visualizer.update.call_count, 3)
        self.assertEqual(mock_sleep.call_count, 2)
        print(f"{GREEN}[✔]{RESET} test_process_stream passed!")

    @patch('src.stream_processor.StreamProcessor.process_stream')
    def test_run(self, mock_process_stream):
        """Test if run method calls process_stream"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            mock_process_stream.return_value = loop.create_future()
            mock_process_stream.return_value.set_result(None)

            self.stream_processor.run(self.mock_logger, num_points=3)

            mock_process_stream.assert_called_once_with(self.mock_logger, 3)
            print(f"{GREEN}[✔]{RESET} test_run passed!")
        finally:
            loop.close()

    @patch('src.stream_processor.StreamProcessor.process_stream', side_effect=KeyboardInterrupt)
    def test_run_keyboard_interrupt(self, mock_process_stream):
        """Test if run method handles KeyboardInterrupt correctly"""
        self.stream_processor.run(self.mock_logger, num_points=3)
        self.mock_logger.info.assert_called_with("StreamProcessor: Stream processing interrupted by user.")
        self.mock_visualizer.close.assert_called_once()
        print(f"{GREEN}[✔]{RESET} test_run_keyboard_interrupt passed!")

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestStreamProcessor)
    runner = unittest.TextTestRunner(resultclass=CustomTestResult, stream=sys.stderr, verbosity=2)
    result = runner.run(suite)
    sys.exit(not result.wasSuccessful())