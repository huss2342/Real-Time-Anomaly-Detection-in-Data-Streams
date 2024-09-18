import asyncio


class StreamProcessor:
    """
    a class to process a data stream, detect anomalies, and visualize the results.

    this processor handles the continuous processing of a data stream, detecting
    anomalies using a provided detector, and updating a visualizer with the results.

    Attributes:
        detector: An object with a 'detect' method for identifying anomalies.
        visualizer: An object for visualizing the data stream and anomalies.
        data_stream: An object with a 'generate_stream' method for producing data.
        time (int): A counter for tracking the current time step.
        debug (bool): Flag to enable or disable debug logging.
    """

    def __init__(self, detector, visualizer, data_stream, debug: bool):
        """
        initialize the StreamProcessor with the given components.
        """
        self.detector = detector
        self.visualizer = visualizer
        self.data_stream = data_stream
        self.time = 0
        self.debug = debug

    async def process_stream(self, logger, num_points: int = None):
        """
        asynchronously process the data stream, detect anomalies, and update the visualizer.

        this method continuously processes data points from the stream until either
        the specified number of points is reached or the visualizer is closed.

        Args:
            logger: A logging object for debug and info messages.
            num_points (int, optional): The number of points to process.
            if None, process indefinitely.

        Returns:
            None
        """
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
        """
        asynchronously run the stream processor.

        this method is a wrapper around process_stream, allowing for easy
        asynchronous execution.

        Args:
            logger: A logging object for debug and info messages.
            num_points (int, optional): The number of points to process.
            if None, process indefinitely.

        Returns:
            None
        """
        await self.process_stream(logger, num_points)

    def run(self, logger, num_points: int = None):
        """
        run the stream processor synchronously.

        this method provides a synchronous interface to run the asynchronous
        stream processing, handling keyboard interrupts, and cleanup.

        Args:
            logger: A logging object for debug and info messages.
            num_points (int, optional): The number of points to process.
            if None, process indefinitely.

        Returns:
            None
        """
        try:
            asyncio.run(self.run_async(logger, num_points))
        except KeyboardInterrupt:
            logger.info("StreamProcessor: Stream processing interrupted by user.")
        finally:
            self.visualizer.close()
