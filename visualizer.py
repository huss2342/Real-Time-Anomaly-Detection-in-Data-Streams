import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

class Visualizer:
    def __init__(self, max_points: int = 1000):
        self.max_points = max_points
        self.values = np.array([])
        self.anomalies = np.array([], dtype=bool)
        self.time = np.array([])

        # Set up the plot
        plt.ion()  # Turn on interactive mode
        self.fig, self.ax = plt.subplots(figsize=(12, 6))
        self.normal_line, = self.ax.plot([], [], lw=2, color='blue', label='Normal')
        self.anomaly_line, = self.ax.plot([], [], 'ro', markersize=5, label='Anomaly')

        self.ax.set_ylim(0, 200)
        self.ax.set_xlim(0, self.max_points)
        self.ax.grid(True)
        self.ax.set_title('Data Stream Anomaly Detection')
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Value')
        self.ax.legend()

    def update(self, value: float, is_anomaly: bool, time: float):
        self.values = np.append(self.values, value)
        self.anomalies = np.append(self.anomalies, is_anomaly)
        self.time = np.append(self.time, time)

        if len(self.values) > self.max_points:
            self.values = self.values[-self.max_points:]
            self.anomalies = self.anomalies[-self.max_points:]
            self.time = self.time[-self.max_points:]

    def update_plot(self):
        self.normal_line.set_data(self.time[~self.anomalies], self.values[~self.anomalies])
        self.anomaly_line.set_data(self.time[self.anomalies], self.values[self.anomalies])

        self.ax.relim()
        self.ax.autoscale_view()

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def close(self):
        plt.close(self.fig)