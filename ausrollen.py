### NUMERISCHE SIMULATION ZUG ###

import math
import numpy as np
import matplotlib.pyplot as plt


# soft parameters
dt = 0.1  # [s]
v_0 = 400 / 3.6  # [m/s]
gradient = 0 / 1000  # [-]
wind = 0 / 3.6  # [m/s], >0: Gegenwind
showLegend = 0
useHeightProfile = 0

# hard parameters
mu_s = 0.002  # [-]
mu_l = 0.  # [-]
mu_O = 0.  # [-]
m = 742000.  # [kg]
g = 9.806  # [m/s^2]
F_N = m*g  # [N]
F_NO = 0.  # [N]
A = 10.  # [m^2]
roh = 1.25  # [kg/m^3]
C_D = 1.52  # [-]

plt.figure()
k = 1
sign = 0

# edit next line for multiple tests. Use "for x in [0]:" to do just one simulation with the given parameters
# for gradient in [0, -5/1000, -10/1000, -15/1000, -20/1000]:
# for gradient in [0, -1.48/1000, -1.49/1000, -1.5/1000]:
# for v_0 in [100/3.6, 200/3.6, 300/3.6, 400/3.6]:
# for wind in [-50/3.6, -25/3.6, 0, 25/3.6, 50/3.6]:
# for wind in [0, -10, -20, -30, -40, -50, -60, -70, -80]:
# for mu_s in [0.001, 0.0015, 0.002]:
# for sign in [1, 0]:
for m in [670000, 742000]:
# for x in [0]:
    t = 0.
    s = 0.
    v = v_0
    v_arr = [v]
    t_arr = [t]
    s_arr = [s]
    while v > 0:
        if useHeightProfile:
            # gradient = -1.5/1000 * math.sin(1.5/1000 * s)
            if s < 10000:
                gradient = -1/1000 * sign
            elif s < 20000:
                gradient = -1/1000 * (1-sign)
            else:
                gradient = 0
        # calculations
        alpha = math.atan(gradient)
        F_Gx = math.sin(alpha) * m * g

        C_1 = roh * C_D * A / (2 * m)
        C_2 = (F_N * (mu_s + mu_l) + F_NO * mu_O + F_Gx) / m
        if v+wind > 0:
            a = C_2 + C_1 * (v + wind) * (v + wind)
        else:
            a = C_2 - C_1 * (v + wind) * (v + wind)
        if abs(a) < 1 / 100000 * dt:  # equilibrium
            break
        v -= a * dt
        s += v * dt
        t += dt
        v_arr.append(v)
        t_arr.append(t)
        s_arr.append(s)
        # print(v)
    print(s, v, a)

    v_arr = np.array(v_arr)
    # t_arr = np.array(t_arr)
    # s_arr = np.array(s_arr)
    plt.subplot(223)
    plt.plot(s_arr, v_arr*3.6)
    plt.xlabel('s [m]')
    plt.ylabel('v [m/s]')
    plt.subplot(222)
    plt.plot(t_arr, s_arr)
    plt.xlabel('t [s]')
    plt.ylabel('s [m]')
    plt.subplot(224)
    plt.plot(t_arr, v_arr*3.6)
    plt.xlabel('t [s]')
    plt.ylabel('v [m/s]')

    # legend
    if showLegend:
        plt.subplot(221)
        plt.plot([k, k])
    k += 1
plt.show()