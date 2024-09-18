import bisect
import matplotlib.pyplot as plt
from matplotlib.backend_bases import Event
import numpy as np


class Visualizer:
    """
    a class for visualizing real-time data stream with anomaly detection.

    the Visualizer provides a mechanism to plot a data stream in real-time,
    highlighting detected anomalies and showing a rolling window for better
    insight into recent data points.

    Attributes:
        max_points (int): Maximum number of points displayed in the plot.
        window_size (int): Size of the rolling window used for display.
        shift_size (int): Number of points to shift the window when the plot
            view updates.
        values (list): List of values to plot on the y-axis.
        anomalies (list): Boolean list indicating which points are anomalies.
        times (list): List of time points corresponding to the values.
        is_closed (bool): Flag to indicate whether the plot is closed.
        x_start (int): Starting position for the x-axis (time).
        fig (matplotlib.figure.Figure): Matplotlib figure object for the plot.
        ax (matplotlib.axes._axes.Axes): Matplotlib axes object for the plot.
        normal_line (matplotlib.lines.Line2D): Line object for plotting normal values.
        anomaly_scatter (matplotlib.collections.PathCollection): Scatter plot object for anomalies.
        window_lines (list): List of vertical lines representing the rolling window.
    """

    def __init__(self, max_points: int = 1000, window_size: int = 100, shift_size: int = 700):
        """
        initialize the Visualizer object.

        Args:
            max_points (int): Maximum number of points to display on the x-axis.
                default is 1000.
            window_size (int): Size of the rolling window to display.
                default is 100.
            shift_size (int): Number of points to shift the window when updating the view.
                default is 700.
        """
        self.max_points = max_points
        self.window_size = window_size
        self.shift_size = shift_size
        self.values = []
        self.anomalies = []
        self.times = []
        self.is_closed = False
        self.x_start = 0

        plt.ion()  # Turn on interactive mode
        self.fig, self.ax = plt.subplots(figsize=(12, 6))
        self.normal_line, = self.ax.plot([], [], lw=2, color='blue', label='Normal')
        self.anomaly_scatter = self.ax.scatter([], [], color='red', s=50, label='Anomaly')
        self.window_lines = []

        self.ax.set_ylim(0, 200)
        self.ax.set_xlim(0, self.max_points)
        self.ax.grid(True)
        self.ax.set_title('Data Stream Anomaly Detection')
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Value')
        self.ax.legend()

        self.fig.canvas.mpl_connect('close_event', self.on_close)

    def on_close(self, _: Event) -> None:
        """
        Handle the event when the plot is closed.

        Args:
            _: The event object for the plot closing event (unused).

        Returns:
            None
        """
        self.is_closed = True

    def update(self, value: float, is_anomaly: bool, time: float) -> None:
        """
        update the data stream with a new value and anomaly status.

        Args:
            value (float): The new value to add to the data stream.
            is_anomaly (bool): Whether the new value is an anomaly.
            time (float): The time corresponding to the new value.

        Returns:
            None
        """
        self.values.append(value)
        self.anomalies.append(is_anomaly)
        self.times.append(time)

    def update_plot(self) -> None:
        """
        Update the plot with the latest data, including normal values and anomalies.

        This method shifts the plot view if necessary and highlights anomalies
        within the defined rolling window.

        Returns:
            None
        """
        if not self.is_closed:
            current_time = self.times[-1]

            # Shift the view if necessary
            if current_time >= self.x_start + self.max_points:
                self.x_start = current_time - self.max_points + self.shift_size

            # Update x-axis limits
            self.ax.set_xlim(self.x_start, self.x_start + self.max_points)

            # Calculate visible range
            visible_start = max(0, bisect.bisect_left(self.times, self.x_start))
            visible_end = bisect.bisect_right(self.times, self.x_start + self.max_points)

            visible_times = self.times[visible_start:visible_end]
            visible_values = self.values[visible_start:visible_end]

            # Update normal line
            self.normal_line.set_data(visible_times, visible_values)

            # Update anomaly scatter
            anomaly_times = [t for t, a in zip(visible_times, self.anomalies[visible_start:visible_end]) if a]
            anomaly_values = [v for v, a in zip(visible_values, self.anomalies[visible_start:visible_end]) if a]
            self.anomaly_scatter.set_offsets(np.c_[anomaly_times, anomaly_values])

            # Update rolling window lines
            for line in self.window_lines:
                line.remove()
            self.window_lines = []

            # Show the current window
            current_window_size = min(len(visible_times), self.window_size)
            if current_window_size > 0:
                window_start = visible_times[-current_window_size]
                window_end = visible_times[-1]
                start_line = self.ax.axvline(window_start, color='gray', linestyle='--', alpha=0.5)
                end_line = self.ax.axvline(window_end, color='gray', linestyle='--', alpha=0.5)
                self.window_lines.extend([start_line, end_line])

            self.ax.relim()
            self.ax.autoscale_view(scalex=False, scaley=True)

            self.fig.canvas.draw()
            self.fig.canvas.flush_events()

    def close(self) -> None:
        """
        Close the plot window.

        Returns:
            None
        """
        plt.close(self.fig)
