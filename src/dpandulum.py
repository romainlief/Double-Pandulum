import numpy as np
from scipy.integrate import solve_ivp


class DoublePendulum:
    def __init__(self, L1, L2, angle1, angle2, color, m1=1.0, m2=1.0, g=9.81):
        self.L1 = L1
        self.L2 = L2
        self.m1 = m1
        self.m2 = m2
        self.g = g

        # angles initiaux
        self.theta1 = angle1
        self.theta2 = angle2

        # vitesses angulaires initiales
        self.omega1 = 0.0
        self.omega2 = 0.0

        self.color = color
        self.positions = []
        self.t = 0.0
        self.cycle = 0

    def derivatives(self, t, y):
        theta1, theta2, omega1, omega2 = y

        m1, m2 = self.m1, self.m2
        L1, L2 = self.L1, self.L2
        g = self.g

        delta = theta1 - theta2

        dtheta1_dt = omega1
        dtheta2_dt = omega2

        denom1 = L1 * (2 * m1 + m2 - m2 * np.cos(2 * delta))
        denom2 = L2 * (2 * m1 + m2 - m2 * np.cos(2 * delta))

        domega1_dt = (
            -g * (2 * m1 + m2) * np.sin(theta1)
            - m2 * g * np.sin(theta1 - 2 * theta2)
            - 2 * np.sin(delta) * m2 * (omega2**2 * L2 + omega1**2 * L1 * np.cos(delta))
        ) / denom1

        domega2_dt = (
            2
            * np.sin(delta)
            * (
                omega1**2 * L1 * (m1 + m2)
                + g * (m1 + m2) * np.cos(theta1)
                + omega2**2 * L2 * m2 * np.cos(delta)
            )
        ) / denom2

        return [dtheta1_dt, dtheta2_dt, domega1_dt, domega2_dt]

    def compute_position(self):
        # position de la première masse
        x1 = self.L1 * np.sin(self.theta1)
        y1 = -self.L1 * np.cos(self.theta1)

        # position de la seconde masse
        x2 = x1 + self.L2 * np.sin(self.theta2)
        y2 = y1 - self.L2 * np.cos(self.theta2)

        return (x1, y1, x2, y2)

    def update(self, dt=0.02):
        y0 = [self.theta1, self.theta2, self.omega1, self.omega2]

        sol = solve_ivp(
            self.derivatives,
            t_span=(self.t, self.t + dt),
            y0=y0,
            method="RK45",
            rtol=1e-9,
            atol=1e-9,
        )

        self.theta1, self.theta2, self.omega1, self.omega2 = sol.y[:, -1]
        self.t += dt

        self.positions.append(self.compute_position())
        self.cycle = (self.cycle + 1) % 360
