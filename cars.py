import random
import numpy as np
import matplotlib.pyplot as plt

# setting up time parameter
t = list(range(0,5))
t = list(np.float_(t))

# setting the cars speed
u1 = 30 
#trajectory of the car with no detection of preceding car
s1 = []
for i in t:
    s = u1 * i 
    s1.append(s)

# setting the speed of the car in front
u2 = random.randint(22, 45) 

# trajectory of car in front at constant speed
s2 = []
for i in t:
    s = 160 + u2 * i 
    s2.append(s)
def square(x):
    return x * x

# finding the time taken for deceleration and the value of deceleration required
def find_time(u1,u2):
    delta_s = 2*u2
    quad = [(square(u1) - 5*square(u2) + 4*u1*u2), (4*u2*delta_s-8*u1*u2+8*square(u2)), (-delta_s*8*u2)]
    time = np.roots(quad)
    time = time[1]
    accel = (u2 - u1)/time
    return time, accel

a = find_time(u1,u2)[1]

time = find_time(u1,u2)[0] 
print (time)

# trajecrtory of decelerating car and subsequent motion
s_1 = []
for i in t:
    if i <= time :
        s = u1 * i + 0.5 * a * square(i)
    else: 
        s = u2 * i
    s_1.append(s)
print (s_1)

# plot to show results
plt.plot(t,s2, 'r', label='Detected Car')
plt.plot(t,s_1, 'g', label='Audi S4 Saloon')
plt.title("Deceleration Curve Maintaining Safe Time Gap Between Vehicles")
plt.xlabel("time (s)")
plt.ylabel("distance (m)")
plt.legend()
plt.show()


