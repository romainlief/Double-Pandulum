from simulation import Simulation
from dpandulum import DoublePendulum

if __name__ == "__main__":
    pendulum = DoublePendulum(
        L1=1.0,
        L2=0.7,
        angle1=1.06465,
        angle2=1.06465,
        m1=1.0,
        m2=0.5,
        color="tab:blue",
        g=9.81,
    )
    pandulum2 = DoublePendulum(
        L1=1.0,
        L2=0.7,
        angle1=1.06465 + 0.01,
        angle2=1.06465 + 0.01,
        m1=1.0,
        m2=0.5,
        color="tab:orange",
        g=9.81,
    )

    sim = Simulation([pendulum, pandulum2], dt=0.005)
    sim.run()