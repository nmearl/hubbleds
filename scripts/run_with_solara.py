from warnings import filterwarnings

filterwarnings(action="ignore", category=UserWarning)

from cosmicds.app import Application
import solara


@solara.component
def App():
    return Application.element(story='hubbles_law', update_db=False,
                               show_team_interface=True, allow_advancing=True,
                               create_new_student=False)


@solara.component
def Page():
    with solara.VBox() as main:
        App()
        solara.Title(title="Hubble's Law Data Story")

    return main
