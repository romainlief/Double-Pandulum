from simulation import Simulation
from dpandulum import DoublePendulum

if __name__ == "__main__":
    pendulum = DoublePendulum(
        L1=1.5,
        L2=1.5,
        angle1=1.06465,
        angle2=2.36465,
        color="tab:blue",
        g=7.81,
    )
    pandulum2 = DoublePendulum(
        L1=1.5,
        L2=1.5,
        angle1=1.06465 + 0.1,
        angle2=2.36465,
        color="tab:orange",
        g=7.81,
    )

    sim = Simulation([pendulum, pandulum2], dt=0.02)
    sim.run()
