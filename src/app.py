import panel as pn
from climate_scenarios_fig import (
    #    adaptation_pathways_caption,
    adaptation_pathways_figs,
    box_fig_plot,
    scenario_captions,
    scenario_fig_plot,
    scenario_pane_titles,
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
    title="DSS_Embrace: Decision Support for Climate Adaptation Planning",
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
            scenario_titles[el],
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

    column_all_scenarios.append((scenario_pane_titles[el], row))

caption_feature_scoring = "Feature scoring analysis showing the relative importance of the choice of climate scenarios (RCPs), climate model (Climate Models), intra-climate model variability (Intra CM variability), thresholds of minimum temperature (Tmin) and thresholds of minimum temperature (Tmax) for the outcomes. The outcomes are the number of concurrent hot days and nights, their frequency and length. Higher numbers and bright colours indicate higher importance."

description_text = "DSS_Embrace is a collaborative environment to embrace deep uncertainties in decision making on climate risks. Deep uncertainties often involve high stakes decisions, unique situations, long-term planning, or situations where the future may be fundamentally different from the past. In dealing with deep uncertainties, experts employ various methods and approaches to enhance decision-making and strategic planning. These include scenario analysis, modeling, simulation, Bayesian approaches, expert opinions, sensitivity analysis, and learning from parallel fields or historical analogies.  DSS_Embrace uses the so-called exploratory modelling framework where decision makers are confronted with several possible climate realisations and policy combinations. The climate realisations are the results of climate models, interannual climate variability and climate scenarios, whereas the policies represent the effect of potential adaptation measures. Adaptation pathways provide a flexible and dynamic approach to decision-making that can be adjusted over time as new information becomes available. Here, we sow some illustrative adaptation pathways to link the climate realisations-policies figure with concrete actions on the ground. DSS_Embrace is co-financed by the Digital Initiative Zurich (DIZH) and the Eclim Group at the Department of Geography."

# add content to template main
template.main.extend(
    pn.Column(
        pn.pane.HTML(description_text, styles=caption_styles),
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
            title="Relative importance of determinants for decision-making",
            **card_style,
        ),
        LINK,
    ),
)
template.servable()
