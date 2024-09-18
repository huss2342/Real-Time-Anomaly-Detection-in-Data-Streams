import asyncio
import logging

class StreamProcessor:
    def __init__(self, detector, visualizer, data_stream, debug: bool):
        self.detector = detector
        self.visualizer = visualizer
        self.data_stream = data_stream
        self.time = 0
        self.debug = debug

    async def process_stream(self, logger, num_points: int = None):
        stream = self.data_stream.generate_stream()

        while (num_points is None or self.time < num_points) and not self.visualizer.is_closed:
            value = next(stream)
            is_anomaly = self.detector.detect(value)
            self.visualizer.update(value, is_anomaly, self.time)

            if self.debug:
                logger.debug(f"Time: {self.time}, Value: {value}, Is Anomaly: {is_anomaly}")

            self.visualizer.update_plot()

            self.time += 1

            if num_points is not None and self.time >= num_points:
                break

            await asyncio.sleep(0.1)

        if self.visualizer.is_closed:
            logger.info("Visualizer window was closed. Stopping the stream processing.")

    async def run_async(self, logger, num_points: int = None):
        await self.process_stream(logger, num_points)

    def run(self, logger, num_points: int = None):
        try:
            asyncio.run(self.run_async(logger, num_points))
        except KeyboardInterrupt:
            logger.info("StreamProcessor: Stream processing interrupted by user.")
        finally:
            self.visualizer.close()