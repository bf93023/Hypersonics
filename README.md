# Aircraft Performance Analysis Readme

This Python script is designed to perform an analysis of aircraft performance based on various input parameters. The analysis includes calculations for take-off, climb, cruise, landing, and glide phases. The results are then visualized through plots showcasing climb distance, percentage of cruise distance, and total time across different lift/drag ratios and cruise Mach numbers.

## Table of Contents

- [Requirements](#requirements)
- [Inputs](#inputs)
- [Functions](#functions)
  - [take_off_throttle_up](#take_off_throttle_up)
  - [landing_glide](#landing_glide)
  - [cruise](#cruise)
  - [run_calculations](#run_calculations)
  - [plot_graphs](#plot_graphs)
- [Usage](#usage)
- [Output](#output)
- [License](#license)

## Requirements

Ensure you have the following Python libraries installed:

- NumPy
- SciPy
- Matplotlib

## Inputs

The script takes the following inputs:

- `lift_drag_ratios`: Array of lift-to-drag ratios.
- `cruise_mach_numbers`: Array of cruise Mach numbers.
- `total_ranges`: Array of total ranges in nautical miles.
- `earth_radius`: Radius of the Earth in feet.
- `gravity_acceleration`: Acceleration due to gravity in feet per second squared.
- `takeoff_acceleration`: Takeoff acceleration in feet per second squared.

## Functions

### `take_off_throttle_up(V_c, a_t)`

Uses kinematic equations to determine time and distance to cruise velocity.

### `landing_glide(V_c, g, LoD, re)`

Utilizes equations to determine time and distance to land based on provided parameters.

### `cruise(TotRan, s_T, s_L, V_c)`

Calculates the distance and time during the cruise phase.

### `run_calculations(LoD, MachNum, TotRan, re, g, a_t)`

Runs the main calculations for different lift-to-drag ratios, cruise Mach numbers, and total ranges.

### `plot_graphs(x_vals, y_vals, xlabel, ylabel, title, legend_labels)`

Generates plots for visualization, including climb distance vs. Mach, cruise distance vs. Mach for different ranges, and total time vs. Mach for different ranges.

## Usage

1. Ensure the required libraries are installed.
2. Set the desired input parameters.
3. Run the script.

## Output

The script generates visualizations of climb distance, percentage of cruise distance, and total time for different lift-to-drag ratios, cruise Mach numbers, and total ranges.
