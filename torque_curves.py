import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from cruise.classes import Car


def torque(omega):
    tc = 450  # engine torque constant (max torque)
    omega_m = 468.89  # max angular velocity
    beta = 0.4  # max engine rolloff (because you cant move with a torque below a certain value)

    return np.clip(tc * (1 - beta * (omega / omega_m - 1) ** 2), 0, None)


# torque plotted against angular velocity
plt.subplot(1, 2, 1)
omega_range = np.linspace(0, 700, 701)  # max angular velocity found from P = tw with max t and P values, = 468.89 rad/s
plt.plot(omega_range, [torque(w) for w in omega_range])
plt.xlabel('Angular velocity $\omega$ [rad/s]')
plt.ylabel('Torque $T$ [Nm]')
plt.grid(True, linestyle='dotted')

plt.subplot(1, 2, 2)
v_range = np.linspace(0, 63, 64)  # max velocity is 62.5856 m/s
alpha = [40, 25, 16, 12, 10]
for gear in range(5):
    omega_range = alpha[gear] * v_range
    plt.plot(v_range, [torque(w) for w in omega_range])
plt.grid(True, linestyle='dotted')
plt.xlabel('Velocity $v$ [m/s]')
plt.ylabel('Torque $T$ [Nm]')

plt.show()
