import asyncio
from data_stream import DataStreamSimulator
from anomaly_detector import AnomalyDetector
from visualizer import Visualizer

class StreamProcessor:
    def __init__(self, detector: AnomalyDetector, visualizer: Visualizer, data_stream: DataStreamSimulator):
        self.detector = detector
        self.visualizer = visualizer
        self.data_stream = data_stream
        self.time = 0

    async def process_stream(self, num_points: int = None):
        stream = self.data_stream.generate_stream()

        while num_points is None or self.time < num_points:
            value = next(stream)
            is_anomaly = self.detector.detect(value)
            self.visualizer.update(value, is_anomaly, self.time)
            self.visualizer.update_plot()

            self.time += 1

            if num_points is not None and self.time >= num_points:
                break

            await asyncio.sleep(0.1)

    async def run_async(self, num_points: int = None):
        await self.process_stream(num_points)

    def run(self, num_points: int = None):
        try:
            asyncio.get_event_loop().run_until_complete(self.run_async(num_points))
        except KeyboardInterrupt:
            print("StreamProcessor: Stream processing interrupted by user.")