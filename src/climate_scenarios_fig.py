import numpy as np
import pandas as pd
import panel as pn
import plotly.express as px
import plotly.graph_objects as go
from global_params_and_utils import (
    DATA_DIRECTORY,
    FIG_DIRECTORY,
    LANGUAGE_WIDGET,
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
        font=dict(size=12),
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
        font=dict(size=12),
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


def translate_RPC26(language):
    return {
        "EN": 'Zurich, Scenario "low global warming"',
        "DE": "Zürich, Szenario «geringe globale Erwärmung»",
    }[language]


def translate_RPC45(language):
    return {
        "EN": 'Zurich, Scenario "medium global warming"',
        "DE": "Zürich, Szenario «mittlere globale Erwärmung»",
    }[language]


def translate_RPC85(language):
    return {
        "EN": 'Zurich, Scenario "high to very high global warming"',
        "DE": "Zürich, Szenario «hohe bis sehr hohe globale Erwärmung»",
    }[language]


translate_scenario_pane_titles = {
    "RPC2.6": translate_RPC26,
    "RPC4.5": translate_RPC45,
    "RPC8.5": translate_RPC85,
}


scenario_pane_titles = {
    el: pn.bind(translate_scenario_pane_titles[el], language=LANGUAGE_WIDGET)
    for el in SCENARIOS
}


def translate_scenario_titles(language):
    return {
        "EN": "Projected number of concurrent hot days and nights",
        "DE": "Prognostizierte Anzahl der zusammen auftretenden Hitzetage und Tropennächte",
    }[language]


scenario_titles = pn.bind(translate_scenario_titles, language=LANGUAGE_WIDGET)


def translate_caption_RPC26(language):
    return {
        "EN": "The figure on the top left shows the yearly projected number of concurrent hot days and nights in Zurich until the end of the century under a scenario of low global warming (i.e. in the order of 1.8°C temperature increase by the end of the century above the period 1850-1900). The threshold for hot days is in the range 28°C–35°C and for hot nights is in the range 15°C–20°C. The lines represent the number of hot days and nights that exceed the thresholds. These lines depict the combination of future hot day and night extremes and the effect of adaptation policies to alleviate such extremes. Stringent policies are those leading to extremes below and up to the black line, more relaxed policies fall between the yellow and pink lines and little to now adaptation policies fall above the pink line. The figure on the top right shows the statistical distribution of the number of hot days and nights per decade using boxplots. In the figure on the bottom should be understood as a metro map. The metro lines represent alternative sequences of adaptation measures that can be taken over time. The black circle depict the beginning of the metro line as well as the transfer to another line. The bar means that the pathway has become ineffective to alleviate the impacts of extremes.",
        "DE": "Die Abbildung oben links zeigt die jährlich prognostizierte Anzahl zusammen auftretender Hitzetage und Tropennächte in Zürich bis zum Ende des Jahrhunderts unter einem Szenario mit geringer globaler Erwärmung (d.h. in der Grössenordnung von 1,8°C Temperaturanstieg bis zum Ende des Jahrhunderts gegenüber dem Zeitraum 1850-1900). Der Schwellenwert für Hitzetage liegt im Bereich von 28°C-35°C und für Tropennächte im Bereich von 15°C-20°C. Die Linien stellen die Anzahl Hitzetage und Tropennächte dar, die diese Schwellenwerte überschreiten. Diese Linien zeigen die Kombination von zukünftigen Extremen von Hitzetagen und Tropennächten und die Wirkung von Anpassungsmassnahmen zur Abschwächung dieser Extreme. Strenge Massnahmen sind solche, die zu Extremen unterhalb und bis zur schwarzen Linie führen, bei weniger strengen Massnahmen liegen die Extreme zwischen der gelben und der rosafarbenen Linie und Extreme bei wenig bis gar keinen Anpassungsmassnahmen liegen oberhalb der rosafarbenen Linie. Die Abbildung oben rechts zeigt die statistische Verteilung der Anzahl der Hitzetage und Tropennächte pro Jahrzehnt anhand von Boxplots. Die untere Abbildung ist als Metrokarte zu verstehen. Die Metrolinien stellen alternative Abfolgen von Anpassungsmassnahmen dar, die im Laufe der Zeit ergriffen werden können. Der schwarze Kreis stellt den Beginn der Metrolinie sowie den Übergang zu einer anderen Linie dar. Der Balken bedeutet, dass der Pfad unwirksam geworden ist, um die Auswirkungen von Extremen abzumildern.",
    }[language]


def translate_caption_RPC45(language):
    return {
        "EN": "The figure on the top left shows the yearly projected number of concurrent hot days and nights in Zurich until the end of the century under a scenario of medium global warming (in the order of 2.7°C temperature increase by the end of the century above the period 1850-1900). The threshold for hot days is in the range 28°C–35°C and for hot nights is in the range 15°C–20°C. The lines represent the number of hot days and nights that exceed the thresholds. These lines depict the combination of future hot day and night extremes and the effect of adaptation policies to alleviate such extremes. Stringent policies are those leading to extremes below and up to the black line, more relaxed policies fall between the yellow and pink lines and little to now adaptation policies fall above the pink line. The figure on the top right shows the statistical distribution of the number of hot days and nights per decade using boxplots. In the figure on the bottom should be understood as a metro map. The metro lines represent alternative sequences of adaptation measures that can be taken over time. The black circle depict the beginning of the metro line as well as the transfer to another line. The bar means that the pathway has become ineffective to alleviate the impacts of extremes.",
        "DE": "Die Abbildung oben links zeigt die jährlich prognostizierte Anzahl zusammen auftretender Hitzetage und Tropennächte in Zürich bis zum Ende des Jahrhunderts unter einem Szenario mit mittlerer globaler Erwärmung (d.h. in der Grössenordnung von 1,8°C Temperaturanstieg bis zum Ende des Jahrhunderts gegenüber dem Zeitraum 1850-1900). Der Schwellenwert für Hitzetage liegt im Bereich von 28°C-35°C und für Tropennächte im Bereich von 15°C-20°C. Die Linien stellen die Anzahl der Hitzetage und Tropennächte dar, die diese Schwellenwerte überschreiten. Diese Linien zeigen die Kombination von zukünftigen Extremen von Hitzetagen und Tropennächte und die Wirkungen von Anpassungsmassnahmen zur Abschwächung dieser Extreme. Strenge Massnahmen sind solche, die zu Extremen unterhalb und bis zur schwarzen Linie führen, bei weniger strengen Massnahmen liegen die Extreme zwischen der gelben und der rosafarbenen Linie und bei wenig bis gar keinen Anpassungsmassnahmen liegen die Extreme oberhalb der rosafarbenen Linie. Die Abbildung oben rechts zeigt die statistische Verteilung der Anzahl Hitzetage und Tropennächte pro Jahrzehnt anhand von Boxplots. Die untere Abbildung ist als Metrokarte zu verstehen. Die Metrolinien stellen alternative Abfolgen von Anpassungsmassnahmen dar, die im Laufe der Zeit ergriffen werden können. Der schwarze Kreis stellt den Beginn der Metrolinie sowie den Übergang zu einer anderen Linie dar. Der Balken bedeutet, dass der Pfad unwirksam geworden ist, um die Auswirkungen von Extremen abzumildern.",
    }[language]


def translate_caption_RPC85(language):
    return {
        "EN": "The figure on the top left shows the yearly projected number of concurrent hot days and nights in Zurich until the end of the century under a scenario of high to very high global warming (e.g. more than 4°C temperature increase by the end of the century above the period 1850-1900). The threshold for hot days is in the range 28°C–35°C and for hot nights is in the range 15°C–20°C. The lines represent the number of hot days and nights that exceed the thresholds. These lines depict the combination of future hot day and night extremes and the effect of adaptation policies to alleviate such extremes. Stringent policies are those leading to extremes below and up to the black line, more relaxed policies fall between the yellow and pink lines and little to now adaptation policies fall above the pink line. The figure on the top right shows the statistical distribution of the number of hot days and nights per decade using boxplots. In the figure on the bottom should be understood as a metro map. The metro lines represent alternative sequences of adaptation measures that can be taken over time. The black circle depict the beginning of the metro line as well as the transfer to another line. The bar means that the pathway has become ineffective to alleviate the impacts of extremes.",
        "DE": "Die Abbildung oben links zeigt die jährlich prognostizierte Anzahl zusammen auftretender Hitzetage und Tropennächte in Zürich bis zum Ende des Jahrhunderts unter einem Szenario mit hoher bis sehr hoher globaler Erwärmung (d.h. in der Grössenordnung von 1,8°C Temperaturanstieg bis zum Ende des Jahrhunderts gegenüber dem Zeitraum 1850-1900). Der Schwellenwert für Hitzetage liegt im Bereich von 28°C-35°C und für Tropennächte im Bereich von 15°C-20°C. Die Linien stellen die Anzahl der Hitzetage und Tropennächte dar, die diese Schwellenwerte überschreiten. Diese Linien zeigen die Kombination von zukünftigen Extremen von Hitzetagen und Tropennächte und die Wirkung von Anpassungsmassnahmen zur Abschwächung dieser Extreme. Strenge Massnahmen sind solche, die zu Extremen unterhalb und bis zur schwarzen Linie führen, bei weniger strengen Massnahmen liegen die Extreme zwischen der gelben und der rosafarbenen Linie und bei wenig bis gar keinen Anpassungsmassnahmen liegen die Extreme oberhalb der rosafarbenen Linie. Die Abbildung oben rechts zeigt die statistische Verteilung der Anzahl Hitzetage und Tropennächte pro Jahrzehnt anhand von Boxplots. Die untere Abbildung ist als Metrokarte zu verstehen. Die Metrolinien stellen alternative Abfolgen von Anpassungsmassnahmen dar, die im Laufe der Zeit ergriffen werden können. Der schwarze Kreis stellt den Beginn der Metrolinie sowie den Übergang zu einer anderen Linie dar. Der Balken bedeutet, dass der Pfad unwirksam geworden ist, um die Auswirkungen von Extremen abzumildern.",
    }[language]


translate_caption_titles = {
    "RPC2.6": translate_caption_RPC26,
    "RPC4.5": translate_caption_RPC45,
    "RPC8.5": translate_caption_RPC85,
}


scenario_captions = {
    el: pn.bind(translate_caption_titles[el], language=LANGUAGE_WIDGET)
    for el in SCENARIOS
}


adaptation_pathways_figs = {
    el: pn.pane.PNG(
        FIG_DIRECTORY / f"metro_map_{number_from_climate_scenario(el)}.PNG",
        width=850,
        align="center",
    )
    for el in SCENARIOS
}


def translate_title_pathways(language):
    return {"EN": "Adaptation pathways", "DE": "Anpassungspfade"}[language]


title_pathways = pn.bind(translate_title_pathways, language=LANGUAGE_WIDGET)


# adaptation_pathways_caption = {
#     "RPC2.6": "Each line represents an adaptation measure. The dot depicts either the starting of a measure or transfer to another measure (or pathway). The bar means that a measure is not anymore effective.",
#     "RPC4.5": "Each line represents an adaptation measure. The dot depicts either the starting of a measure or transfer to another measure (or pathway). The dashed lines show the overlapping amongst two or more measure. The bar means that a measure is not anymore effective.",
#     "RPC8.5": "Each line represents an adaptation measure. The dot depicts either the starting of a measure or transfer to another measure (or pathway). The dashed lines show the overlapping amongst two or more measure. The bar means that a measure is not anymore effective.",
# }
