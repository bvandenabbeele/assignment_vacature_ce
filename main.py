"""Run this file to run the model and save the results"""
import plotly.express as px
import plotly.io as pio

from read_data import create_dataframe_from_input


if __name__ == "__main__":
    pio.renderers.default = "png"

    DATA_FILE = "data/1997.txt"
    data = create_dataframe_from_input(data_file=DATA_FILE)

    fig = px.line(
        data,
        x="date",
        y="temp",
        labels={"date": "Date", "temp": "Temperature (°C)"},
        title=f"Temperature recorded between {min(data['date']).strftime('%d %b %Y')} and {max(data['date']).strftime('%d %b %Y')} in De Bilt")
    fig.write_image("figures/temperature.png")
