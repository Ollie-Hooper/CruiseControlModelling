from math import cos, sin, pi
import numpy as np


class Car:

    def __init__(self, mass, dimensions, drag_coefficient, power, torque, top_speed, wheel_dimensions):
        self.mass = mass
        self.height = dimensions[0]
        self.width = dimensions[1]
        self.length = dimensions[2]
        self.Cd = drag_coefficient
        self.power = power
        self.peak_torque = torque
        self.top_speed = top_speed
        self.wheel_width = wheel_dimensions[0]
        self.wheel_radius = wheel_dimensions[1]

        self.gear_ratio = 500

        self.mu = 0.25
        self.g = -9.81
        self.air_density = 1
        self.angle = 0

        self.speed = 0

    def cross_sectional_area(self):
        return self.height * self.width

    def torque(self, v):
        gear_ratio = self.gear_ratio
        r = self.wheel_radius
        wheel_rpm = v / (2*pi*r)
        engine_rpm = wheel_rpm * gear_ratio

        width = 100
        peak_torque = self.peak_torque
        peak_torque_rpm = 3500
        min_rpm = 2320
        max_rpm = 4500

        if engine_rpm < min_rpm:
            return 100
        elif engine_rpm > max_rpm:
            return 0
        else:
            return -((1/width)**2)*(engine_rpm - peak_torque_rpm)**2 + peak_torque

    def acc_force(self, v):
        t = self.torque(v)
        r = self.wheel_radius
        a = self.angle
        return t / r #* sin(a))

    def friction(self):
        mu = self.mu
        M = self.mass
        g = self.g
        a = self.angle
        return mu * M * g * cos(a)

    def weight(self):
        m = self.mass
        g = self.g
        a = self.angle
        return m * g * sin(a)

    def drag(self, v):
        Cd = self.Cd
        A = self.cross_sectional_area()
        rho = self.air_density
        a = self.angle
        return 0.5 * Cd * A * rho * v ** 2

    def acceleration(self, v, t):
        v = v[0]
        A = self.acc_force(v)
        F = self.friction()
        W = self.weight()
        d = self.drag(v)
        m = self.mass
        return (A - F - W - d) / m


class TorquePlotting:

    def __init__(self, power, torque):
        self.power = power
        self.torque = torque

    def torque_curves(self, omega):
        t = self.torque  # engine torque constant (max torque)
        omega_m = self.power / t  # max angular velocity
        beta = 0.4  # max engine rolloff (because you cant move with a torque below a certain value)

        return np.clip(t * (1 - beta * (omega / omega_m - 1) ** 2), 0, None)
