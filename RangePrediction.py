import numpy as np
import scipy as sp
from matplotlib import pyplot as plt
import os

# Clear Terminal
os.system("cls")  # Clearing the terminal for better visibility


# -----------INPUTS-----------------
lift_drag_ratios = np.array([4, 5, 6, 7, 8])  # Lift/Drag
cruise_mach_numbers = np.linspace(2, 7, 10)  # Cruse Mach number
total_ranges = [3500, 4000, 4500, 5000, 5500]  # Total range in nmi
earth_radius = 20925641.8  # Radius of the earth in ft
gravity_acceleration = 32.174  # Acceleration due to gravity in ft/s^2
takeoff_acceleration = 0.3 * gravity_acceleration  # Take off Acceleration in ft/s^2

# -----------Output Arrays-----------------
climb_distance_arrays = [None] * len(lift_drag_ratios)
percentage_cruise_arrays = [None] * len(lift_drag_ratios)
total_time_arrays = [None] * len(lift_drag_ratios)
climb_distance_arrays_arrays = []
percentage_cruise_arrays_arrays = []
total_time_arrays_arrays = []


# ----------------------TAKE OFF/THROTTLE UP---------------------------------------
def take_off_throttle_up(V_c, a_t):
    """Use kinematic equations to determine time and distance to cruise velocity"""

    t_T = V_c / a_t  # time to cruse in seconds
    s_T = 0.5 * a_t * t_T**2  # cruise distance covered in ft

    return t_T, s_T


# ----------------------Landing and Glide------------------------------------------
def landing_glide(V_c, g, LoD, re):
    """Using equations on slide 3 provided by Dr. Bowcutt to determine time and distance to land"""
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
    """Calculate the distance and time at cruise"""

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
            PerCruise_Vals = np.zeros((len(MachNum)))
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
                PerCruise = s_C / TotRan_i * 100
                PerCruise_Vals[j] = PerCruise
            climb_distance_arrays[i] = s_L_Vals
            percentage_cruise_arrays[i] = PerCruise_Vals
            total_time_arrays[i] = TotalTime_Vals
        climb_distance_arrays_arrays.append(climb_distance_arrays.copy())
        percentage_cruise_arrays_arrays.append(percentage_cruise_arrays.copy())
        total_time_arrays_arrays.append(total_time_arrays.copy())


run_calculations(
    lift_drag_ratios,
    cruise_mach_numbers,
    total_ranges,
    earth_radius,
    gravity_acceleration,
    takeoff_acceleration,
)


def plot_graphs(x_vals, y_vals, xlabel, ylabel, title, legend_labels):
    """Plotting code"""
    plt.figure()
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    for i in range(len(lift_drag_ratios)):
        plt.plot(x_vals, y_vals[i], label=f"L/D {lift_drag_ratios[i]}")
    plt.legend()


# Generate s_L vs Mach plot
plot_graphs(
    cruise_mach_numbers,
    climb_distance_arrays_arrays[0],
    "Mach",
    "$s_L$",
    "$s_L$ vs Mach",
    legend_labels=None,
)

# Generate s_C/Range vs Mach plots
for r in range(len(total_ranges)):
    title = f"$\\frac{{s_C}}{{\\text{{Range}}}}$ vs Mach: Range {total_ranges[r]} nmi"
    plot_graphs(
        cruise_mach_numbers,
        percentage_cruise_arrays_arrays[r],
        "Mach",
        title,
        title,
        legend_labels=lift_drag_ratios,
    )


# Generate Total time vs Mach plots
for r in range(len(total_ranges)):
    plot_graphs(
        cruise_mach_numbers,
        total_time_arrays_arrays[r],
        "Mach",
        "Total Time [min]",
        f"Total Time [min] vs Mach: Range {total_ranges[r]}",
        legend_labels=lift_drag_ratios,
    )

plt.show()
