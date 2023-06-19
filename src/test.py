import panel as pn
from climate_scenarios_fig import box_fig_plot, scenario_fig_plot
from global_params_and_utils import (
    FIG_DIRECTORY,
    HISTORICAL_YEARS,
    SCENARIOS,
    SCENARIOS_YEARS,
)
from historical_data_fig import historical_data_plot

template = pn.template.MaterialTemplate(
    title="DSS_Embrace",
    header_background="ForestGreen",
)


LINK = pn.pane.Markdown(
    """
    
    See [EClim webpage](https://eclim-research.ch/) 

"""
)

PLOTLY_HISTORICAL_DATA_PANE = pn.pane.Plotly(historical_data_plot, width=1200)
PLOTLY_SCENARIO_FIG_DATA_PANE = {
    el: pn.pane.Plotly(scenario_fig_plot[el]) for el in SCENARIOS
}


# Widgets

widget_historical_years = pn.widgets.IntRangeSlider(
    name="Historical Years Range",
    start=HISTORICAL_YEARS[0],
    end=HISTORICAL_YEARS[1],
    value=HISTORICAL_YEARS,
    step=1,
)


widget_scenarios_years = pn.widgets.IntRangeSlider(
    name="Scenarios Years Range",
    start=SCENARIOS_YEARS[0],
    end=SCENARIOS_YEARS[1],
    value=SCENARIOS_YEARS,
    step=1,
)


card_style = {
    "header_color": "white",
    "header_background": "DarkSeaGreen",
    "active_header_background": "ForestGreen",
    "styles": {"background": "white"},
    "collapsed": True,
    "width": 1220,
}


PLOTLY_XAXIS_RANGE_UPDATE_js_code = """
    target.layout.xaxis.range = source.value
    target.properties.layout.change.emit()
"""
PLOTLY_HISTORICAL_DATA_PANE_link = widget_historical_years.jslink(
    PLOTLY_HISTORICAL_DATA_PANE, code={"value": PLOTLY_XAXIS_RANGE_UPDATE_js_code}
)

PLOTLY_SCENARIO_FIG_DATA_PANE_js_code = """
    target.layout.xaxis.range = source.value
    target.properties.layout.change.emit()
"""
PLOTLY_SCENARIO_FIG_DATA_PANE_link = {
    el: widget_scenarios_years.jslink(
        PLOTLY_SCENARIO_FIG_DATA_PANE[el],
        code={"value": PLOTLY_XAXIS_RANGE_UPDATE_js_code},
    )
    for el in SCENARIOS
}


column_all_scenarios = pn.Accordion(width=1200)
for el in SCENARIOS:
    scenario_fig = PLOTLY_SCENARIO_FIG_DATA_PANE[el]
    box_fig = box_fig_plot[el]
    row = pn.Row(scenario_fig, box_fig)

    column_all_scenarios.append((el, row))


def view_climate_scenarios(selected_climate_scenarios):
    column_all_scenarios.clear()
    for el in selected_climate_scenarios:
        scenario_fig = scenario_fig_plot[el]
        box_fig = box_fig_plot[el]
        row = pn.Row(scenario_fig, box_fig)

        column_all_scenarios.append(row)
    return column_all_scenarios


# add content to template main

template.main.extend(
    pn.Column(
        pn.Card(
            widget_historical_years,
            PLOTLY_HISTORICAL_DATA_PANE,
            title="Zürich, Historical Data",
            **card_style,
        ),
        pn.Card(
            widget_scenarios_years,
            column_all_scenarios,
            # view_climate_scenarios_as_tabs,
            title="Climate Scenarios",
            **card_style,
        ),
        pn.Card(
            pn.Row(
                pn.pane.PNG(FIG_DIRECTORY / "Presentation3.png", width=590),
                pn.pane.PNG(FIG_DIRECTORY / "feature_scoring.png", width=590),
            ),
            title="RPC8.5 and Feature Scoring",
            **card_style,
        ),
        LINK,
    ),
)
template.servable()
