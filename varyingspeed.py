import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from math import cos, sin, pi
#import control as ct
from cruise.classes import Car, TorquePlotting

def PID_speeds():
    car = Car(1611, [1.443, 1.849, 4.694], 0.23, 211000, 450, 62.5856, [0.216, 0.2285])
    # solving the ODE to find velocity
    t_max = 600
    N = 600
    t = np.linspace(0, t_max, N)

    
    tauI = 20
    tauD = .17
        
    # PID controller
    Kp = .1        # proportional gain
    Ki = 0.7                   # integral gain
    Kd = 1.5       # derivative gain
    P = np.zeros(N)          # initialize proportional term
    I = np.zeros(N)          # initialize integral term
    D = np.zeros(N)          # initialize derivative term
    e = np.zeros(N)          # initialize error
    PID_output = np.zeros(N)         # initialize controller output
    current_v = np.zeros(N)  # initialize process variable
    req_v = np.zeros(N)         # initialize required velocity
    req_vlim = np.zeros(N)    # initialise target velocity limits (to allow for signal latency)
    t_acc = 15                   # time lag for acceleration
    t_brake = 25               # time lag for braking
    lag_slow = 1.5               # typical lag for slowing down (to define target velocity limits)
    lag_speed = 0.5              # typical lag for speeding down (to define target velocity limits)
    speed_lim = [5,25,31,18,0,15,20] # speed limit changes over course of time t
    change_t = [0,50,100,200,350,500,600] # times when speed limit changes
    for i in range(1, len(speed_lim)):
        # defining target velocity limits (less than speed limit to allow for kickback)
        req_v[change_t[i-1]:change_t[i]] = speed_lim[i-1]
        req_vlim[change_t[i-1]:change_t[i]] = speed_lim[i-1]
        if speed_lim[i-1] > speed_lim[i]:
            req_vlim[change_t[i-1]:change_t[i]] = speed_lim[i-1]-lag_speed
        # else:
        #     req_vlim[change_t[i-1]:int(change_t[i-1]+1.5*t_brake)] = speed_lim[i-1]-lag_slow
        #     req_vlim[int(change_t[i-1]+1.5*t_brake):change_t[i]] = speed_lim[i-1]-lag_slow
        req_vlim[0:change_t[1]] = speed_lim[0]-2*lag_slow
        
        
    for i in range(1,N): # 1 to N are each second
    
        # changing incline angle over time
        if i >= N/4:
            car.angle += .1*car.angle
        elif i >= N/3:
            car.angle = car.angle
        elif i >= 0:
            car.angle = 0*car.angle
            
            
            
        # simulate process for one time step
        ts = [t[i-1],t[i]]       # time interval
        
        car.v_req = req_vlim[i] # define required speed in class Car
        car.input = PID_output[i-1]  # define error in class Car
        v = odeint(car.acceleration, current_v[i-1],ts) # find velocity 
        
        
        v_lag = req_vlim[i] # defining general velocity lag
        
        for n in range(0,len(change_t)-1):
            if speed_lim[n+1] < speed_lim[n]:
                if change_t[n]+t_brake <= t[i] <= change_t[n+1]:
                    if change_t[n+1] - t[i] <= t_brake and i + t_brake < t_max:
                        v_lag = req_vlim[i+t_brake] # adding braking time to velocity lag
            elif speed_lim[n+1] > speed_lim[n]:
                if change_t[n+1]+t_acc >= t[i] >= change_t[n]:
                    if change_t[n+1] - t[i] <= t_acc  and i + t_acc < t_max:
                        v_lag = req_vlim[i-t_acc] # subtracting accelerating time to velocity lag
                        
        
        current_v[i] = v[1]             # record current velocity
        e[i] = v_lag - current_v[i]     # calculate error = required velocity (to the limit) - current velocity
        dt = t[i] - t[i-1]              # calculate time step
        # defining PID output
        if car.v_req == req_vlim[0]:    # defining seperate coefficients for starting at v = 0
            tau_I,tau_D = 10, .1 
            K_p, K_i, K_d = .56 , 1, 1.6   
            P[i] = K_p * e[i]           # proportional term
            I[i] = I[i-1] + (K_i/tau_I) * e[i] * dt  #  integral term
           # D[i] = -K_d * tau_D * abs((current_v[i]-current_v[i-1]))/dt # derivative term
            D[i] = -K_d * tau_D * (current_v[i-1])/dt # derivative term, avoid derivative kick
        else:
           
            P[i] = Kp * e[i]           # proportional term
            I[i] = I[i-1] + (Ki/tauI) * e[i] * dt  # integral term
           # D[i] = -Kd * tauD * abs((current_v[i]-current_v[i-1]))/dt # derivative term
            D[i] = -Kd * tauD * current_v[i-1]/dt # derivative term, avoid derivative kick
        
        PID_output[i] = P[i] + I[i] + D[i] # calculate new controller output
        
    # plot PID response
    plt.figure(1,figsize=(15,7))
    plt.plot(t,req_v,'k-',linewidth=2,label='Required Velocity')
    plt.plot(t,current_v,'b',linewidth=2,label='Output Velocity $v$')
   # plt.plot(t,req_vlim,'r:',linewidth=2,label='Velocity Constraints')
    plt.xlabel('Time $t$ [s]', fontsize=20, fontweight='bold')
    plt.ylabel('Velocity $v$ [m/s]',fontsize=20, fontweight='bold')
    plt.legend(loc='best')
    plt.rcParams.update({'font.size': 22})
    plt.show()
    
PID_speeds()