import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np


class Simulation:
    def __init__(self, pendulums, trail_length=100, dt=0.02):
        self.pendulums = pendulums  # liste de DoublePendulum
        self.trail_length = trail_length
        self.dt = dt
        self.hue_step = 0.02  # incrément de teinte à chaque nouveau point
        self.trail_colors = []  # liste de listes de teintes (par pendule)
        self.hue_cursors = []  # teinte courante par pendule

        plt.style.use("dark_background")
        self.fig, self.ax = plt.subplots()
        self.ax.set_aspect("equal")
        self.ax.set_xlim(
            -sum(p.L1 + p.L2 for p in pendulums), sum(p.L1 + p.L2 for p in pendulums)
        )
        self.ax.set_ylim(
            -sum(p.L1 + p.L2 for p in pendulums), sum(p.L1 + p.L2 for p in pendulums)
        )

        self.lines = []
        self.masses = []
        self.trails = []
        color_map = ["PuBu", "Wistia"]

        for i, p in enumerate(pendulums):
            # segment du pendule
            (line,) = self.ax.plot([], [], lw=3, color=p.color)
            self.lines.append(line)

            # masses (cercles)
            (mass1,) = self.ax.plot([], [], "o", color=p.color, markersize=7)
            (mass2,) = self.ax.plot([], [], "o", color=p.color, markersize=7)
            self.masses.append((mass1, mass2))

            # traînées
            # utilisation d'un scatter avec une palette 'hsv' pour l'effet arc-en-ciel
            trail = self.ax.scatter(
                [], [], s=6, c=[], cmap=color_map[i], vmin=0, vmax=1, alpha=0.8
            )
            self.trails.append(trail)
            # init couleurs de la traînée
            self.trail_colors.append([])
            self.hue_cursors.append(0.0)

    def init_func(self):
        for line in self.lines:
            line.set_data([], [])
        for mass_pair in self.masses:
            for m in mass_pair:
                m.set_data([], [])
        for trail in self.trails:
            trail.set_offsets(np.empty((0, 2)))
            trail.set_array(np.array([]))
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
            # Traînée colorée avec couleurs fixes par point
            # Ajoute des teintes pour les nouveaux points ajoutés à p.positions
            total_positions = len(p.positions)
            existing_colors = len(self.trail_colors[i])
            if total_positions > existing_colors:
                new_count = total_positions - existing_colors
                new_hues = (
                    self.hue_cursors[i] + np.arange(new_count) * self.hue_step
                ) % 1.0
                self.trail_colors[i].extend(new_hues.tolist())
                self.hue_cursors[i] = (
                    self.hue_cursors[i] + new_count * self.hue_step
                ) % 1.0

            trail_positions = np.array(p.positions[-self.trail_length :])
            if len(trail_positions) > 0:
                trail_x = trail_positions[:, 2]  # x2
                trail_y = trail_positions[:, 3]  # y2
                offsets = np.column_stack((trail_x, trail_y))
                # couleurs correspondantes des mêmes points
                colors_slice = np.array(self.trail_colors[i][-len(trail_positions) :])
                self.trails[i].set_offsets(offsets)
                self.trails[i].set_array(colors_slice)

        return self.lines + [m for pair in self.masses for m in pair] + self.trails

    def run(self, interval=20):
        anim = FuncAnimation(
            self.fig,
            self.update_func,
            init_func=self.init_func,
            frames=1000,
            interval=interval,
            blit=True,
        )
        plt.show()
