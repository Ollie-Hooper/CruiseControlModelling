import numpy as np

import matplotlib.pyplot as plt

from scipy.integrate import odeint

from cruise.classes import Car


def main():
    car = Car(1611, [1.443, 1.849, 4.694], 0.23, 211000, 240, 62.5856, [0.216, 0.2285])

    t = np.linspace(0, 200, 200)
    v0 = 0

    v = odeint(car.acceleration, v0, t)

    plt.plot(t, v*3.6)
    plt.show()


if __name__ == "__main__":
    main()