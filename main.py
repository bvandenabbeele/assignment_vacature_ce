"""Run this file to run the model and save the results"""

from heat_model import create_daily_temperature_setpoint, calculate_heat_demand_simple
from plots import create_temp_fig, create_q_fig
from read_data import create_dataframe_from_input


if __name__ == "__main__":
    DATA_FILE = "data/1997.txt"
    U = 1  # W/m²K; average heat transfer coefficient
    A = 400  # m²; surface area

    THERMOSTAT = {
    # H: T (°C)
        7: 19,
        21: 16
    }

    data = create_dataframe_from_input(data_file=DATA_FILE)
    data["t_set"] = create_daily_temperature_setpoint(THERMOSTAT, repeat=365).values
    data["Q"] = calculate_heat_demand_simple(u=U,a=A, t_set=data["t_set"], t_outside=data["temp"]).values

    create_temp_fig(data).write_image("figures/temperature.png")
    create_q_fig(data, THERMOSTAT).write_image("figures/heat_demand.png")
