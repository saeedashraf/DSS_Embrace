import numpy as np
import pandas as pd
import panel as pn
import param
import plotly.express as px

pn.extension("plotly", template="material")


class SimpleCase(param.Parameterized):
    case_1 = param.ObjectSelector(
        default="implemented",
        objects=["implemented", "not implemented"],
        label="Pick a Case",
    )
    bounds = param.Range((-2, 4), bounds=(-2, 4), precedence=1)
    show_fig = param.Boolean(False, label="Show Figure", precedence=2)

    @param.depends("case_1", watch=True)
    def _update_bounds(self):
        if self.case_1 == "not implemented":
            self.param["bounds"].precedence = -1
            self.param["show_fig"].precedence = -1
            self.param["bounds"].default = None
        else:
            self.param["bounds"].precedence = 1
            self.param["show_fig"].precedence = 2
            self.param["bounds"].default = (-2, 4)

    @param.depends("case_1", "bounds")
    def view(self):
        if self.case_1 == "implemented":
            a = np.linspace(self.bounds[0], self.bounds[1])
            df = pd.DataFrame(a, a).reset_index().rename(columns={"index": "X", 0: "Y"})
            return px.line(df, x="X", y="Y", title="Title")
        else:
            return None

    @param.depends("show_fig")
    def view_show_fig(self):
        if self.show_fig is True:
            a = np.linspace(-10, 10)
            df = pd.DataFrame(a, a).reset_index().rename(columns={"index": "X", 0: "Y"})
            return px.line(df, x="X", y="Y", title="Show Figure")
        else:
            return None


a = SimpleCase(name="Simple Case", parameters=["case_1", "bounds", "show_fig"])
pn.Row(a.param, a.view, a.view_show_fig).servable(title="DSS_Embrance")
