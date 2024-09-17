import matplotlib.pyplot as plt

class Visualizer:
    def __init__(self, max_points: int = 1000):
        self.max_points = max_points
        self.values = []
        self.anomalies = []
        self.fig, self.ax = plt.subplots()
        self.line, = self.ax.plot([], [], lw=2)
        self.ax.set_ylim(0, 200)
        self.ax.set_xlim(0, self.max_points)
        self.ax.grid()
        self.ax.set_title('Data Stream')
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Value')
        self.ax.plot([], [], lw=2)
        self.ax.plot([], [], lw=2)

    async def update(self, value: float, is_anomaly: bool):
        self.values.append(value)
        self.anomalies.append(is_anomaly)
        if len(self.values) > self.max_points:
            self.values.pop(0)
            self.anomalies.pop(0)
        self.line.set_data(range(len(self.values)), self.values)
        self.line.set_color(['r' if a else 'b' for a in self.anomalies])
        self.ax.relim()
        self.ax.autoscale_view()
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        plt.pause(0.1)