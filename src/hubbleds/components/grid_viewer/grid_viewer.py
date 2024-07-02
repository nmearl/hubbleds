import solara

@solara.component
def ToolBar(viewer):
    solara.Row(
        children=[
            solara.Text(viewer.state.title, style={"padding-left": "1ch"}),
            solara.v.Spacer(),
            viewer.toolbar,
        ],
        margin=0,
        style={"align-items": "center", "background-color": "#0E397E"},
    )


@solara.component
def GridViewer(viewer):
    layout = solara.Column(
        children=[
            ToolBar(viewer),
            viewer.figure_widget,
        ],
        gap="0px",
        margin=0,
        style={},
        classes=["elevation-2"],
    )
    with solara.Card(
        children=[layout]
    ):
        pass