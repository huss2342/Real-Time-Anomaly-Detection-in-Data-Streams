import unittest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
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
        self.stream_processor = StreamProcessor(self.mock_detector, self.mock_visualizer, self.mock_data_stream, debug=False)

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
        stream_processor_debug = StreamProcessor(self.mock_detector, self.mock_visualizer, self.mock_data_stream, debug=True)
        self.assertTrue(stream_processor_debug.debug)
        print(f"{GREEN}[✔]{RESET} test_initialization_with_debug passed!")

    @patch('asyncio.sleep', new_callable=AsyncMock)
    def test_process_stream(self, mock_sleep):
        """Test if process_stream method processes data correctly"""
        async def run_test():
            self.mock_visualizer.is_closed = False
            await self.stream_processor.process_stream(self.mock_logger, num_points=3)
            print(f"Time: {self.stream_processor.time}")
            print(f"Detector call count: {self.mock_detector.detect.call_count}")
            print(f"Visualizer update call count: {self.mock_visualizer.update.call_count}")
            print(f"Sleep call count: {mock_sleep.call_count}")
            self.assertEqual(self.stream_processor.time, 3)
            self.assertEqual(self.mock_detector.detect.call_count, 3)
            self.assertEqual(self.mock_visualizer.update.call_count, 3)
            self.assertEqual(mock_sleep.call_count, 2)
        asyncio.run(run_test())
        print(f"{GREEN}[✔]{RESET} test_process_stream passed!")

    @patch('asyncio.sleep', new_callable=AsyncMock)
    def test_process_stream_with_debug(self, mock_sleep):
        """Test if process_stream method logs debug information when in debug mode"""
        async def run_test():
            stream_processor_debug = StreamProcessor(self.mock_detector, self.mock_visualizer, self.mock_data_stream, debug=True)
            self.mock_visualizer.is_closed = False
            await stream_processor_debug.process_stream(self.mock_logger, num_points=3)
            self.assertEqual(self.mock_logger.debug.call_count, 3)
        asyncio.run(run_test())
        print(f"{GREEN}[✔]{RESET} test_process_stream_with_debug passed!")

    @patch('asyncio.sleep', new_callable=AsyncMock)
    def test_process_stream_visualizer_closed(self, mock_sleep):
        """Test if process_stream stops when visualizer is closed"""
        async def run_test():
            self.mock_visualizer.is_closed = True
            await self.stream_processor.process_stream(self.mock_logger)
            self.assertEqual(self.stream_processor.time, 0)
            self.mock_logger.info.assert_called_with("Visualizer window was closed. Stopping the stream processing.")
        asyncio.run(run_test())
        print(f"{GREEN}[✔]{RESET} test_process_stream_visualizer_closed passed!")

    def test_run_async(self):
        """Test if run_async method calls process_stream"""
        async def run_test():
            with patch.object(self.stream_processor, 'process_stream', new_callable=AsyncMock) as mock_process_stream:
                await self.stream_processor.run_async(self.mock_logger, num_points=3)
                mock_process_stream.assert_called_once_with(self.mock_logger, 3)
        asyncio.run(run_test())
        print(f"{GREEN}[✔]{RESET} test_run_async passed!")

    def test_run(self):
        """Test if run method calls run_async"""
        with patch.object(self.stream_processor, 'run_async', new_callable=AsyncMock) as mock_run_async:
            self.stream_processor.run(self.mock_logger, num_points=3)
            mock_run_async.assert_called_once()
        print(f"{GREEN}[✔]{RESET} test_run passed!")

        def test_run_keyboard_interrupt(self):
            """Test if run method handles KeyboardInterrupt correctly"""

            async def mock_run_async(logger, num_points):
                raise KeyboardInterrupt()

            with patch.object(self.stream_processor, 'run_async', new_callable=AsyncMock, side_effect=mock_run_async):
                self.stream_processor.run(self.mock_logger, num_points=3)
                self.mock_logger.info.assert_called_with("StreamProcessor: Stream processing interrupted by user.")
                self.mock_visualizer.close.assert_called_once()
            print(f"{GREEN}[✔]{RESET} test_run_keyboard_interrupt passed!")

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestStreamProcessor)
    runner = unittest.TextTestRunner(resultclass=CustomTestResult, stream=sys.stderr, verbosity=2)
    result = runner.run(suite)
    sys.exit(not result.wasSuccessful())