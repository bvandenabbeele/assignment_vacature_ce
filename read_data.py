"""Functions for reading the data files"""
import numpy as np
import pandas as pd


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
