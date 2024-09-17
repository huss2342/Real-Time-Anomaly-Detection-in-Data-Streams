import asyncio
from data_stream import DataStreamSimulator
from anomaly_detector import AnomalyDetector
from visualizer import Visualizer

class StreamProcessor:
    def __init__(self, detector: AnomalyDetector, visualizer: Visualizer, data_stream: DataStreamSimulator):
        self.detector = detector
        self.visualizer = visualizer
        self.data_stream = data_stream

    async def process_stream(self):
        for value in self.simulator.generate_stream():
            is_anomaly = self.detector.detect(value)
            await self.visualizer.update(value, is_anomaly)
            await asyncio.sleep(0.1)
