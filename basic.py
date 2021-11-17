import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from math import cos, sin

        

#function returning dy/dx
def model(v, t):
    mass = 1611
    height = 1.443
    width = 1.849
    length = 4.694
    Cd = 0.23
    power = 211000
    torque = 450
    top_speed = 62.5856
    wheel_width = 0.216
    wheel_radius = 0.2285

    mu = 0.25
    g = -9.81
    air_density = 1
    angle = 0.2

    def acc_force():
        t = torque
        r = wheel_radius
        a = angle
        return t / (r * sin(a))

    def friction():
        m = mass
        a = angle
        return mu * m * g * cos(a)

    def weight():
        m = mass
        a = angle
        return m * g * sin(a)

    def drag(v):
        h = height
        w = width
        ad = air_density
        return 0.5 * Cd * h * w * ad * v ** 2

    
    dvdt = (acc_force() - friction() - weight() - drag(v)) / mass
    return dvdt


t = np.linspace(0, 100, 200)

v0 = 0

v = odeint(model, v0, t)

plt.plot(t, v)
plt.show()


















 
