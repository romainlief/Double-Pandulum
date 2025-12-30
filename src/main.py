from simulation import Simulation
from dpandulum import DoublePendulum

if __name__ == "__main__":
    pendulum = DoublePendulum(
        L1=1.0,
        L2=1.0,
        angle1=1.06465,
        angle2=1.06465,
        color="tab:blue",
        g=9.81,
    )

    sim = Simulation([pendulum], dt=0.005)
    sim.run()
