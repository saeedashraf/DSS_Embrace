import numpy as np
import pandas as pd
import plotly.graph_objects as go
from global_params_and_utils import DATA_DIRECTORY, plotly_as_python_dict


def _plot_historical_data():
    df_from_csv_dfq50_years_obs = pd.read_csv(DATA_DIRECTORY / "dfq50_years_obs.csv")
    arr_from_sql_dfq50_years_obs = df_from_csv_dfq50_years_obs["q50_years_obs"].values

    df_from_csv_dfq75_years_obs = pd.read_csv(DATA_DIRECTORY / "dfq75_years_obs.csv")
    arr_from_sql_dfq75_years_obs = df_from_csv_dfq75_years_obs["q75_years_obs"].values

    df_from_csv_dfq90_years_obs = pd.read_csv(DATA_DIRECTORY / "dfq90_years_obs.csv")
    arr_from_sql_dfq90_years_obs = df_from_csv_dfq90_years_obs["q90_years_obs"].values

    df_from_csv = pd.read_csv(DATA_DIRECTORY / "array_data_matrix_HotDays_obs.csv")
    arr_from_sql_matrix_HotDays_obs = df_from_csv.values.reshape((80, 41, 2))

    # TODO: hardcoded - it should come from the the previous arr
    x_axis_obs = np.arange(1981, 2020 + 1)

    p_Step = 1
    alpha_Fade_obs = 1

    fig = go.Figure()

    for i in range(0, len(arr_from_sql_matrix_HotDays_obs), p_Step):
        a = arr_from_sql_matrix_HotDays_obs[i, 1:, 1:2].astype(float)
        if i == 0:
            fig.add_trace(
                go.Scatter(
                    x=x_axis_obs,
                    y=a[:, 0],
                    line=dict(color="green", dash="dash"),
                    opacity=alpha_Fade_obs,
                    name="Obs.",
                )
            )
        else:
            fig.add_trace(
                go.Scatter(
                    x=x_axis_obs,
                    y=a[:, 0],
                    line=dict(color="green", dash="dash"),
                    opacity=alpha_Fade_obs,
                    name="Policy {}".format(i),
                )
            )

    fig.add_trace(
        go.Scatter(
            x=x_axis_obs,
            y=arr_from_sql_dfq50_years_obs.flatten(),
            line=dict(color="black", width=2.5),
            opacity=1,
            name="Median",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=x_axis_obs,
            y=arr_from_sql_dfq75_years_obs.flatten(),
            line=dict(color="yellow", width=2.5),
            opacity=1,
            name="75th percentile",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=x_axis_obs,
            y=arr_from_sql_dfq90_years_obs.flatten(),
            line=dict(color="magenta", width=2.5),
            opacity=1,
            name="90th percentile",
        )
    )

    # Customize x-axis
    fig.update_xaxes(
        title="Years",
        range=(x_axis_obs.min(), x_axis_obs.max()),
        showgrid=True,
    )

    # Customize y-axis
    fig.update_yaxes(
        title="Number of Hot Days & Nights",
        # range=x_axis_obs,
        showgrid=True,
    )

    # Add title, font, and width to the figure
    fig.update_layout(
        title="Number of concurrent hot days and nights in Zurich between 1981-2020",
        font=dict(size=20),
    )

    return plotly_as_python_dict(fig)


historical_data_plot = _plot_historical_data()
historical_data_caption = " Yearly number of observed concurrent hot days and nights in Zurich between 1981-2020. The threshold for hot days is in the range 28°C–35°C and for hot nights is in the range 15°C–20°C.  Each line represents an adaptation policy. More stringent policies are those below the median (black line). The case from moderate to low or no adaptation is shown by the policies falling above the 75th (yellow line) and 90th (pink line) percentile respectively. It can be inferred that even in the years 2003 and 2015 the number of concurrent hot days a nights could be considerably reduced through different combination of adaptation policies aimed at reducing both hot days and nights."
