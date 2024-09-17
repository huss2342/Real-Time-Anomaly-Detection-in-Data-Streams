import asyncio
import argparse
import sys
from data_stream import DataStreamSimulator
from anomaly_detector import RollingAverageDetector, ZScoreDetector
from stream_processor import StreamProcessor
from visualizer import Visualizer

def get_detector(detector_type, window_size, threshold):
    if detector_type == 'rolling_average':
        return RollingAverageDetector(window_size=window_size, threshold_std=threshold)
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

async def main_async(detector_type='rolling_average', window_size=100, threshold=3.0):
    # Data Stream Simulation
    simulator = DataStreamSimulator(
        base_value=100,
        noise_level=10,
        seasonal_factor=20,
        trend_factor=0.01,
        cycle_period=1000
    )
    detector = get_detector(detector_type, window_size, threshold)
    visualizer = Visualizer(max_points=1000)
    processor = StreamProcessor(detector, visualizer, simulator)

    print(f"Starting real-time anomaly detection using {detector_type} detector...")
    print("Close the plot window or press Ctrl+C to stop the process.")

    # Run the stream processor and update the plot concurrently
    await asyncio.gather(
        run_stream_processor(processor),
        update_plot(visualizer)
    )

def main(detector_type='rolling_average', window_size=100, threshold=3.0):
    asyncio.run(main_async(detector_type, window_size, threshold))

def usage():
    return """
    Usage: python main.py [OPTIONS]

    Real-time Anomaly Detection in Data Streams

    Options:
      --detector TYPE    Type of anomaly detector to use. 
                         Choices: rolling_average, zscore. 
                         Default: rolling_average
      --window SIZE      Window size for the detector. 
                         Default: 100
      --threshold VALUE  Threshold for anomaly detection. 
                         Default: 3.0
      -h, --help         Show this help message and exit

    Example:
      python main.py --detector zscore --window 150 --threshold 2.5
    """

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] in ['-h', '--help']:
        print(usage())
        sys.exit(0)

    parser = argparse.ArgumentParser(description="Real-time Anomaly Detection",
                                     usage=usage())
    parser.add_argument('--detector', type=str, default='rolling_average',
                        choices=['rolling_average', 'zscore'],
                        help='Type of anomaly detector to use')
    parser.add_argument('--window', type=int, default=100,
                        help='Window size for the detector')
    parser.add_argument('--threshold', type=float, default=3.0,
                        help='Threshold for anomaly detection')

    args = parser.parse_args()

    main(args.detector, args.window, args.threshold)