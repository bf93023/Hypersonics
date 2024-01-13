import numpy as np
import scipy as sp
from matplotlib import pyplot as plt
import os

# Clear Terminal
os.system("cls")  # Clearing the terminal for better visibility


# -----------INPUTS-----------------
LoD = np.array([4, 5, 6, 7, 8])  # Lift/Drag
MachNum = np.linspace(2, 7, 10)  # Cruse Mach number
TotRan = [3500, 4000, 4500, 5000, 5500]  # Total range in nmi
re = 20925641.8  # Radius of the earth in ft
g = 32.174  # Acceleration due to gravity in ft/s^2
a_t = 0.3 * g  # Take off Acceleration in ft/s^2
s_L_Arrays = [None] * len(LoD)
PerCruse_Arrays = [None] * len(LoD)
TotalTime_Arrays = [None] * len(LoD)
s_L_Arrays_Arrays = []
PerCruse_Arrays_Arrays = []
TotalTime_Arrays_Arrays = []


# ----------------------TAKE OFF/THROTTLE UP---------------------------------------
def take_off_throttle_up(V_c, a_t):
    """Use kinimatic equations to determine time and distance to cruse velocity"""

    t_T = V_c / a_t  # time to cruse in seconds
    s_T = 0.5 * a_t * t_T**2  # cruise distance covered in ft

    return t_T, s_T


# ----------------------Landing and Glide------------------------------------------
def landing_glide(V_c, g, LoD, re):
    """Using equations on slide 3 provided by Dr. Bockut to determine time and distance to land"""
    A = g / LoD
    B = g * re
    C = (1 + V_c / np.sqrt(B)) / (1 - V_c / np.sqrt(B))
    D = 1
    E = (2 * A) / np.sqrt(B)

    t_L = (1 / E) * (np.log(C) - np.log(D))

    s_L = (
        -np.sqrt(B) * t_L
        - (B / A) * np.log(1 + C * np.exp(-E * t_L))
        + (B / A) * np.log(1 + C)
    )

    return t_L, s_L


# ----------------------CRUSE----------------------------------------------------
def cruise(TotRan, s_T, s_L, V_c):
    """calculate the distance and time at cruse"""

    s_C = TotRan - s_T - s_L
    t_C = s_C / V_c

    return t_C, s_C


# ------------------------RUN CALCULATIONS------------------------------------------
def run_calculations(LoD, MachNum, TotRan, re, g, a_t):
    for k in range(len(TotRan)):
        TotRan_i = TotRan[k] * 6076.12  # converts nmi to ft
        # print("-------------- Range:", TotRan[k], "nmi --------------")
        for i in range(len(LoD)):
            LoD_i = LoD[i]
            # print("\n\nL/D:", LoD_i)
            PerCruse_Vals = np.zeros((len(MachNum)))
            s_L_Vals = np.zeros(len(MachNum))
            TotalTime_Vals = np.zeros((len(MachNum)))
            for j in range(len(MachNum)):
                # print("Mach Number:", MachNum[j])
                V_c = MachNum[j] * 1125.328084  # converts mach number to ft/s
                t_T, s_T = take_off_throttle_up(V_c, a_t)
                t_L, s_L = landing_glide(
                    V_c, g, LoD_i, re
                )  # calculate time spent in climb and distance covered in climb
                s_L_Vals[j] = s_L
                t_C, s_C = cruise(TotRan_i, s_T, s_L, V_c)
                t_total = (t_T + t_L + t_C) / 60
                TotalTime_Vals[j] = t_total
                PerCruse = s_C / TotRan_i * 100
                PerCruse_Vals[j] = PerCruse
            s_L_Arrays[i] = s_L_Vals
            PerCruse_Arrays[i] = PerCruse_Vals
            TotalTime_Arrays[i] = TotalTime_Vals
        s_L_Arrays_Arrays.append(s_L_Arrays.copy())
        PerCruse_Arrays_Arrays.append(PerCruse_Arrays.copy())
        TotalTime_Arrays_Arrays.append(TotalTime_Arrays.copy())


run_calculations(LoD, MachNum, TotRan, re, g, a_t)


def plot_graphs(x_vals, y_vals, xlabel, ylabel, title, legend_labels):
    """Plotting code"""
    plt.figure()
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    for i in range(len(LoD)):
        plt.plot(x_vals, y_vals[i], label=f"L/D {LoD[i]}")
    plt.legend()


# Generate s_L vs Mach plot
plot_graphs(MachNum, s_L_Arrays, "Mach", "$s_L$", "$s_L$ vs Mach", legend_labels=None)

# Generate s_C/Range vs Mach plots
for r in range(len(TotRan)):
    title = f"$\\frac{{s_C}}{{\\text{{Range}}}}$ vs Mach: Range {TotRan[r]} nmi"
    plot_graphs(
        MachNum, PerCruse_Arrays_Arrays[r], "Mach", title, title, legend_labels=LoD
    )


# Generate Total time vs Mach plots
for r in range(len(TotRan)):
    plot_graphs(
        MachNum,
        TotalTime_Arrays_Arrays[r],
        "Mach",
        "Total Time [min]",
        f"Total Time [min] vs Mach: Range {TotRan[r]}",
        legend_labels=LoD,
    )

plt.show()
