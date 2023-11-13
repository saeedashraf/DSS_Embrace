import json
from pathlib import Path

import panel as pn
import plotly.io as pio

DATA_DIRECTORY = Path("./src/data/")
FIG_DIRECTORY = Path("./src/fig/")

SCENARIOS = ["RPC2.6", "RPC4.5", "RPC8.5"]
SCENARIOS_AS_NUMBER = SCENARIOS[-3] + SCENARIOS[-1]
SCENARIOS_COLOR = {"26": "green", "45": "orange", "85": "red"}
SCENARIOS_YEARS = (2020, 2100)
HISTORICAL_YEARS = (1981, 2020)


def plotly_as_python_dict(fig):
    return json.loads(pio.to_json(fig))


def number_from_climate_scenario(climate_scenario):
    return climate_scenario[-3] + climate_scenario[-1]


LANGUAGE_WIDGET = pn.widgets.Select(
    name="EN/DE", options=["EN", "DE"], value="EN", width=80
)
