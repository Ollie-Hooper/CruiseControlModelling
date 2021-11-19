import numpy as np
from cruise.classes import Car


class TorquePlotting:

    def __init__(self, power, torque):
        self.power = power
        self.torque = torque

    def torque_curves(self, omega):
        t = self.torque  # engine torque constant (max torque)
        omega_m = self.power / t  # max angular velocity
        beta = 0.4  # max engine rolloff (because you cant move with a torque below a certain value)

        return np.clip(t * (1 - beta * (omega / omega_m - 1) ** 2), 0, None)
