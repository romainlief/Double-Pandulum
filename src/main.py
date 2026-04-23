from simulation import Simulation
from dpandulum import DoublePendulum

if __name__ == "__main__":
    pendulum = []
    for i in range(25):
        pendulum.append(
            DoublePendulum(
                L1=1.5,
                L2=1.5,
                angle1=3.06465 + i * 0.0001,
                angle2=1.86465,
                color="tab:blue",
                g=7.81,
            )
        )

    sim = Simulation(pendulum, dt=0.015)
    sim.run()
