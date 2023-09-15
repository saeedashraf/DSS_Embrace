import numpy as np
import pandas as pd
import panel as pn
import plotly.express as px
import plotly.graph_objects as go
from global_params_and_utils import (
    DATA_DIRECTORY,
    FIG_DIRECTORY,
    SCENARIOS,
    SCENARIOS_COLOR,
    SCENARIOS_YEARS,
    number_from_climate_scenario,
    plotly_as_python_dict,
)


# only to be plotted, not used in the app due to big data (7MB/figure)
def _plot_box_fig(climate_scenario):
    scenario_as_number = number_from_climate_scenario(climate_scenario)

    # Load data from CSV file
    df = pd.read_csv(DATA_DIRECTORY / f"data_total_decadal_{scenario_as_number}.csv")
    df2 = df.iloc[:, -8:]

    # Set colors for the box plots
    colors = 8 * [SCENARIOS_COLOR[scenario_as_number]]

    # Plot box plots with colors
    fig = px.box(
        df2,
        color_discrete_sequence=colors,
    )

    # Customize layout
    fig.update_yaxes(
        range=[0, 120],
    )

    fig.update_layout(
        # title=f"Zurich {climate_scenario}",
        font=dict(size=18),
        yaxis_title="Number of Hot Days & Nights <br> per Decade",
        xaxis_title="Years",
        boxmode="group",
        width=570,
    )
    fig.update_xaxes(tickangle=30)

    # fig.write_image(FIG_DIRECTORY / f"box_fig_RPC_{scenario_as_number}.png")

    return plotly_as_python_dict(fig)


def _plot_number_of_hot_days_and_nights(climate_scenario):
    scenario_as_number = number_from_climate_scenario(climate_scenario)

    column = f"q50_years_{scenario_as_number}"
    df_from_csv_dfq50_years = pd.read_csv(DATA_DIRECTORY / f"df{column}.csv")
    arr_from_sql_dfq50_years = df_from_csv_dfq50_years[column].values

    column = f"q75_years_{scenario_as_number}"
    df_from_csv_dfq75_years = pd.read_csv(DATA_DIRECTORY / f"df{column}.csv")
    arr_from_sql_dfq75_years = df_from_csv_dfq75_years[column].values

    column = f"q90_years_{scenario_as_number}"
    df_from_csv_dfq90_years = pd.read_csv(DATA_DIRECTORY / f"df{column}.csv")
    arr_from_sql_dfq90_years = df_from_csv_dfq90_years[column].values

    df_from_csv = pd.read_csv(
        DATA_DIRECTORY / f"array_data_matrix_HotDays_{scenario_as_number}.csv"
    )
    arr_from_sql_matrix_HotDays = df_from_csv.values.reshape((5440, 120, 2))

    p_Step = 300
    alpha_Fade = 1

    fig = go.Figure()

    x_axis = np.arange(2020, 2101, step=1)

    for i in range(0, len(arr_from_sql_matrix_HotDays), p_Step):
        a = arr_from_sql_matrix_HotDays[i, 1:, 1:2].astype(float)
        fig.add_trace(
            go.Scatter(
                x=x_axis,
                y=a[:, 0],
                mode="lines",
                line=dict(color=SCENARIOS_COLOR[scenario_as_number], dash="dash"),
                opacity=alpha_Fade,
                name=f"Proj. Policy {i//p_Step+1}",
            )
        )

    fig.add_trace(
        go.Scatter(
            x=x_axis,
            y=arr_from_sql_dfq50_years[:],
            mode="lines",
            line=dict(color="black", width=1.5),
            opacity=1,
            name="median",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=x_axis,
            y=arr_from_sql_dfq75_years[:],
            mode="lines",
            line=dict(color="yellow", width=1.5),
            opacity=1,
            name="75th percentile",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=x_axis,
            y=arr_from_sql_dfq90_years[:],
            mode="lines",
            line=dict(color="magenta", width=2),
            opacity=1,
            name="90th percentile",
        )
    )
    # Andrei: range based on scenarios_data_range, remove tickvals
    # Customize x-axis
    fig.update_xaxes(
        range=[SCENARIOS_YEARS[0], SCENARIOS_YEARS[1]],
    )

    # Customize y-axis
    fig.update_yaxes(
        title="Number of Hot Days & Nights (M1)",
        range=[0, 40],
    )

    # Set subplot title
    fig.update_layout(
        # title=f"Zurich {climate_scenario}",
        font=dict(size=18),
        xaxis_title="Year",
        yaxis_title="Number of Hot Days & Nights",
        width=570,
    )
    fig.update_xaxes(tickangle=30)

    return plotly_as_python_dict(fig)


box_fig_plot = {el: _plot_box_fig(el) for el in SCENARIOS}


# box_fig_plot = {
#     el: pn.pane.PNG(
#         FIG_DIRECTORY / f"box_fig_RPC_{number_from_climate_scenario(el)}.png", width=570
#     )
#     for el in SCENARIOS
# }
scenario_fig_plot = {el: _plot_number_of_hot_days_and_nights(el) for el in SCENARIOS}

scenario_titles = {
    "RPC2.6": "Zurich, Scenario of low global warming",
    "RPC4.5": "Zurich, Scenario of medium global warming",
    "RPC8.5": "Zurich, Scenario of high to very high global warming",
}

# Projected number of concurrent hot days and nights in Zurich under

scenario_captions = {
    "RPC2.6": "The figure on the top left shows the yearly projected number of concurrent hot days and nights in Zurich until the end of the century under a scenario of low global warming (e.g. RCP2.6). The threshold for hot days is in the range 28°C–35°C and for hot nights is in the range 15°C–20°C.  Each line represents an adaptation policy in combination with a future realization of the climate. More stringent policies are those below the median (black line). The case from moderate to low or no adaptation is shown by the policies falling above the 75th (yellow line) and 90th (pink line) percentile respectively. The figure on the top right shows the statistical distribution of the number of hot days and nights per decade using boxplots. In the figure on the bottom each line represents an adaptation measure. The dot depicts either the starting of a measure or transfer to another measure (or pathway). The bar means that a measure is not anymore effective.",
    "RPC4.5": "The figure on the top left shows the yearly projected number of concurrent hot days and nights in Zurich until the end of the century under a scenario of medium global warming (e.g. RCP4.5). The threshold for hot days is in the range 28°C–35°C and for hot nights is in the range 15°C–20°C.  Each line represents an adaptation policy in combination with a future realization of the climate. More stringent policies are those below the median (black line). The case from moderate to low or no adaptation is shown by the policies falling above the 75th (yellow line) and 90th (pink line) percentile respectively. The figure on the top right shows the statistical distribution of the number of hot days and nights per decade using boxplots. In the figure on the bottom each line represents an adaptation measure. The dot depicts either the starting of a measure or transfer to another measure (or pathway). The dashed lines show the overlapping amongst two or more measure. The bar means that a measure is not anymore effective.",
    "RPC8.5": "The figure on the top left shows the yearly projected number of concurrent hot days and nights in Zurich until the end of the century under a scenario of high to very high global warming (e.g. RCP8.5). The threshold for hot days is in the range 28°C–35°C and for hot nights is in the range 15°C–20°C.  Each line represents an adaptation policy in combination with a future realization of the climate. More stringent policies are those below the median (black line). The case from moderate to low or no adaptation is shown by the policies falling above the 75th (yellow line) and 90th (pink line) percentile respectively. The figure on the top right shows the statistical distribution of the number of hot days and nights per decade using boxplots. In the figure on the bottom each line represents an adaptation measure. The dot depicts either the starting of a measure or transfer to another measure (or pathway). The dashed lines show the overlapping amongst two or more measure. The bar means that a measure is not anymore effective.",
}


adaptation_pathways_figs = {
    el: pn.pane.PNG(
        FIG_DIRECTORY / f"metro_map_{number_from_climate_scenario(el)}.PNG",
        width=850,
        align="center",
    )
    for el in SCENARIOS
}

# adaptation_pathways_caption = {
#     "RPC2.6": "Each line represents an adaptation measure. The dot depicts either the starting of a measure or transfer to another measure (or pathway). The bar means that a measure is not anymore effective.",
#     "RPC4.5": "Each line represents an adaptation measure. The dot depicts either the starting of a measure or transfer to another measure (or pathway). The dashed lines show the overlapping amongst two or more measure. The bar means that a measure is not anymore effective.",
#     "RPC8.5": "Each line represents an adaptation measure. The dot depicts either the starting of a measure or transfer to another measure (or pathway). The dashed lines show the overlapping amongst two or more measure. The bar means that a measure is not anymore effective.",
# }
