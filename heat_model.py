"""$Q = U  A  (T_{setpoint} - T_{outside}) / 1000$

    - $U$: De gemiddelde warmteoverdrachtcoëfficiënt $(W/ m^2K )$. Schat een realistisch getal in op basis van literatuur.
    - $A$: Totale schiloppervlak ($m^2$) van de woning (ramen, muren, dak etc). Neem voor het gemak een oppervlak van 400 $m^2$.
    - $T_{setpoint}$: Streeftemperatuur in de woning (bijv. 20°C). **Bonus: variëer de set-point temperatuur voor dag en nacht.**
    - $T_{outside}$: Buitentemperatuur per uur (°C)
"""
import numpy as np
import pandas as pd


def create_daily_temperature_setpoint(settimes: dict[int, int|float], repeat: int) -> pd.Series:
    """Create a temperature setpoint series for a single day in hours and repeat it for the desired number of days.

    :param settimes: dict of {time: temp} value pairs. Times will be converted to integers.
    :param repeat: how many times the single day setpoints should be repeated to create the full length series.
    :return: pandas Series of temperature setpoints.
    """
    # create empty series
    t_set = pd.Series(data=24*[0], name="t_set", dtype=np.float64)

    # created sorted list of times and matching temperature list
    times = sorted([int(t) for t in settimes.keys()])
    temps = [settimes[t] for t in times]

    # populate series with temperatures
    for i, time in enumerate(times):
        end_slice = times[i+1] if i+1 < len(times) else len(t_set)
        t_set[time:end_slice] = temps[i]

    # add temperatures to the front if we need to loop around
    if times[0] != 0:
        t_set[:times[0]] = temps[-1]

    return t_set.iloc[pd.RangeIndex(repeat*24)%24]


def calculate_heat_demand_simple(u: float, a: float, t_set: float | pd.Series, t_outside: float | pd.Series) -> pd.Series:
    """_summary_

    :param u: _description_
    :param a: _description_
    :param t_set: _description_
    :param t_outside: _description_
    :return:
    """

    q_raw = u * a * (t_set - t_outside) / 1000
    q = q_raw.clip(lower=0)
    q_stored = (-q_raw.clip(upper=0)).cumsum()

    for i in range(len(q)):
        if q[i] > 0 and q_stored[i] > 0:
            q_used = min(q[i], q_stored[i])
            q[i] -= q_used
            q_stored[i::] -= q_used

    return q


def calculate_heat_pump_power(efficiency: float, t_condensation: int | float, t_outside: pd.Series, heat_demand: pd.Series) -> pd.Series:
    """_summary_

    :param efficiency: _description_
    :param t_condensation: _description_
    :param t_outside: _description_
    :param heat_demand: _description_
    :return: _description_
    """
    cop = efficiency * t_condensation / (t_condensation - t_outside)
    return heat_demand / cop


if __name__ == "__main__":
    from read_data import create_dataframe_from_input
    calculate_heat_demand_simple(
        1,
        400,
        19.,
        create_dataframe_from_input("data/1997.txt")["temp"]
    )
