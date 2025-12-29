import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

class Simulation:
    def __init__(self, pendulums, trail_length=200, dt=0.02):
        self.pendulums = pendulums  # liste de DoublePendulum
        self.trail_length = trail_length
        self.dt = dt

        # Setup Matplotlib
        self.fig, self.ax = plt.subplots()
        self.ax.set_aspect('equal')
        self.ax.set_xlim(-sum(p.L1 + p.L2 for p in pendulums),
                         sum(p.L1 + p.L2 for p in pendulums))
        self.ax.set_ylim(-sum(p.L1 + p.L2 for p in pendulums),
                         sum(p.L1 + p.L2 for p in pendulums))

        self.lines = []
        self.masses = []
        self.trails = []

        for p in pendulums:
            # segment du pendule
            line, = self.ax.plot([], [], lw=3, color=p.color)
            self.lines.append(line)

            # masses (cercles)
            mass1, = self.ax.plot([], [], 'o', color=p.color, markersize=10)
            mass2, = self.ax.plot([], [], 'o', color=p.color, markersize=10)
            self.masses.append((mass1, mass2))

            # traînées
            trail, = self.ax.plot([], [], lw=1, color=p.color, alpha=0.6)
            self.trails.append(trail)

    def init_func(self):
        for line in self.lines:
            line.set_data([], [])
        for mass_pair in self.masses:
            for m in mass_pair:
                m.set_data([], [])
        for trail in self.trails:
            trail.set_data([], [])
        return self.lines + [m for pair in self.masses for m in pair] + self.trails

    def update_func(self, frame):
        for i, p in enumerate(self.pendulums):
            p.update(self.dt)
            x1, y1, x2, y2 = p.compute_position()

            # Segment
            self.lines[i].set_data([0, x1, x2], [0, y1, y2])
            # Masses
            self.masses[i][0].set_data([x1], [y1])
            self.masses[i][1].set_data([x2], [y2])
            # Traînée
            trail_positions = np.array(p.positions[-self.trail_length:])
            if len(trail_positions) > 0:
                trail_x = trail_positions[:, 2]  # x2
                trail_y = trail_positions[:, 3]  # y2
                self.trails[i].set_data(trail_x, trail_y)

        return self.lines + [m for pair in self.masses for m in pair] + self.trails

    def run(self, interval=20):
        anim = FuncAnimation(
            self.fig,
            self.update_func,
            init_func=self.init_func,
            frames=1000,
            interval=interval,
            blit=True
        )
        plt.show()
