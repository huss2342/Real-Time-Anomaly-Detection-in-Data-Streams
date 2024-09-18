import asyncio
import argparse
import sys
import logging
from data_stream import DataStreamSimulator
from anomaly_detector import AdaptiveRollingAverageDetector
from stream_processor import StreamProcessor
from visualizer import Visualizer


def setup_logging(debug):
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(level=level,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        filename='anomaly_detection_debug.log' if debug else None)
    return logging.getLogger(__name__)


async def main_async(detector_type, window_size, threshold, adaptation_rate, debug):
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
    visualizer = Visualizer(max_points=1000, window_size=window_size)  # Pass window_size here
    processor = StreamProcessor(detector, visualizer, simulator, debug)

    logger.info(f"Starting real-time anomaly detection using {detector_type} detector...")
    logger.info("Close the plot window or press Ctrl+C to stop the process.")

    await processor.run_async(logger)

    if visualizer.is_closed:
        logger.info("Visualizer window was closed. Exiting the program.")
        sys.exit(0)


def main():
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