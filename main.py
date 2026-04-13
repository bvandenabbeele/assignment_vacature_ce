import numpy as np
import pandas as pd
import plotly.express as px
import plotly.io as pio

from datetime import timedelta, datetime


def create_dataframe_from_input(data_file: str) -> pd.DataFrame:
    """Create a pandas.DataFrame from input csv file.
    The output DataFrame has two columns:

        - date: timestamp of the measurement (datetime)
        - temp: measured temperature in degrees Celsius

    :param data_file: path to csv file
    :return: pandas.DataFrame
    """
    df = pd.read_csv(
        data_file, 
        comment="#",
        usecols=(1, 2, 3), 
        names=("date", "time", "temp"),
        parse_dates=["date"],
        date_format="%Y%m%d",
        converters={"temp": lambda x: int(x)/10},
        dtype={"time": np.int8}
    )

    df["date"] = pd.to_timedelta(df["time"] - 1, unit="h") + df["date"]
    df.drop(columns="time", inplace=True)

    return df


if __name__ == "__main__":
    pio.renderers.default = "png"
    
    data_file = "data/1997.txt"
    data = create_dataframe_from_input(data_file=data_file)

    fig = px.line(
        data, 
        x="date", 
        y="temp", 
        labels=dict(date="Date", temp="Temperature (°C)"), 
        title=f"Temperature recorded between {min(data['date']).strftime('%d %b %Y')} and {max(data['date']).strftime('%d %b %Y')} in De Bilt")
    fig.write_image("figures/temperature.png")