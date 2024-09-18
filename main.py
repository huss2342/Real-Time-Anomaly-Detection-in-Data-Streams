import asyncio
import argparse
import sys
from data_stream import DataStreamSimulator
from anomaly_detector import AdaptiveRollingAverageDetector, ZScoreDetector
from stream_processor import StreamProcessor
from visualizer import Visualizer

def get_detector(detector_type, window_size, threshold, adaptation_rate=0.1):
    if detector_type == 'adaptive_rolling_average':
        return AdaptiveRollingAverageDetector(window_size=window_size, initial_threshold=threshold, adaptation_rate=adaptation_rate)
    elif detector_type == 'zscore':
        return ZScoreDetector(window_size=window_size, threshold=threshold)
    else:
        raise ValueError(f"Unknown detector type: {detector_type}")

async def run_stream_processor(processor):
    await processor.run_async()

async def update_plot(visualizer):
    while True:
        visualizer.update_plot()
        await asyncio.sleep(0.1)

async def main_async(detector_type, window_size, threshold, adaptation_rate):
    simulator = DataStreamSimulator(
        base_value=100,
        noise_level=10,
        seasonal_factor=20,
        trend_factor=0.01,
        cycle_period=1000
    )
    detector = get_detector(detector_type, window_size, threshold, adaptation_rate)
    visualizer = Visualizer(max_points=1000)
    processor = StreamProcessor(detector, visualizer, simulator)

    print(f"Starting real-time anomaly detection using {detector_type} detector...")
    print("Close the plot window or press Ctrl+C to stop the process.")

    await asyncio.gather(
        run_stream_processor(processor),
        update_plot(visualizer)
    )

def main():
    parser = argparse.ArgumentParser(
        description="Real-time Anomaly Detection in Data Streams",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('--detector', type=str, default='adaptive_rolling_average',
                        choices=['adaptive_rolling_average', 'zscore'],
                        help='Type of anomaly detector to use (default: adaptive_rolling_average)')
    parser.add_argument('--window', type=int, default=100,
                        help='Window size for the detector (default: 100)')
    parser.add_argument('--threshold', type=float, default=3.0,
                        help='Initial threshold for anomaly detection (default: 3.0)')
    parser.add_argument('--adaptation-rate', type=float, default=0.1,
                        help='Adaptation rate for adaptive rolling average detector (default: 0.1)')

    args = parser.parse_args()

    try:
        asyncio.run(main_async(args.detector, args.window, args.threshold, args.adaptation_rate))
    except KeyboardInterrupt:
        print("\nProgram interrupted by user. Exiting...")
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()