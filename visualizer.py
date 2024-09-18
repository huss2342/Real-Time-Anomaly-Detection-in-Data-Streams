import matplotlib.pyplot as plt
import numpy as np

class Visualizer:
    def __init__(self, max_points: int = 1000):
        self.max_points = max_points
        self.values = []
        self.anomalies = []
        self.times = []

        plt.ion()
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
        self.values.append(value)
        self.anomalies.append(is_anomaly)
        self.times.append(time)

        if len(self.values) > self.max_points:
            self.values = self.values[-self.max_points:]
            self.anomalies = self.anomalies[-self.max_points:]
            self.times = self.times[-self.max_points:]

    def update_plot(self):
        normal_times = [t for t, a in zip(self.times, self.anomalies) if not a]
        normal_values = [v for v, a in zip(self.values, self.anomalies) if not a]
        anomaly_times = [t for t, a in zip(self.times, self.anomalies) if a]
        anomaly_values = [v for v, a in zip(self.values, self.anomalies) if a]

        self.normal_line.set_data(normal_times, normal_values)
        self.anomaly_line.set_data(anomaly_times, anomaly_values)

        self.ax.relim()
        self.ax.autoscale_view()

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def close(self):
        plt.close(self.fig)