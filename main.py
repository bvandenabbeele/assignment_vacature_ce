"""Run this file to run the model and save the results"""
import plotly.express as px

from heat_model import \
    create_daily_temperature_setpoint, \
    calculate_heat_demand_simple, \
    calculate_heat_pump_power
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
    HEAT_PUMP_EFFICIENCY = .6
    HEAT_PUMP_T_COND = 35  # °C

    data = create_dataframe_from_input(data_file=DATA_FILE)
    data["t_set"] = create_daily_temperature_setpoint(THERMOSTAT, repeat=365).values
    data["Q"] = calculate_heat_demand_simple(u=U,a=A, t_set=data["t_set"], t_outside=data["temp"]).values
    data["heat_pump"] = calculate_heat_pump_power(HEAT_PUMP_EFFICIENCY, HEAT_PUMP_T_COND, data["temp"], data["Q"])

    print(data["heat_pump"][data["heat_pump"]>0].median())

    temp_fig = px.line(
        data,
        x="date",
        y="temp",
        labels={"date": "Date", "temp": "Temperature (°C)"},
        title=f"Temperature recorded between {min(data['date']).strftime('%d %b %Y')} and {max(data['date']).strftime('%d %b %Y')} in De Bilt"
    )
    temp_fig.write_image("figures/temperature.png")

    thermo_info = f"based on thermostat settings: {', '.join([f'{temp}°C from {time}:00' for time, temp in THERMOSTAT.items()])}"

    q_fig = px.line(
        data,
        x="date",
        y="Q",
        labels={"date": "Date", "Q": "Heat Demand (kWh/h)"},
        title=f"Heat demand {thermo_info}"
    )
    q_fig.write_image("figures/heat_demand.png")

    power_fig = px.line(
        data,
        x="date",
        y="heat_pump",
        labels={"date": "Date", "heat_pump": "Heat Pump Power (kW)"},
        title=f"Heat Pump Power {thermo_info}"
    )
    power_fig.write_image("figures/power.png")
