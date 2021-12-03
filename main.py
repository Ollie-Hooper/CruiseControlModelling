import numpy as np

import matplotlib.pyplot as plt

from scipy.integrate import odeint

from cruise.classes import Car, TorquePlotting


def main():
    car = Car(1611, [1.443, 1.849, 4.694], 0.23, 211000, 450, 62.5856, [0.216, 0.2285])
  #  car = Car(19000, [2.5,5.875,3.993], 0.8, 324000, 2100, 37.5514, [0.315, 0.5717])
    curves = TorquePlotting(211000, 450)

    # solving the ODE to find velocity
    t = np.linspace(0, 200, 200)
    v0 = 0

    v = odeint(car.acceleration, v0, t)
    v1 = []
    for i in v:
        v1.append(i*2.23694)

    plt.subplot(1, 2, 1)
    plt.plot(t, v*3.6)
    plt.xlabel('Time $t$ [s]')
    plt.ylabel('Velocity $v$ [m/s]')
    plt.grid(True, linestyle='dotted')

    plt.subplot(1, 2, 2)
    plt.plot(t, v1, 'r')
    plt.xlabel('Time $t$ [s]')
    plt.ylabel('Velocity $v$ [mph]')
    plt.grid(True, linestyle='dotted')

    plt.suptitle('Velocity over time of Tesla model 3')
    plt.show()

    # plotting the torque graphs (against angular velocity and velocity)
    plt.subplot(1, 2, 1)
    omega_range = np.linspace(0, 700, 701)  # max angular velocity found from P = tw
    plt.plot(omega_range, [curves.torque_curves(w) for w in omega_range])
    plt.xlabel('Angular velocity $\omega$ [rad/s]')
    plt.ylabel('Torque $T$ [Nm]')
    plt.grid(True, linestyle='dotted')

    plt.subplot(1, 2, 2)
    v_range = np.linspace(0, 63, 64)  # max velocity is 62.5856 m/s
    alpha = [40, 25, 16, 12, 10]
    for gear in range(5):
        omega_range = alpha[gear] * v_range
        plt.plot(v_range, [curves.torque_curves(w) for w in omega_range])
    plt.grid(True, linestyle='dotted')
    plt.xlabel('Velocity $v$ [m/s]')
    plt.ylabel('Torque $T$ [Nm]')

    plt.show()


if __name__ == "__main__":
    main()
