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
    pandulum2 = DoublePendulum(
        L1=1.0,
        L2=0.7,
        angle1=1.06465 + 0.01,
        angle2=1.06465 + 0.01,
        color="tab:orange",
        g=9.81,
    )

    sim = Simulation([pendulum, pandulum2], dt=0.01)
    sim.run()