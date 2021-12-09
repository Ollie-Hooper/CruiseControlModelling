from math import cos, sin, pi
import numpy as np
import matplotlib.pyplot as plt


class Car:

    def __init__(self, name, mass, frontal_area, drag_coefficient, torque, wheel_dimensions, engine_rpm, gears,
                 final_drive):
        self.name = name
        self.mass = mass
        self.frontal_area = frontal_area
        self.Cd = drag_coefficient
        self.min_torque = torque[0]
        self.max_torque = torque[1]
        self.wheel_width = wheel_dimensions[0]
        self.wheel_radius = wheel_dimensions[1]

        self.min_engine_rpm = engine_rpm[0]
        self.max_engine_rpm = engine_rpm[1]

        self.drivetrain_efficiency = 0.841

        self.gear = 1
        self.gears = gears
        self.final_drive_ratio = final_drive

        self.mu = 0.25
        self.g = -9.81
        self.air_density = 1
        self.angle = 0

        self.speed = 0

        # PID parameters
        self.v_req = 0  # required speed
        self.input = False  # PID controller output/plant input (Feedback path)

    def torque(self, v):
        radius = self.wheel_radius
        t_min = self.min_torque
        t_max = self.max_torque
        r_min = self.min_engine_rpm
        r_max = self.max_engine_rpm

        a = 4 * (t_max - t_min) / (r_max - r_min) ** 2

        r_peak = (r_max + r_min) / 2

        wheel_rpm = (v / (2 * pi * radius)) * 60

        gear_ratio = self.gears[self.gear] * self.final_drive_ratio
        engine_rpm = wheel_rpm * gear_ratio

        if engine_rpm <= r_min:
            # Check if first gear
            if self.gear == 1:
                return t_min * gear_ratio
            # Change down gear
            self.gear -= 1
        elif engine_rpm >= r_peak:
            # Check not top gear
            if self.gear != len(self.gears):
                # Change up gear
                self.gear += 1

        if engine_rpm >= r_max:
            # Check if top gear
            if self.gear == len(self.gears):
                return 0

        gear_ratio = self.gears[self.gear] * self.final_drive_ratio
        engine_rpm = wheel_rpm * gear_ratio

        r = engine_rpm

        t = -a * (r - r_peak) ** 2 + t_max

        return t * gear_ratio

    def acc_force(self, v):
        t = self.torque(v) * self.drivetrain_efficiency
        r = self.wheel_radius
        return t / r

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
        A = self.frontal_area
        rho = self.air_density
        a = self.angle
        return 0.5 * Cd * A * rho * v ** 2

    def acceleration(self, v, t):
        if self.input != False:
            if self.v_req != v:
                v += self.input

        A = self.acc_force(v)
        W = self.weight()
        d = self.drag(v)
        m = self.mass

        a = (A - W - d) / m

        return a

    def engine_torque_curve(self):
        t_min = self.min_torque
        t_max = self.max_torque
        r_min = self.min_engine_rpm
        r_max = self.max_engine_rpm

        a = 4 * (t_max - t_min) / (r_max - r_min) ** 2

        r_peak = (r_max + r_min) / 2

        r = np.linspace(0, self.max_engine_rpm)
        t = np.zeros(len(r))

        t[r <= self.min_engine_rpm] = self.min_torque
        t[r > self.min_engine_rpm] = -a * (r[r > self.min_engine_rpm] - r_peak) ** 2 + t_max

        return r, t

    def plot_torques(self):
        r, t_e = self.engine_torque_curve()
        curves = {}

        for gear, ratio in self.gears.items():
            gear_ratio = ratio * self.final_drive_ratio
            curves[gear] = t_e * gear_ratio * self.drivetrain_efficiency

        plt.plot(r, t_e)
        plt.title(f"Engine torque curve of {self.name}")
        plt.ylabel(r"Engine torque $\tau$ [Nm]")
        plt.xlabel("Engine rpm")
        plt.show()

        for gear, t_w in curves.items():
            plt.plot(r, t_w, label=gear)

        plt.ylabel(r"Wheel torque $\tau$ [Nm]")
        plt.xlabel("Engine rpm")
        plt.title(f"Wheel torque curves of {self.name}")
        plt.legend(loc="upper left", title="Gear")
        plt.show()

        for gear, t_w in curves.items():
            v = (2 * pi * self.wheel_radius) * (
                    r[r > self.min_engine_rpm] / (self.gears[gear] * self.final_drive_ratio)) / 60
            plt.plot(v * 2.2369362920544025, t_w[r > self.min_engine_rpm], label=gear)

        plt.ylabel(r"Wheel torque $\tau$ [Nm]")
        plt.xlabel("Velocity $v$ [mph]")
        plt.title(f"Wheel torque curves of {self.name}")
        plt.legend(loc="upper right", title="Gear")
        plt.show()
