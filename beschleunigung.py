### NUMERISCHE SIMULATION ZUG ###

import math
import numpy as np
import matplotlib.pyplot as plt

plt.close('all')

# soft parameters
dt = 0.1  # [s]
v_0 = 0 / 3.6  # [m/s]
gradient = 0 / 1000  # [-]
wind = 0 / 3.6  # [m/s], >0: Gegenwind
engineThrottle = 100 / 100 # [%]
showPlot = 1
showLegend = 0
useHeightProfile = 0
topspeed = 250 / 3.6 # [m/s]

# hard parameters
muRail = 0.002 # 0.002  # [-]
muAxle = 0.  # [-]
muCatenary = 0.  # [-]
massTrain= 364000 # 742000.  # [kg]
g = 9.806  # [m/s^2]
forceNormal= massTrain *g  # [N]
forceNormalCatenary = 0.  # [N] # Oberleitung
powerEngine = 4800000 #8000000. #[W]
forceTraction = 200000 #300000. #[N] # Anfahrzugkraft
areaFront = 10.  # [m^2]
rohAir = 1.25  # [kg/m^3]
coefficientAero = 1.57 # 1.52  # [-]

if showPlot:
    plt.figure()
k = 1
sign = 0

# edit next line for multiple tests. Use "for x in [0]:" to do just one simulation with the given parameters
# for gradient in [0, -5/1000, -10/1000, -15/1000, -20/1000]:
# for gradient in [0, -1.48/1000, -1.49/1000, -1.5/1000]:
# for v_0 in [100/3.6, 200/3.6, 300/3.6, 400/3.6]:
# for wind in [-50/3.6, -25/3.6, 0, 25/3.6, 50/3.6]:
# for wind in [0, -10, -20, -30, -40, -50, -60, -70, -80]:
# for muRail in [0.001, 0.0015, 0.002]:
# for sign in [1, 0]:
# for massTrain in [670000, 742000]:
for x in [0]:
    
    # init loop
    a = 0.
    t = 0.
    s = 0.
    v = v_0
    a_arr = [0]
    v_arr = [v]
    t_arr = [t]
    s_arr = [s]

    while t < 10 * 3600 and v < topspeed: # 10h max
        # gravitational force
        if useHeightProfile:
            # gradient = -1.5/1000 * math.sin(1.5/1000 * s)
            if s < 10000:
                gradient = -1/1000 * sign
            elif s < 20000:
                gradient = -1/1000 * (1-sign)
            else:
                gradient = 0
        alpha = math.atan(gradient)
        forceGravitationInX = - math.sin(alpha) * massTrain * g

        # aerodynamic force
        forceAero = - 0.5 * rohAir * coefficientAero * areaFront  * (v + wind) * (v + wind)
        # tailwind > v: positive aero force
        if wind > v:
            forceAero = -forceAero

        # rolling force (tracks & axles)
        forceRollingRail = -(muRail + muAxle) * massTrain * g

        # rolling force (catenary)
        forceRollingCateneray = -muCatenary * forceNormalCatenary

        # engine force
        forceEngine = min(engineThrottle * powerEngine / max(v,0.1), forceTraction)

        # acceleration
        forceTotal = forceGravitationInX + forceAero + forceRollingRail + forceRollingCateneray + forceEngine
        a = forceTotal / massTrain

        if abs(a) < 1 / 100000 * dt:  # equilibrium
            break

        v += a * dt
        s += v * dt
        t += dt
        a_arr.append(a)
        v_arr.append(v)
        t_arr.append(t)
        s_arr.append(s)
        # print(v)
    # print(t,s,v,a)
    print('mu_R = ', muRail, ', C_D = ', coefficientAero)
    print('t= ',round(t,0),', s= ', round(s,0))

    if showPlot:
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