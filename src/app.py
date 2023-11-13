import panel as pn
from climate_scenarios_fig import (
    #    adaptation_pathways_caption,
    adaptation_pathways_figs,
    box_fig_plot,
    caption_pathways,
    scenario_captions,
    scenario_fig_plot,
    scenario_pane_titles,
    scenario_titles,
    title_pathways,
)
from global_params_and_utils import (
    FIG_DIRECTORY,
    HISTORICAL_YEARS,
    LANGUAGE_WIDGET,
    SCENARIOS,
    SCENARIOS_YEARS,
)
from historical_data_fig import (
    PLOTLY_HISTORICAL_DATA_PANE,
    historical_data_caption,
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
    "styles": {
        "background": "white",
    },
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
            scenario_titles,
            styles=title_styles,
            align="center",
        ),
        pn.Row(scenario_fig, box_fig),
        pn.pane.HTML(
            title_pathways,
            styles=title_styles,
            align="center",
        ),
        pn.Row(
            adaptation_pathways_figs[el],
            pn.pane.HTML(
                caption_pathways, styles=caption_styles, align="center", width=470
            ),
        ),
        pn.pane.HTML(scenario_captions[el], styles=caption_styles),
        # pn.pane.HTML(adaptation_pathways_caption[el], styles=caption_styles),
    )

    column_all_scenarios.append((scenario_pane_titles[el], row))


def translate_caption_feature_scoring(language):
    return {
        "EN": "Feature scoring analysis showing the relative importance of the choice of climate scenarios (RCPs), climate model (Climate Models), intra-climate model variability (Intra CM variability), thresholds of minimum temperature (Tmin) and thresholds of minimum temperature (Tmax) for the outcomes. The outcomes are the number of concurrent hot days and nights, their frequency and length. Higher numbers and bright colours indicate higher importance.",
        "DE": "Feature-Scoring-Analyse, die die relative Bedeutung der Auswahl der Klimaszenarien (RCPs), des Klimamodells (Klimamodelle), der Variabilität innerhalb des Klimamodells (Intra-CM-Variabilität), der Schwellenwerte der Mindesttemperatur (Tmin) und der Schwellenwerte der Maximaltemperatur (Tmax) für die Ergebnisse zeigt. Die Ergebnisse sind die Anzahl der zusammen auftretender Hitzetage und Tropenächte, deren Häufigkeit und Dauer. Höhere Zahlen und hellere Farben kenntzeichnen eine höhere Bedeutung.",
    }[language]


caption_feature_scoring = pn.bind(
    translate_caption_feature_scoring, language=LANGUAGE_WIDGET
)


def translate_title_historical(language):
    return {"EN": "Zürich, Historical Data", "DE": "Zürich: Historische Daten"}[
        language
    ]


historical_title = pn.bind(translate_title_historical, language=LANGUAGE_WIDGET)


def translate_description_text(language):
    return {
        "EN": "DSS_Embrace is a collaborative environment to embrace deep uncertainties in decision making on climate risks. Deep uncertainties often involve high stakes decisions, unique situations, long-term planning, or situations where the future may be fundamentally different from the past. In dealing with deep uncertainties, experts employ various methods and approaches to enhance decision-making and strategic planning. These include scenario analysis, modeling, simulation, Bayesian approaches, expert opinions, sensitivity analysis, and learning from parallel fields or historical analogies.  DSS_Embrace uses the so-called exploratory modelling framework where decision makers are confronted with several possible climate realisations and policy combinations. The climate realisations are the results of climate models, interannual climate variability and climate scenarios, whereas the policies represent the effect of potential adaptation measures. Adaptation pathways provide a flexible and dynamic approach to decision-making that can be adjusted over time as new information becomes available. Here, we sow some illustrative adaptation pathways to link the climate realisations-policies figure with concrete actions on the ground. DSS_Embrace is co-financed by the Digital Initiative Zurich (DIZH) and the Eclim Group at the Department of Geography.",
        "DE": "DSS_Embrace ist eine kollaborative Umgebung, um grossen Unsicherheiten bei der Entscheidungsfindung in Zusammenhang mit Klimarisiken zu berücksichtigen. Bei grossen Unsicherheiten geht es oft um Entscheidungen, bei denen viel auf dem Spiel steht, um einzigartige Fälle, um langfristige Planung oder um Situationen, in denen sich die Zukunft wesentlich von der Vergangenheit unterscheiden kann. Im Umgang mit grossen Unsicherheiten setzen Experten verschiedene Methoden und Ansätze ein, um die Entscheidungsfindung und strategische Planung zu verbessern. Dazu gehören Szenarioanalyse, Modellierung, Simulation, Bayesische Ansätze, Expertenmeinungen, Sensitivitätsanalysen und Lernen aus Parallelfeldern oder historischen Analogien. DSS_Embrace verwendet den so genannten explorativen Modellierungsansatz, bei dem die Entscheidungsträger mit mehreren möglichen Entwicklungen des Klimas und Strategiekombinationen konfrontiert werden. Die Klimaentwicklungen sind die Ergebnisse von Klimamodellen, interannueller Klimavariabilität und Klimaszenarien, während die Strategien die Wirkung möglicher Anpassungsmassnahmen darstellen. Anpassungspfade bieten einen flexiblen und dynamischen Ansatz für die Entscheidungsfindung, der im Laufe der Zeit angepasst werden kann, wenn neue Informationen verfügbar werden. Hier werden einige illustrative Anpassungspfade aufgezeigt, um die Abbildung der Klimaentwicklungsstrategien mit konkreten Massnahmen vor Ort zu verbinden. DSS_Embrace wird von der Digitalisierungsinitiative der Zürcher Hochuschulen (DIZH) und der Eclim-Gruppe am Geographischen Institut mitfinanziert.",
    }[language]


description_text = pn.bind(translate_description_text, language=LANGUAGE_WIDGET)


def translate_title_historical(language):
    return {"EN": "Zürich, Historical Data", "DE": "Zürich: Historische Daten"}[
        language
    ]


historical_title = pn.bind(translate_title_historical, language=LANGUAGE_WIDGET)


def translate_title_climate_scenarios(language):
    return {"EN": "Climate Scenarios", "DE": "Klimaszenarien"}[language]


climate_scenarios_title = pn.bind(
    translate_title_climate_scenarios, language=LANGUAGE_WIDGET
)


def translate_title_decision_making(language):
    return {
        "EN": "Relative importance of determinants for decision-making",
        "DE": "Relative Bedeutung der Determinanten für die Entscheidungsfindung",
    }[language]


decision_making_title = pn.bind(
    translate_title_decision_making, language=LANGUAGE_WIDGET
)
# add content to template main
template.main.extend(
    pn.Column(
        LANGUAGE_WIDGET,
        pn.pane.HTML(
            description_text,
            styles=caption_styles,
            width=card_style["width"],
        ),
        pn.Card(
            widget_historical_years,
            PLOTLY_HISTORICAL_DATA_PANE,
            pn.pane.HTML(historical_data_caption, styles=caption_styles),
            title=historical_title,
            **card_style,
        ),
        pn.Card(
            widget_scenarios_years,
            column_all_scenarios,
            title=climate_scenarios_title,
            **card_style,
        ),
        pn.Card(
            pn.pane.PNG(
                FIG_DIRECTORY / "feature_scoring.png",
                width=700,
                align="center",
            ),
            pn.pane.HTML(caption_feature_scoring, styles=caption_styles),
            title=decision_making_title,
            **card_style,
        ),
        LINK,
    ),
)
template.servable()

# Not FEASIBLE - Update Titles
title = {
    "EN": "DSS_Embrace: Decision Support for Climate Adaptation Planning",
    "DE": "DSS_Embrace: Entscheidungshilfe für die Planung von Klimaanpassungsmassnahmen",
}
