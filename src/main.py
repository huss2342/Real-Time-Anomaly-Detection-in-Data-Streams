"""
Real-time Anomaly Detection in Data Streams

This script demonstrates real-time anomaly detection in data streams using an adaptive rolling average detector.
It simulates a continuous data stream, processes the data points, detects anomalies, and visualizes the results
in real-time using an interactive plot.

The script utilizes the following components:
- DataStreamSimulator: Generates a simulated data stream with configurable parameters.
- AdaptiveRollingAverageDetector: Detects anomalies in the data stream using an adaptive rolling average algorithm.
- StreamProcessor: Processes the data stream, applies the anomaly detector, and updates the visualizer.
- Visualizer: Displays the data points, anomalies, and rolling window in real-time using a matplotlib plot.

Usage:
    python main.py [--window WINDOW_SIZE] [--threshold THRESHOLD] [--adaptation-rate RATE] [--debug]

Arguments:
    --window WINDOW_SIZE: Window size for the detector (default: 100)
    --threshold THRESHOLD: Initial threshold for anomaly detection (default: 3.0)
    --adaptation-rate RATE: Adaptation rate for adaptive rolling average detector (default: 0.1)
    --debug: Enable debug mode and log detailed information to a file

Example:
    python main.py --window 150 --threshold 2.5 --adaptation-rate 0.05 --debug
"""

import asyncio
import argparse
import sys
import logging
from data_stream import DataStreamSimulator
from anomaly_detector import AdaptiveRollingAverageDetector
from stream_processor import StreamProcessor
from visualizer import Visualizer


def setup_logging(debug):
    """
    Set up logging configuration based on the debug mode.

    Args:
        debug (bool): Whether to enable debug mode.

    Returns:
        logging.Logger: Configured logger object.
    """
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(level=level,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        filename='anomaly_detection_debug.log' if debug else None)
    return logging.getLogger(__name__)


async def main_async(detector_type, window_size, threshold, adaptation_rate, debug):
    """
    asynchronous main function for real-time anomaly detection.

    Args:
        detector_type (str): Type of the anomaly detector.
        window_size (int): Window size for the detector.
        threshold (float): Initial threshold for anomaly detection.
        adaptation_rate (float): Adaptation rate for adaptive rolling average detector.
        debug (bool): Whether to enable debug mode.
    """
    logger = setup_logging(debug)

    simulator = DataStreamSimulator(
        base_value=100,
        noise_level=10,
        seasonal_factor=20,
        trend_factor=0.01,
        cycle_period=1000
    )
    detector = AdaptiveRollingAverageDetector(window_size=window_size, initial_threshold=threshold,
                                              adaptation_rate=adaptation_rate)
    visualizer = Visualizer(max_points=1000, window_size=window_size)
    processor = StreamProcessor(detector, visualizer, simulator, debug)

    logger.info(f"Starting real-time anomaly detection using {detector_type} detector...")
    logger.info("Close the plot window or press Ctrl+C to stop the process.")

    await processor.run_async(logger)

    if visualizer.is_closed:
        logger.info("Visualizer window was closed. Exiting the program.")
        sys.exit(0)


def main():
    """
    The main function of the anomaly detection program.

    This function sets up the command-line argument parser, parses the provided arguments,
    and initializes the necessary components for anomaly detection, including the data stream
    simulator, anomaly detector, visualizer, and stream processor.

    It then runs the anomaly detection process asynchronously using the provided parameters.

    The function handles keyboard interrupts and other exceptions, logging any errors that occur.
    """
    parser = argparse.ArgumentParser(
        description="Real-time Anomaly Detection in Data Streams",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('--window', type=int, default=100,
                        help='Window size for the detector (default: 100)')
    parser.add_argument('--threshold', type=float, default=3.0,
                        help='Initial threshold for anomaly detection (default: 3.5)')
    parser.add_argument('--adaptation-rate', type=float, default=0.1,
                        help='Adaptation rate for adaptive rolling average detector (default: 0.1)')
    parser.add_argument('--debug', action='store_true',
                        help='Enable debug mode and log detailed information to a file')

    args = parser.parse_args()

    try:
        asyncio.run(
            main_async('adaptive_rolling_average', args.window, args.threshold, args.adaptation_rate, args.debug))
    except KeyboardInterrupt:
        print("\nProgram interrupted by user. Exiting...")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        sys.exit(0)


if __name__ == "__main__":
    main()
