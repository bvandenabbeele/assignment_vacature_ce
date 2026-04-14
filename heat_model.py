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
    """Calculate the head demand of a home.

    The following equation is used to calculate heat demand
    $Q = U  A  (T_{setpoint} - T_{outside}) / 1000$

        - $U$: De gemiddelde warmteoverdrachtcoëfficiënt $(W/ m^2K )$. Schat een realistisch getal in op basis van literatuur.
        - $A$: Totale schiloppervlak ($m^2$) van de woning (ramen, muren, dak etc). Neem voor het gemak een oppervlak van 400 $m^2$.
        - $T_{setpoint}$: Streeftemperatuur in de woning (bijv. 20°C). **Bonus: variëer de set-point temperatuur voor dag en nacht.**
        - $T_{outside}$: Buitentemperatuur per uur (°C)

    The negative heat demand from the equation above is regarded as stored heat and used as a buffer to offset subsequent positive head demand. \
        This ensures that there is no heat demand e.g. during the after a hot Summer day until the house has fully cooled down.

    :param u: heat transfer coefficient.
    :param a: surface area.
    :param t_set: temperature setpoint inside.
    :param t_outside: outside temperature.
    :return: pandas series of the heat demand for the heat pump
    """

    q_raw = u * a * (t_set - t_outside) / 1000
    # keep only positive heat demand
    q = q_raw.clip(lower=0)
    # use negative heat demand to build a buffer of stored heat
    q_stored = (-q_raw.clip(upper=0)).cumsum()

    # loop over the heat demand. whenever we have a positive heat demand and some heat in our buffer, \
    # we use that heat to lower the heat demand for the heat pump. The used heat is taken out of the buffer.
    for i in range(len(q)):
        if q[i] > 0 and q_stored[i] > 0:
            q_used = min(q[i], q_stored[i])
            q[i] -= q_used
            q_stored[i::] -= q_used

    return q


def calculate_heat_pump_power(efficiency: float, t_condensation: int | float, t_outside: pd.Series, heat_demand: pd.Series) -> pd.Series:
    """Calculate heat pump power draw.

    For COP we use COP = efficiency * t_cond / (t_cond - t_outside)

    :param efficiency: heat pump efficiency
    :param t_condensation: heat pump condensation temperature
    :param t_outside: outside temperature
    :param heat_demand: heat generation demanded of the heat pump
    :return: pandas series of the power draw of the heat pump
    """
    cop = efficiency * t_condensation / (t_condensation - t_outside)
    return heat_demand / cop
