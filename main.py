import numpy as np

import matplotlib.pyplot as plt

from scipy.integrate import odeint

from cruise.classes import Car


def main():
    audi = Car("Audi S4 Saloon", 1795, 2.04, 0.31, (100, 410), (0.216, 0.2286), (1500, 6500),
               {1: 3.665, 2: 1.999, 3: 1.407, 4: 1.000, 5: 0.742}, 3.511)  # Audi S4 Saloon
    man = Car("MAN TGX", 19000, 23.459, 0.8, (100, 2100), (0.315, 0.28575), (1500, 4500),
              {1: 16.41, 2: 13.28, 3: 11.32, 4: 9.16, 5: 7.19, 6: 5.82, 7: 4.63, 8: 3.75, 9: 3.02, 10: 2.44, 11: 1.92,
               12: 1.55, 13: 1.24, 14: 1.0}, 2.53)  # MAN TGX

    # solving the ODE to find velocity
    t = np.linspace(0, 100, 1000)
    v0 = 0

    v_audi = odeint(audi.acceleration, v0, t)

    v_man = odeint(man.acceleration, v0, t)

    plt.subplot(1, 2, 1)
    plt.title(f'Velocity of {audi.name}')
    plt.plot(t, v_audi * 2.2369362920544025)
    plt.xlabel('Time $t$ [s]')
    plt.ylabel('Velocity $v$ [mph]')
    plt.grid(True, linestyle='dotted')

    plt.subplot(1, 2, 2)
    plt.title(f'Velocity of {man.name}')
    plt.plot(t, v_man * 2.2369362920544025, 'r')
    plt.xlabel('Time $t$ [s]')
    plt.ylabel('Velocity $v$ [mph]')
    plt.grid(True, linestyle='dotted')

    plt.tight_layout()

    plt.show()

    audi.plot_torques()
    man.plot_torques()


if __name__ == "__main__":
    main()
