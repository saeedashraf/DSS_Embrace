import panel as pn
import param

template = pn.template.MaterialTemplate(
    title="DSS_Embrace",
    side="DSS_Embrace",
)


class DSS_Embrace(param.Parameterized):
    _climate_scenarios = ["RPC2.6", "RPC4.5", "RPC8.5"]
    climate_scenarios = param.ListSelector(
        _climate_scenarios,
        objects=_climate_scenarios,
        label="Climate Scenarios",
        precedence=1,
    )
    figs_climate_scenarios = {
        "RPC2.6": ["4.png", "13.png"],
        "RPC4.5": ["7.png", "12.png"],
        "RPC8.5": ["10.png", "11.png"],
    }

    _scenarios_data_range = (2020, 2100)
    scenarios_data_range = param.Range(
        _scenarios_data_range, bounds=_scenarios_data_range, precedence=1
    )

    show_historical_data = param.Boolean(
        True, label="Show Historical Data", precedence=2
    )

    _historical_data_range = (1981, 2019)
    historical_data_range = param.Range(
        _historical_data_range, bounds=_historical_data_range, precedence=2
    )
    show_feature_scoring = param.Boolean(
        True, label="Show Feature Scoring", precedence=3
    )

    @param.depends("climate_scenarios", "scenarios_data_range")
    def view(self):
        res = pn.Column()
        for el in self.climate_scenarios:
            row = pn.Row()
            for fig in self.figs_climate_scenarios[el]:
                row.append(pn.pane.PNG(f"./src/fig/{fig}", width=600))
            res.append(row)
        return res

    @param.depends("show_historical_data", "historical_data_range")
    def view_show_historical_data(self):
        if self.show_historical_data is True:
            return pn.pane.PNG("./src/fig/1.png", width=800)

        else:
            return None

    @param.depends("show_feature_scoring")
    def view_show_feature_scoring(self):
        if self.show_feature_scoring is True:
            return pn.pane.PNG("./src/fig/14_.png", width=800)
        else:
            return None


app = DSS_Embrace(
    name="Parameters",
    parameters=[
        "climate_scenarios",
        "scenarios_data_range",
        "historical_data_range",
        "show_historical_data",
        "show_feature_scoring",
    ],
)
link = pn.pane.Markdown(
    """
    
    See [EClim webpage](https://eclim-research.ch/) 

"""
)
template.sidebar.append(
    pn.Column(
        app.param["climate_scenarios"],
        app.param["scenarios_data_range"],
        pn.layout.Divider(),
        app.param["show_historical_data"],
        app.param["historical_data_range"],
        pn.layout.Divider(),
        app.param["show_feature_scoring"],
        pn.Spacer(height=20),
        link,
    )
)


template.main.append(
    pn.Column(
        app.view,
        app.view_show_historical_data,
        app.view_show_feature_scoring,
    ),
)

template.servable()
