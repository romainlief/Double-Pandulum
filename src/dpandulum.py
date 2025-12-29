import numpy as np
from scipy.integrate import solve_ivp

class DoublePendulum:
    def __init__(self, L1, L2, angle1, angle2, color, g=9.81):
        self.L1 = L1
        self.L2 = L2
                
        self.angle1 = angle1
        self.angle2 = angle2
        
        self.p1 = 0.0
        self.p2 = 0.0
        
        self.color = color
        self.g = g
        self.positions = []
        self.t = 0.0
        self.cycle = 0

    def update(self, dt=0.02):
        y0 = [self.angle1, self.angle2, self.p1, self.p2]

        sol = solve_ivp(
            self.derivatives,
            t_span=(self.t, self.t + dt),
            y0=y0,
            method="RK45",
            rtol=1e-9,
            atol=1e-9
        )

        self.angle1, self.angle2, self.p1, self.p2 = sol.y[:, -1]
        self.t += dt

        self.positions.append(self.compute_position())
        self.cycle = (self.cycle + 1) % 360

    def compute_position(self):
        x1 = self.L1 * np.sin(self.angle1)
        y1 = -self.L1 * np.cos(self.angle1)
        x2 = x1 + self.L2 * np.sin(self.angle2)
        y2 = y1 - self.L2 * np.cos(self.angle2)
        return (x1, y1, x2, y2)

    def derivatives(self, t, y):
        a1, a2, p1, p2 = y
        delta = a1 - a2
        cos_d = np.cos(delta)
        sin_d = np.sin(delta)

        denom = 16 - 9 * cos_d**2

        # vitesses angulaires
        a1_dot = self.g * (2 * p1 - 3 * cos_d * p2) / denom
        a2_dot = self.g * (8 * p2 - 3 * cos_d * p1) / denom

        # dérivées des moments
        p1_dot = -(a1_dot * a2_dot * sin_d + 3 * self.g * np.sin(a1))
        p2_dot = -(-a1_dot * a2_dot * sin_d + self.g * np.sin(a2))

        return [a1_dot, a2_dot, p1_dot, p2_dot]
