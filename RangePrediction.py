import numpy as np 
import scipy as sp 
from matplotlib import pyplot as plt 


# -----------INPUTS-----------------
LoD = np.array([4,5,6,7,8])               #Lift/Drag
MachNum = np.linspace(2,7,10)           #Cruse Mach number
TotRan = [3500, 4000, 4500, 5000, 5500] #Total range in nmi
re = 20925641.8                         #Radius of the earth in ft
g = 32.174                              #Acceleration due to gravity in ft/s^2
a_t = 0.3                               #Take off Acceleration in g's
a_t = 0.3*g                             #Take off Acceleration in ft/s^2 


#----------------------TAKE OFF/THROTTLE UP---------------------------------------
def takeOffThrotUp(V_c, a_t):
    """Use kinimatic equations to determine time and distance to cruse velocity"""

    t_T = V_c/a_t           #time to cruse in seconds
    s_T = 0.5*a_t*t_T**2    #distance covered in ft

    return t_T, s_T

#----------------------Landing and Glide------------------------------------------
def landingGlide(V_c, g, LoD, re):
    """Using equations on slide 3 provided by Dr. Bockut to determine time and distance to land"""
    A = g/LoD
    B = g*re
    C = (1+V_c/np.sqrt(B))/(1-V_c/np.sqrt(B))
    D = 1
    E = (2*A)/np.sqrt(B)

    t_L = (1/E)*(np.log(C)-np.log(D))

    s_L = -np.sqrt(B)*t_L-(B/A)*np.log(1+C*np.exp(-E*t_L))+(B/A)*np.log(1+C)

    return t_L, s_L

#----------------------CRUSE----------------------------------------------------
def cruse(TotRan, s_T, s_L, V_c):
    """calculate the distance and time at cruse"""

    s_C = TotRan-s_T-s_L
    t_C = s_C/V_c

    return t_C, s_C
    
#------------------------RUN CALCULATIONS------------------------------------------
def run(LoD, MachNum, TotRan, re, g, a_t):
    for k in range(len(TotRan)):
        TotRan_i = TotRan[k] * 6076.12  # converts nmi to ft
        print("-------------- Range:", TotRan[k], "nmi --------------")
        for i in range(len(LoD)):
            LoD_i = LoD[i]
            print("L/D:", LoD_i)
            for j in range(len(MachNum)):
                print("Mach Number:", MachNum[j])
                V_c = MachNum[j] * 1125.328084  # converts mach number to ft/s
                t_T, s_T = takeOffThrotUp(V_c, a_t)
                t_L, s_L = landingGlide(V_c, g, LoD_i, re)
                t_C, s_C = cruse(TotRan_i, s_T, s_L, V_c)
                t_total = (t_T + t_L + t_C) / 60
                PerCruse = s_C / TotRan_i * 100
                print("time in minutes:")
                print(t_total)
                print("percent at cruse:")
                print(PerCruse)

run(LoD, MachNum, TotRan, re, g, a_t)
