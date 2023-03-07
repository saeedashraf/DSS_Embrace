import numpy as np
import pandas as pd
import panel as pn
import param
import plotly.graph_objects as go

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
        df_from_csv_dfq50_years_obs = pd.read_csv("./src/data/dfq50_years_obs.csv")
        arr_from_sql_dfq50_years_obs = df_from_csv_dfq50_years_obs[
            "q50_years_obs"
        ].values

        df_from_csv_dfq75_years_obs = pd.read_csv("./src/data/dfq75_years_obs.csv")
        arr_from_sql_dfq75_years_obs = df_from_csv_dfq75_years_obs[
            "q75_years_obs"
        ].values

        df_from_csv_dfq90_years_obs = pd.read_csv("./src/data/dfq90_years_obs.csv")
        arr_from_sql_dfq90_years_obs = df_from_csv_dfq90_years_obs[
            "q90_years_obs"
        ].values

        df_from_csv = pd.read_csv("./src/data/array_data_matrix_HotDays_obs.csv")
        arr_from_sql_matrix_HotDays_obs = df_from_csv.values.reshape((80, 41, 2))

        # TODO: hardcoded - it should come from the the previous arr
        x_axis_obs = np.arange(1981, 2020 + 1)

        p_Step = 1
        alpha_Fade_obs = 1

        fig = go.Figure()

        for i in range(0, len(arr_from_sql_matrix_HotDays_obs), p_Step):
            a = arr_from_sql_matrix_HotDays_obs[i, 1:, 1:2].astype(float)
            fig.add_trace(
                go.Scatter(
                    x=x_axis_obs,
                    y=a[:, 0],
                    line=dict(color="green", dash="dash"),
                    opacity=alpha_Fade_obs,
                )
            )

        fig.add_trace(
            go.Scatter(
                x=x_axis_obs,
                y=arr_from_sql_dfq50_years_obs.flatten(),
                line=dict(color="black", width=2.5),
                opacity=1,
            )
        )
        fig.add_trace(
            go.Scatter(
                x=x_axis_obs,
                y=arr_from_sql_dfq75_years_obs.flatten(),
                line=dict(color="yellow", width=2.5),
                opacity=1,
            )
        )
        fig.add_trace(
            go.Scatter(
                x=x_axis_obs,
                y=arr_from_sql_dfq90_years_obs.flatten(),
                line=dict(color="red", width=2.5),
                opacity=1,
            )
        )
        # Andrei: remove `ticktext=values`, dynamig range using historical_data_range
        # Customize x-axis
        fig.update_xaxes(
            title="Years",
            tickvals=x_axis_obs,
            tickfont=dict(size=15),
            range=[self.historical_data_range[0], self.historical_data_range[1]],
            showgrid=True,
        )

        # Customize y-axis
        fig.update_yaxes(
            title="Number of Hot Days & Nights",
            titlefont=dict(size=17),
            range=[0, 30],
            showgrid=True,
        )

        # Add title to the figure
        fig.update_layout(
            title="Historical number of Hot Days & Nights (M1) Over the Years",
            title_font=dict(size=20),
        )

        # update with
        fig.update_layout(width=1200)
        if self.show_historical_data is True:
            return fig

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
