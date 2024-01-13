# Aircraft Range and Performance Calculator

This Python program calculates the take-off, cruise, and landing performance of an aircraft based on user-defined parameters. It provides insights into the distance covered, time taken, and other performance metrics.

## Dependencies

Make sure you have the following dependencies installed:

- `numpy`
- `scipy`
- `matplotlib`

## How to Use

1. Open the `aircraft_performance_calculator.py` file.
2. Set the input parameters in the code under the `# -----------INPUTS-----------------` section.
3. Run the script.

The program will generate plots illustrating the aircraft's climb, cruise, and overall performance based on different lift/drag ratios and cruise Mach numbers.

## Input Parameters

- `LoD`: Array of Lift/Drag ratios.
- `MachNum`: Array of cruise Mach numbers.
- `TotRan`: Array of total ranges in nautical miles.
- `re`: Radius of the Earth in feet.
- `g`: Acceleration due to gravity in ft/s^2.
- `a_t`: Takeoff acceleration in ft/s^2.

## Functions

### `take_off_throttle_up(V_c, a_t)`

Calculates time and distance to reach cruise velocity during takeoff.

### `landing_glide(V_c, g, LoD, re)`

Determines time and distance for landing based on glide equations.

### `cruise(TotRan, s_T, s_L, V_c)`

Calculates distance and time during cruise phase.

### `run_calculations(LoD, MachNum, TotRan, re, g, a_t)`

Runs the main calculations for various lift/drag ratios and cruise Mach numbers.

### `plot_graphs(x_vals, y_vals, xlabel, ylabel, title, legend_labels)`

Generates and displays plots for visualizing the results.

## Plots

The program generates three types of plots:

1. **$s_L$ vs Mach**: Illustrates climb performance with respect to Mach number.

2. **$\frac{s_C}{\text{Range}}$ vs Mach**: Shows the percentage of cruise distance with respect to total range.

3. **Total Time vs Mach**: Displays the total time taken for the aircraft to complete the journey.
