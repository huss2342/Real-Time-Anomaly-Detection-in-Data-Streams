import asyncio
from data_stream import DataStreamSimulator
from anomaly_detector import RollingAverageDetector
from stream_processor import StreamProcessor
from visualizer import Visualizer

async def main():
    simulator = DataStreamSimulator()
    detector = RollingAverageDetector()
    visualizer = Visualizer()
    processor = StreamProcessor(simulator, detector, visualizer)
    await processor.process_stream()

if __name__ == "__main__":
    asyncio.run(main())