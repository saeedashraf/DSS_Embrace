import numpy as np
import pandas as pd
import panel as pn
import plotly.graph_objects as go
from global_params_and_utils import (
    DATA_DIRECTORY,
    LANGUAGE_WIDGET,
    plotly_as_python_dict,
)


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

    p_Step = 4
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
                    name="Policy {}".format(i // p_Step),
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
        title="TODO",
        font=dict(size=20),
    )

    return plotly_as_python_dict(fig)


def translate_PLOTLY_HISTORICAL_DATA_PANE(language):
    title = {
        "EN": "Historic concurrent hot days and nights in Zurich and policy impact",
        "DE": "Historische zusammen auftretende Hitzetage und Tropennächte in Zürich <br>und Strategiewirkung",
    }[language]
    historical_data_plot = _plot_historical_data()

    historical_data_plot["layout"]["title"]["text"] = title
    return pn.pane.Plotly(historical_data_plot, width=1200)


PLOTLY_HISTORICAL_DATA_PANE = pn.bind(
    translate_PLOTLY_HISTORICAL_DATA_PANE, language=LANGUAGE_WIDGET
)


def translate_historical_data_caption(language):
    return {
        "EN": "The graph depicts the yearly number of observed concurrent hot days (28°C–35°C) and nights (15°C–20°C) in Zurich from 1981 to 2020 and the impact of different adaptation policies. The lines represent the number of hot days and nights that exceed the thresholds. These lines depict the combination of observed hot day and night extremes and the effect of adaptation policies to alleviate such extremes. Stringent policies are those leading to extremes below and up to the black line, more relaxed policies fall between the yellow and pink lines and little to now adaptation policies fall above the pink line. From the graph, it can be inferred that even in the years 2003 and 2015 the number of concurrent hot days and nights extremes could have been considerably reduced",
        "DE": "Die Grafik stellt die jährliche Anzahl der beobachteten zusammen auftretenden Hitzetage (28°C-35°C) und Tropennächte (15°C-20°C) in Zürich von 1981 bis 2020 sowie die Wirkung verschiedener Anpassungsmassnahmen dar. Die Linien stellen die Anzahl Hitzetage und Tropennächte dar, die die Schwellenwerte überschreiten. Diese Linien zeigen die Kombination von beobachteten Extremen von heissen Tagen und Nächten und die Wirkung von Anpassungsmassnahmen zur Abschwächung dieser Extreme. Strenge Massnahmen sind solche, die zu Extremen unterhalb und bis zur schwarzen Linie führen, die Extreme unter weniger strengen Massnahmen liegen zwischen der gelben und der rosafarbenen Linie und die Extreme unter wenig bis gar keinen Anpassungsmassnahmen liegen oberhalb der rosafarbenen Linie. Aus der Graphik lässt sich ableiten, dass selbst in den Jahren 2003 und 2015 die Zahl der zusammen auftretenden Hitzetage und Tropennächte erheblich hätte reduziert werden können.",
    }[language]


historical_data_caption = pn.bind(
    translate_historical_data_caption, language=LANGUAGE_WIDGET
)
