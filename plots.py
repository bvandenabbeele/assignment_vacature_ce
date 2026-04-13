"""Functions to create figures"""
import pandas as pd
import plotly as pl
import plotly.express as px


def create_temp_fig(data: pd.DataFrame):
    """_summary_
    """
    fig = px.line(
        data,
        x="date",
        y="temp",
        labels={"date": "Date", "temp": "Temperature (°C)"},
        title=f"Temperature recorded between {min(data['date']).strftime('%d %b %Y')} and {max(data['date']).strftime('%d %b %Y')} in De Bilt")

    return fig

def create_q_fig(data: pd.DataFrame, settemps: dict[int, int|float]):
    """_summary_
    """
    fig = px.line(
        data,
        x="date",
        y="Q",
        labels={"date": "Date", "Q": "Heat Demand (kWh/h)"},
        title=f"Heat demand based on thermostat settings: {", ".join([f'{temp}°C from {time}:00' for time, temp in settemps.items()])}"
    )

    return fig
