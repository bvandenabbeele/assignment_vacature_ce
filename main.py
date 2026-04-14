"""Run this file to run the model and save the results"""

from heat_model import create_daily_temperature_setpoint, calculate_heat_demand_simple
from plots import create_temp_fig, create_q_fig
from read_data import create_dataframe_from_input


if __name__ == "__main__":
    DATA_FILE = "data/1997.txt"
    A = 400  # m²; surface area
    # I'm assuming a cubic house with one shared wall, for 80m² a side. Windows/doors take up 25% of wall area.
    # U-values are taken from https://publications.jrc.ec.europa.eu/repository/bitstream/JRC117739/cost_optimal_energy_renovations_online.pdf
    # as the averages of U-values listed in Figure 2 for the Netherlands
    U = (80*1.1 + .75*160*1.45 + .25*160*1.3 + 80*2.25)/A  # W/m²K; average heat transfer coefficient

    THERMOSTAT = {
    # time: temp (°C)
        7: 19,
        21: 16
    }

    data = create_dataframe_from_input(data_file=DATA_FILE)
    data["t_set"] = create_daily_temperature_setpoint(THERMOSTAT, repeat=365).values
    data["Q"] = calculate_heat_demand_simple(u=U,a=A, t_set=data["t_set"], t_outside=data["temp"]).values

    create_temp_fig(data).write_image("figures/temperature.png")
    create_q_fig(data, THERMOSTAT).write_image("figures/heat_demand.png")
