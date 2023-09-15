import panel as pn
from climate_scenarios_fig import (
    #    adaptation_pathways_caption,
    adaptation_pathways_figs,
    box_fig_plot,
    scenario_captions,
    scenario_fig_plot,
    scenario_titles,
)
from global_params_and_utils import (
    FIG_DIRECTORY,
    HISTORICAL_YEARS,
    SCENARIOS,
    SCENARIOS_YEARS,
)
from historical_data_fig import (
    historical_data_caption,
    historical_data_plot,
)

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

caption_styles = {"font-size": "16px"}
title_styles = {"font-size": "20px", "text-align": "center", "font-weight": "bold"}
column_all_scenarios = pn.Accordion(width=1200)
for el in SCENARIOS:
    scenario_fig = PLOTLY_SCENARIO_FIG_DATA_PANE[el]
    box_fig = box_fig_plot[el]
    row = pn.Column(
        pn.pane.HTML(
            "Projected number of concurrent hot days and nights",
            styles=title_styles,
            align="center",
        ),
        pn.Row(scenario_fig, box_fig),
        pn.pane.HTML(
            "Adaptation pathways",
            styles=title_styles,
            align="center",
        ),
        adaptation_pathways_figs[el],
        pn.pane.HTML(scenario_captions[el], styles=caption_styles),
        # pn.pane.HTML(adaptation_pathways_caption[el], styles=caption_styles),
    )

    column_all_scenarios.append((scenario_titles[el], row))

caption_feature_scoring = "Feature scoring analysis showing the relative importance of the choice of climate scenarios (RCPs), climate model (Climate Models), intra-climate model variability (Intra CM variability), thresholds of minimum temperature (Tmin) and thresholds of minimum temperature (Tmax) for the outcomes. The outcomes are the number of concurrent hot days and nights, their frequency and length. Higher numbers and bright colours indicate higher importance."

# add content to template main
template.main.extend(
    pn.Column(
        pn.Card(
            widget_historical_years,
            PLOTLY_HISTORICAL_DATA_PANE,
            pn.pane.HTML(historical_data_caption, styles=caption_styles),
            title="Zürich, Historical Data",
            **card_style,
        ),
        pn.Card(
            widget_scenarios_years,
            column_all_scenarios,
            title="Climate Scenarios",
            **card_style,
        ),
        pn.Card(
            pn.pane.PNG(
                FIG_DIRECTORY / "feature_scoring.png",
                width=700,
                align="center",
            ),
            pn.pane.HTML(caption_feature_scoring, styles=caption_styles),
            title="Feature Scoring",
            **card_style,
        ),
        LINK,
    ),
)
template.servable()
