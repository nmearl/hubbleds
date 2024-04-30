import dataclasses

import numpy as np
import pandas as pd
import solara
from cosmicds.widgets.table import Table
from cosmicds.components import ScaffoldAlert
from cosmicds import load_custom_vue_components
from glue_jupyter.app import JupyterApplication
from reacton import ipyvuetify as rv
from solara import Reactive
from pathlib import Path
from astropy.table import Table

from ...components import DataTable, SpectrumViewer, SpectrumSlideshow, DopplerSlideshow
from ...data_management import *
from ...state import GLOBAL_STATE, LOCAL_STATE
from ...widgets.selection_tool import SelectionTool
from ...data_models.student import student_data, StudentMeasurement, example_data
from .component_state import ComponentState, Marker


GUIDELINE_ROOT = Path(__file__).parent / "guidelines"

gjapp = JupyterApplication(GLOBAL_STATE.data_collection, GLOBAL_STATE.session)

component_state = ComponentState()


def _on_galaxy_selected(galaxy):
    is_in = np.isin(
        [x.name for x in student_data.measurements], galaxy["name"]
    )  # Avoid duplicates
    already_present = is_in.size > 0 and is_in[0]

    if not already_present:
        student_data.measurements.append(StudentMeasurement(**galaxy))
        component_state.total_galaxies.value += 1


def _on_example_galaxy_table_row_selected(row):
    galaxy = row["item"]
    component_state.selected_example_galaxy.set(galaxy)
    component_state.lambda_rest.set(galaxy['rest_wave'])
    component_state.lambda_obs.subscribe(
        lambda *args: example_data.update(galaxy['id'], {'measured_wave': args[0]}))


def _on_galaxy_table_row_selected(row):
    galaxy = row["item"]
    component_state.selected_galaxy.set(galaxy)
    component_state.lambda_rest.set(galaxy['rest_wave'])
    component_state.lambda_obs.subscribe(
        lambda *args: student_data.update(galaxy['id'], {'measured_wave': args[0]}))


@solara.component
def Page():
    # Custom vue-only components have to be registered in the Page element
    #  currently, otherwise they will not be available in the front-end
    load_custom_vue_components()

    # Solara's reactivity is often tied to the _context_ of the Page it's
    #  being rendered in. Currently, in order to trigger subscribed callbacks,
    #  state connections need to be initialized _inside_ a Page.
    component_state.setup()

    solara.Text(
        f"Current step: {component_state.current_step.value}, "
        f"Next step: {Marker(component_state.current_step.value.value + 1)}"
        f"Can advance: {component_state.can_transition(next=True)}"
    )

    if LOCAL_STATE.debug_mode:

        def _on_select_galaxies_clicked():
            gal_tab = Table(component_state.galaxy_data)
            gal_tab["id"] = [str(x) for x in gal_tab["id"]]
            for i in range(5 - component_state.total_galaxies.value):
                gal = dict(gal_tab[i])
                _on_galaxy_selected(gal)

            component_state.transition_to(Marker.sel_gal3, force=True)

        solara.Button("Select 5 Galaxies", on_click=_on_select_galaxies_clicked)
        solara.Text(f"{component_state.doppler_calc_dialog.value}")

    with rv.Row():
        with rv.Col(cols=4):
            ScaffoldAlert(
                GUIDELINE_ROOT / "GuidelineIntro.vue",
                event_next_callback=lambda *args: component_state.transition_next(),
                can_advance=component_state.can_transition(next=True),
                show=component_state.is_current_step(Marker.mee_gui1),
            )
            ScaffoldAlert(
                GUIDELINE_ROOT / "GuidelineSelectGalaxies1.vue",
                event_next_callback=lambda *args: component_state.transition_next(),
                event_back_callback=lambda *args: component_state.transition_previous(),
                can_advance=component_state.can_transition(next=True),
                show=component_state.is_current_step(Marker.sel_gal1),
            )
            ScaffoldAlert(
                GUIDELINE_ROOT / "GuidelineSelectGalaxies2.vue",
                event_next_callback=lambda *args: component_state.transition_next(),
                event_back_callback=lambda *args: component_state.transition_previous(),
                can_advance=component_state.can_transition(next=True),
                show=component_state.is_current_step(Marker.sel_gal2),
                state_view={
                    "total_galaxies": component_state.total_galaxies.value,
                    "selected_galaxy": bool(component_state.selected_galaxy.value),
                },
            )
            ScaffoldAlert(
                GUIDELINE_ROOT / "GuidelineSelectGalaxies3.vue",
                event_next_callback=lambda *args: component_state.transition_next(),
                event_back_callback=lambda *args: component_state.transition_previous(),
                can_advance=component_state.can_transition(next=True),
                show=component_state.is_current_step(Marker.sel_gal3),
                state_view={
                    "total_galaxies": component_state.total_galaxies.value,
                    "selected_galaxy": bool(component_state.selected_galaxy.value),
                },
            )
            ScaffoldAlert(
                GUIDELINE_ROOT / "GuidelineSelectGalaxies4.vue",
                event_next_callback=lambda *args: component_state.transition_next(),
                event_back_callback=lambda *args: component_state.transition_previous(),
                can_advance=component_state.can_transition(next=True),
                show=component_state.is_current_step(Marker.sel_gal4),
            )

        with rv.Col(cols=8):
            # TODO: for some reason, if a component using `element` takes too
            #  long to load, it'll be inserted at the end of the page render.
            #  Wrapping in a card seems to alleviate this.
            with rv.Card(class_="pa-0 ma-0", elevation=0):
                selection_tool = SelectionTool.element(
                    table_layer_data=component_state.galaxy_data
                )

            def _define_selection_tool_callbacks():
                """Store a galaxy that has been clicked in the selection tool"""
                selection_tool_widget = solara.get_widget(selection_tool)
                selection_tool_widget.on_galaxy_selected = (
                    lambda gal: _on_galaxy_selected(gal)
                )
                selection_tool_widget.observe(
                    lambda gal: component_state.selected_galaxy.set(gal["new"]),
                    ["current_galaxy"],
                )

            solara.use_effect(_define_selection_tool_callbacks)

            def _update_selection_tool():
                """Whenever the step changes, check to see if we need to update
                the highlighting or show/hide the green dots."""
                selection_tool_widget = solara.get_widget(selection_tool)
                selection_tool_widget.show_galaxies(
                    component_state.is_current_step(Marker.sel_gal2)
                    or component_state.is_current_step(Marker.sel_gal3)
                )
                if component_state.is_current_step(
                    Marker.sel_gal2
                ) or component_state.is_current_step(Marker.sel_gal3):
                    selection_tool_widget.center_on_start_coordinates()
                selection_tool_widget.highlighted = component_state.is_current_step(
                    Marker.sel_gal2
                ) or component_state.is_current_step(Marker.sel_gal3)

            solara.use_effect(
                _update_selection_tool, [component_state.current_step.value]
            )

    with rv.Row():
        with rv.Col(cols=4):
            ScaffoldAlert(
                GUIDELINE_ROOT / "GuidelineNoticeGalaxyTable.vue",
                event_next_callback=lambda *args: component_state.transition_next(),
                can_advance=component_state.can_transition(next=True),
                show=component_state.is_current_step(Marker.not_gal_tab),
            )
            ScaffoldAlert(
                GUIDELINE_ROOT / "GuidelineChooseRow.vue",
                event_next_callback=lambda *args: component_state.transition_next(),
                event_back_callback=lambda *args: component_state.transition_previous(),
                can_advance=component_state.can_transition(next=True),
                show=component_state.is_current_step(Marker.cho_row1),
            )
            ScaffoldAlert(
                GUIDELINE_ROOT / "GuidelineDopplerCalc4.vue",
                event_next_callback=lambda *args: component_state.transition_next(),
                event_back_callback=lambda *args: component_state.transition_previous(),
                can_advance=component_state.can_transition(next=True),
                show=component_state.is_current_step(Marker.dop_cal4),
                state_view={
                    "lambda_obs": component_state.lambda_obs.value,
                    "lambda_rest": component_state.lambda_rest.value,
                    "failed_validation_4": component_state.doppler_calc_state.failed_validation_4.value,
                },
            )
            ScaffoldAlert(
                GUIDELINE_ROOT / "GuidelineCheckMeasurement.vue",
                event_next_callback=lambda *args: component_state.transition_next(),
                event_back_callback=lambda *args: component_state.transition_previous(),
                can_advance=component_state.can_transition(next=True),
                show=component_state.is_current_step(Marker.che_mea1),
            )

        with rv.Col(cols=8):
            if Marker.cho_row1.value <= component_state.current_step.value.value < Marker.rem_gal1.value:
                example_data_table = DataTable(
                    title="Example Galaxy",
                    headers=[
                        {
                            "text": "Galaxy Name",
                            "align": "start",
                            "sortable": False,
                            "value": "name",
                        },
                        {"text": "Element", "value": "element"},
                        {
                            "text": "&lambda;<sub>rest</sub> (&Aring;)",
                            "value": "rest_wave",
                        },
                        {
                            "text": "&lambda;<sub>obs</sub> (&Aring;)",
                            "value": "measured_wave",
                        },
                        {"text": "Velocity (km/s)", "value": "velocity"},
                    ],
                    items=example_data.dict(exclude={'measurements': {'__all__': 'spectrum'}})["measurements"],
                    highlighted=component_state.is_current_step(Marker.cho_row1),
                    event_on_row_selected=_on_example_galaxy_table_row_selected,
                )
            else:
                data_table = DataTable(
                    title="My Galaxies",
                    headers=[
                        {
                            "text": "Galaxy Name",
                            "align": "start",
                            "sortable": False,
                            "value": "name",
                        },
                        {"text": "Element", "value": "element"},
                        {
                            "text": "&lambda;<sub>rest</sub> (&Aring;)",
                            "value": "rest_wave",
                        },
                        {
                            "text": "&lambda;<sub>obs</sub> (&Aring;)",
                            "value": "measured_wave",
                        },
                        {"text": "Velocity (km/s)", "value": "velocity"},
                    ],
                    items=student_data.dict(exclude={'measurements': {'__all__': 'spectrum'}})["measurements"],
                    highlighted=component_state.is_current_step(Marker.not_gal_tab),
                    event_on_row_selected=_on_example_galaxy_table_row_selected,
                )

    with rv.Row():
        with rv.Col(cols=4):
            ScaffoldAlert(
                GUIDELINE_ROOT / "GuidelineSpectrum.vue",
                event_next_callback=lambda *args: component_state.transition_next(),
                event_back_callback=lambda *args: component_state.transition_previous(),
                can_advance=component_state.can_transition(next=True),
                show=component_state.is_current_step(Marker.mee_spe1),
                # or component_state.is_current_step(Marker.spe_tut1),
                state_view={
                    "spectrum_tutorial_opened": component_state.spectrum_tutorial_opened.value
                },
            )
            ScaffoldAlert(
                GUIDELINE_ROOT / "GuidelineRestwave.vue",
                event_next_callback=lambda *args: component_state.transition_next(),
                event_back_callback=lambda *args: component_state.transition_previous(),
                can_advance=component_state.can_transition(next=True),
                show=component_state.is_current_step(Marker.res_wav1),
                state_view={
                    "selected_example_galaxy": component_state.selected_example_galaxy.value,
                    "lambda_on": component_state.lambda_on.value,
                    "lambda_used": component_state.lambda_used.value,
                },
            )
            ScaffoldAlert(
                GUIDELINE_ROOT / "GuidelineObswave1.vue",
                event_next_callback=lambda *args: component_state.transition_next(),
                event_back_callback=lambda *args: component_state.transition_previous(),
                can_advance=component_state.can_transition(next=True),
                show=component_state.is_current_step(Marker.obs_wav1),
                state_view={
                    "selected_example_galaxy": component_state.selected_example_galaxy.value,
                },
            )
            ScaffoldAlert(
                GUIDELINE_ROOT / "GuidelineObswave2.vue",
                event_next_callback=lambda *args: component_state.transition_next(),
                event_back_callback=lambda *args: component_state.transition_previous(),
                can_advance=component_state.can_transition(next=True),
                show=component_state.is_current_step(Marker.obs_wav2),
                state_view={
                    "selected_example_galaxy": component_state.selected_example_galaxy.value,
                    "zoom_tool_activate": component_state.zoom_tool_activated.value,
                },
            )
            ScaffoldAlert(
                GUIDELINE_ROOT / "GuidelineDopplerCalc0.vue",
                event_next_callback=lambda *args: component_state.transition_next(),
                event_back_callback=lambda *args: component_state.transition_previous(),
                can_advance=component_state.can_transition(next=True),
                show=component_state.is_current_step(Marker.dop_cal0),
            )
            ScaffoldAlert(
                GUIDELINE_ROOT / "GuidelineDopplerCalc2.vue",
                event_next_callback=lambda *args: component_state.transition_next(),
                event_back_callback=lambda *args: component_state.transition_previous(),
                can_advance=component_state.can_transition(next=True),
                show=component_state.is_current_step(Marker.dop_cal2),
            )

        with rv.Col(cols=8):
            if component_state.current_step.value.value >= Marker.mee_spe1.value:
                spec_data = example_data.model_dump()["measurements"][0]["spectrum"]

                spectrum_viewer = SpectrumViewer(
                    Table(
                        {"wave": spec_data["wave"], "flux": spec_data["flux"]}
                    ).to_pandas(),
                    lambda_obs=component_state.lambda_obs,
                    spectrum_click_enabled=component_state.current_step.value.value >= Marker.obs_wav1.value,
                    on_lambda_clicked=lambda: component_state.lambda_used.set(True),
                    on_zoom_clicked=lambda: component_state.zoom_tool_activated.set(
                        True
                    ),
                    on_spectrum_clicked=lambda: component_state.spectrum_clicked.set(
                        True
                    ),
                )

    with rv.Row():
        with rv.Col(cols=4):
            pass

        with rv.Col(cols=8):
            if component_state.current_step.value.value >= Marker.mee_spe1.value:
                SpectrumSlideshow(
                    event_on_dialog_opened=lambda *args: component_state.spectrum_tutorial_opened.set(
                        True
                    )
                )

            component_state.doppler_calc_dialog.value = component_state.is_current_step(Marker.dop_cal5)

            DopplerSlideshow(
                dialog=component_state.doppler_calc_dialog.value,
                titles=component_state.doppler_calc_state.titles.value,
                step=component_state.doppler_calc_state.step.value,
                length=component_state.doppler_calc_state.length.value,
                lambda_obs=component_state.lambda_obs.value,
                lambda_rest=component_state.lambda_rest.value,
                max_step_completed_5=component_state.doppler_calc_state.max_step_completed_5.value,
                failed_validation_5=component_state.doppler_calc_state.failed_validation_5.value,
                interact_steps_5=component_state.doppler_calc_state.interact_steps_5.value,
                student_vel=component_state.student_vel.value,
                student_c=component_state.doppler_calc_state.student_c.value,
                event_set_student_vel_calc=lambda *args: component_state.doppler_calc_state.student_vel_calc.set(True),
                event_next_callback=lambda *args: component_state.transition_next()
            )
