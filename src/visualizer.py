import bisect

import matplotlib.pyplot as plt
import numpy as np


class Visualizer:
    def __init__(self, max_points: int = 1000, window_size: int = 100, shift_size: int = 700):
        self.max_points = max_points
        self.window_size = window_size
        self.shift_size = shift_size
        self.values = []
        self.anomalies = []
        self.times = []
        self.is_closed = False
        self.x_start = 0

        plt.ion()
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

    def on_close(self, event):
        self.is_closed = True

    def update(self, value: float, is_anomaly: bool, time: float):
        self.values.append(value)
        self.anomalies.append(is_anomaly)
        self.times.append(time)

    def update_plot(self):
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

    def close(self):
        plt.close(self.fig)