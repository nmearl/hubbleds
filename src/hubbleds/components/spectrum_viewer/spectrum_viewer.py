import pandas as pd
import solara
import reacton.ipyvuetify as rv
from ipyvuetify import VuetifyTemplate
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from astropy.table import Table
from pandas import DataFrame
from typing import Callable


df = Table(
    {"wave": np.linspace(3000, 8000, 1000), "flux": np.random.sample(1000)}
).to_pandas()


@solara.component
def SpectrumViewer(
    data: DataFrame,
    obs_wave: float | None = None,
    spectrum_click_enabled: bool = False,
    on_obs_wave_measured: Callable = None,
    on_obs_wave_tool_clicked: Callable = lambda: None,
    on_zoom_tool_clicked: Callable = lambda: None,
):
    vertical_line_visible = solara.use_reactive(False)
    toggle_group_state, set_toggle_group_state = solara.use_state(None)

    def _obs_wave_tool_toggled():
        on_obs_wave_tool_clicked()

    with rv.Card():
        with rv.Toolbar(color="primary", dense=True):
            with rv.ToolbarTitle():
                solara.Text("SPECTRUM VIEWER")

            rv.Spacer()

            with rv.BtnToggle(
                v_model=toggle_group_state,
                on_v_model=set_toggle_group_state,
                flat=True,
                tile=True,
                group=True,
            ):
                solara.IconButton(
                    icon_name="mdi-select-search",
                    on_click=on_zoom_tool_clicked,
                )

                solara.IconButton(
                    icon_name="mdi-lambda",
                    on_click=_obs_wave_tool_toggled,
                )

        if data is None:
            with rv.Sheet(
                style_="height: 360px", class_="d-flex justify-center align-center"
            ):
                rv.ProgressCircular(size=100, indeterminate=True, color="primary")

            return
        elif not isinstance(data, DataFrame):
            with rv.Sheet(
                style_="height: 360px", class_="d-flex justify-center align-center"
            ):
                solara.Text("Select a galaxy to view its spectrum")

            return

        fig = px.line(data, x="wave", y="flux")

        fig.add_vline(
            x=obs_wave,
            line_width=1,
            line_color="red",
            # annotation_text="1BASE",
            # annotation_font_size=12,
            # annotation_position="top right",
            visible=vertical_line_visible.value and obs_wave > 0.0,
        )

        fig.add_shape(
            editable=False,
            x0=6790,
            x1=6830,
            y0=85,
            y1=100,
            xref="x",
            yref="y",
            line_color="red",
            fillcolor="red",
            # visible=
        )

        fig.update_layout(
            xaxis_zeroline=False,
            yaxis_zeroline=False,
            xaxis=dict(
                showspikes=toggle_group_state == 1,
                showline=toggle_group_state == 1,
                spikecolor="black",
                spikethickness=1,
                spikedash="solid",
                spikemode="across",
                spikesnap="cursor",
            ),
            spikedistance=-1,
            hovermode="x",
        )

        def _clicked(**kwargs):
            if spectrum_click_enabled and toggle_group_state == 1:
                vertical_line_visible.set(True)
                # lambda_obs.set(round(kwargs['points']['xs'][0]))
                on_obs_wave_measured(round(kwargs["points"]["xs"][0]))

        solara.FigurePlotly(
            fig,
            on_click=lambda kwargs: _clicked(**kwargs),
            dependencies=[
                obs_wave,
                vertical_line_visible.value,
                data,
                toggle_group_state,
            ],
        )
