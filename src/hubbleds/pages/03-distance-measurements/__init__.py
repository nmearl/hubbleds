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

from ...components import DataTable, AngsizeDosDontsSlideshow
from ...data_management import *
from ...state import GLOBAL_STATE, LOCAL_STATE, mc_callback
from ...utils import DISTANCE_CONSTANT
from ...widgets.selection_tool import SelectionTool
from ...data_models.student import student_data, StudentMeasurement, example_data
from .component_state import ComponentState, Marker


GUIDELINE_ROOT = Path(__file__).parent / "guidelines"

gjapp = JupyterApplication(GLOBAL_STATE.data_collection, GLOBAL_STATE.session)

component_state = ComponentState()


# def _on_galaxy_selected(galaxy):
#     is_in = np.isin(
#         [x.name for x in student_data.measurements], galaxy["name"]
#     )  # Avoid duplicates
#     already_present = is_in.size > 0 and is_in[0]

#     if not already_present:
#         student_data.measurements.append(StudentMeasurement(**galaxy))
#         component_state.total_galaxies.value += 1


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

    mc_scoring, set_mc_scoring  = solara.use_state(LOCAL_STATE.mc_scoring.value)

    solara.Text(
        f"Current step: {component_state.current_step.value.value}. {component_state.current_step.value}"
    )

    if (component_state.current_step.value.value < Marker.fil_rem1.value):
        solara.Text(
            f"Next step: {Marker(component_state.current_step.value.value + 1)} "
            f"Can advance: {component_state.can_transition(next=True)}"
        )
    else:
        solara.Text(
            "End of Stage"
        )

    # if LOCAL_STATE.debug_mode:

        # def _on_select_galaxies_clicked():
        #     gal_tab = Table(component_state.galaxy_data)
        #     gal_tab["id"] = [str(x) for x in gal_tab["id"]]
        #     for i in range(5 - component_state.total_galaxies.value):
        #         gal = dict(gal_tab[i])
        #         _on_galaxy_selected(gal)

        #     component_state.transition_to(Marker.sel_gal3, force=True)

        # solara.Button("Select 5 Galaxies", on_click=_on_select_galaxies_clicked)


    with solara.ColumnsResponsive(12, large=[4,8]):
        with rv.Col():
            ScaffoldAlert(
                GUIDELINE_ROOT / "GuidelineAngsizeMeas1.vue",
                event_next_callback=lambda *args: component_state.transition_next(),
                can_advance=component_state.can_transition(next=True),
                show=component_state.is_current_step(Marker.ang_siz1),
            )
            ScaffoldAlert(
                GUIDELINE_ROOT / "GuidelineAngsizeMeas2.vue",
                event_next_callback=lambda *args: component_state.transition_next(),
                event_back_callback=lambda *args: component_state.transition_previous(),
                can_advance=component_state.can_transition(next=True),
                show=component_state.is_current_step(Marker.ang_siz2),
            )
            ScaffoldAlert(
                GUIDELINE_ROOT / "GuidelineAngsizeMeas2b.vue",
                event_next_callback=lambda *args: component_state.transition_next(),
                event_back_callback=lambda *args: component_state.transition_previous(),
                can_advance=component_state.can_transition(next=True),
                show=component_state.is_current_step(Marker.ang_siz2b),
            )
            ScaffoldAlert(
                #FIX This will need to be wired up once measuring tool is implemented
                GUIDELINE_ROOT / "GuidelineAngsizeMeas3.vue",
                event_next_callback=lambda *args: component_state.transition_next(),
                event_back_callback=lambda *args: component_state.transition_previous(),
                can_advance=component_state.can_transition(next=True),
                show=component_state.is_current_step(Marker.ang_siz3),
            )
            ScaffoldAlert(
                #FIX This will need to be wired up once measuring tool is implemented
                GUIDELINE_ROOT / "GuidelineAngsizeMeas4.vue",
                event_next_callback=lambda *args: component_state.transition_next(),
                event_back_callback=lambda *args: component_state.transition_previous(),
                can_advance=component_state.can_transition(next=True),
                show=component_state.is_current_step(Marker.ang_siz4),
            )
            ScaffoldAlert(
                GUIDELINE_ROOT / "GuidelineAngsizeMeas5a.vue",
                event_next_callback=lambda *args: component_state.transition_next(),
                event_back_callback=lambda *args: component_state.transition_previous(),
                can_advance=component_state.can_transition(next=True),
                show=component_state.is_current_step(Marker.ang_siz5a),
                state_view={
                    "dosdonts_tutorial_opened": component_state.dosdonts_tutorial_opened.value
                },
            )
            # This was skipped in voila version
            # ScaffoldAlert(
            #     GUIDELINE_ROOT / "GuidelineAngsizeMeas6.vue",
            #     event_next_callback=lambda *args: component_state.transition_next(),
            #     event_back_callback=lambda *args: component_state.transition_previous(),
            #     can_advance=component_state.can_transition(next=True),
            #     show=component_state.is_current_step(Marker.ang_siz6),
            # )
            ScaffoldAlert(
                GUIDELINE_ROOT / "GuidelineDotplotSeq5.vue",
                event_next_callback=lambda *args: component_state.transition_next(),
                event_back_callback=lambda *args: component_state.transition_previous(),
                event_force_transition=lambda *args: component_state.transition_to(Marker.rep_rem1),
                can_advance=component_state.can_transition(next=True),
                show=component_state.is_current_step(Marker.dot_seq5),
            )
            ScaffoldAlert(
                #FIX This will need to be wired up once measuring tool is implemented
                GUIDELINE_ROOT / "GuidelineDotplotSeq5b.vue",
                event_next_callback=lambda *args: component_state.transition_next(),
                event_back_callback=lambda *args: component_state.transition_previous(),
                can_advance=component_state.can_transition(next=True),
                show=component_state.is_current_step(Marker.dot_seq5b),
            )

        with rv.Col():
            with rv.Col(cols=6, offset=3):
                if component_state.current_step.value.value >= Marker.ang_siz5a.value:
                    AngsizeDosDontsSlideshow(
                        event_on_dialog_opened=lambda *args: component_state.dosdonts_tutorial_opened.set(
                            True
                        )
                    )

    with solara.ColumnsResponsive(12, large=[4,8]):
        with rv.Col():
            ScaffoldAlert(
                #FIX This will need to be wired up once table is implemented
                GUIDELINE_ROOT / "GuidelineChooseRow1.vue",
                event_next_callback=lambda *args: component_state.transition_next(),
                event_back_callback=lambda *args: component_state.transition_previous(),
                can_advance=component_state.can_transition(next=True),
                show=component_state.is_current_step(Marker.cho_row1),
            )
            ScaffoldAlert(
                GUIDELINE_ROOT / "GuidelineAngsizeMeas5.vue",
                event_next_callback=lambda *args: component_state.transition_next(),
                event_back_callback=lambda *args: component_state.transition_previous(),
                can_advance=component_state.can_transition(next=True),
                show=component_state.is_current_step(Marker.ang_siz5),
            )
            ScaffoldAlert(
                GUIDELINE_ROOT / "GuidelineEstimateDistance1.vue",
                event_next_callback=lambda *args: component_state.transition_next(),
                event_back_callback=lambda *args: component_state.transition_previous(),
                can_advance=component_state.can_transition(next=True),
                show=component_state.is_current_step(Marker.est_dis1),
            )
            ScaffoldAlert(
                GUIDELINE_ROOT / "GuidelineEstimateDistance2.vue",
                event_next_callback=lambda *args: component_state.transition_next(),
                event_back_callback=lambda *args: component_state.transition_previous(),
                can_advance=component_state.can_transition(next=True),
                show=component_state.is_current_step(Marker.est_dis2),
                state_view={
                    "distance_const": DISTANCE_CONSTANT
                },
            )
            ScaffoldAlert(
                #FIX This will need to be wired up once table is implemented
                GUIDELINE_ROOT / "GuidelineChooseRow2.vue",
                event_next_callback=lambda *args: component_state.transition_next(),
                event_back_callback=lambda *args: component_state.transition_previous(),
                can_advance=component_state.can_transition(next=True),
                show=component_state.is_current_step(Marker.cho_row2),
            )
            ScaffoldAlert(
                #FIX This will need to be wired up once measuring tool is implemented
                GUIDELINE_ROOT / "GuidelineEstimateDistance3.vue",
                event_next_callback=lambda *args: component_state.transition_next(),
                event_back_callback=lambda *args: component_state.transition_previous(),
                can_advance=component_state.can_transition(next=True),
                show=component_state.is_current_step(Marker.est_dis3),
                state_view={
                    "distance_const": DISTANCE_CONSTANT,
                    "meas_theta": 10, #FIX to pass student's value once we hook up angular size measurements
                },
            )
            ScaffoldAlert(
                GUIDELINE_ROOT / "GuidelineEstimateDistance4.vue",
                event_next_callback=lambda *args: component_state.transition_next(),
                event_back_callback=lambda *args: component_state.transition_previous(),
                can_advance=component_state.can_transition(next=True),
                show=component_state.is_current_step(Marker.est_dis4),
                state_view={
                    "distance_const": DISTANCE_CONSTANT,
                    "meas_theta": 10, #FIX to pass student's value once we hook up angular size measurements
                },
            )
            ScaffoldAlert(
                #FIX This will need to be wired up once table is implemented
                GUIDELINE_ROOT / "GuidelineDotplotSeq5a.vue",
                event_next_callback=lambda *args: component_state.transition_next(),
                event_back_callback=lambda *args: component_state.transition_previous(),
                can_advance=component_state.can_transition(next=True),
                show=component_state.is_current_step(Marker.dot_seq5a),
            )
            ScaffoldAlert(
                GUIDELINE_ROOT / "GuidelineDotplotSeq5c.vue",
                event_next_callback=lambda *args: component_state.transition_next(),
                event_back_callback=lambda *args: component_state.transition_previous(),
                can_advance=component_state.can_transition(next=True),
                show=component_state.is_current_step(Marker.dot_seq5c),
            )
            ScaffoldAlert(
                GUIDELINE_ROOT / "GuidelineRepeatRemainingGalaxies.vue",
                event_next_callback=lambda *args: component_state.transition_next(),
                event_back_callback=lambda *args: component_state.transition_to(Marker.dot_seq5),
                can_advance=component_state.can_transition(next=True),
                show=component_state.is_current_step(Marker.rep_rem1),
            )
            ScaffoldAlert(
                GUIDELINE_ROOT / "GuidelineFillRemainingGalaxies.vue",
                # event_next_callback should go to next stage but I don't know how to set that up.
                event_back_callback=lambda *args: component_state.transition_previous(),
                show=component_state.is_current_step(Marker.fil_rem1),
            )

        with rv.Col():
            solara.Markdown("blah blah")

    with solara.ColumnsResponsive(12, large=[4,8]):
        with rv.Col():
            ScaffoldAlert(
                GUIDELINE_ROOT / "GuidelineDotplotSeq1.vue",
                event_next_callback=lambda *args: component_state.transition_next(),
                event_back_callback=lambda *args: component_state.transition_previous(),
                can_advance=component_state.can_transition(next=True),
                show=component_state.is_current_step(Marker.dot_seq1),
            )
            ScaffoldAlert(
                GUIDELINE_ROOT / "GuidelineDotplotSeq2.vue",
                event_next_callback=lambda *args: component_state.transition_next(),
                event_back_callback=lambda *args: component_state.transition_previous(),
                can_advance=component_state.can_transition(next=True),
                show=component_state.is_current_step(Marker.dot_seq2),
                event_mc_callback=lambda event: mc_callback(event = event, local_state = LOCAL_STATE, set_score=set_mc_scoring),
                state_view={'mc_score': mc_scoring.get('ang_meas_consensus'), 'score_tag': 'ang_meas_consensus'}
            )            
            ScaffoldAlert(
                GUIDELINE_ROOT / "GuidelineDotplotSeq3.vue",
                event_next_callback=lambda *args: component_state.transition_next(),
                event_back_callback=lambda *args: component_state.transition_previous(),
                can_advance=component_state.can_transition(next=True),
                show=component_state.is_current_step(Marker.dot_seq3),
            )
            ScaffoldAlert(
                GUIDELINE_ROOT / "GuidelineDotplotSeq4.vue",
                event_next_callback=lambda *args: component_state.transition_next(),
                event_back_callback=lambda *args: component_state.transition_previous(),
                can_advance=component_state.can_transition(next=True),
                show=component_state.is_current_step(Marker.dot_seq4),
            )
            ScaffoldAlert(
                GUIDELINE_ROOT / "GuidelineDotplotSeq4a.vue",
                event_next_callback=lambda *args: component_state.transition_next(),
                event_back_callback=lambda *args: component_state.transition_previous(),
                can_advance=component_state.can_transition(next=True),
                show=component_state.is_current_step(Marker.dot_seq4a),
                event_mc_callback=lambda event: mc_callback(event = event, local_state = LOCAL_STATE, set_score=set_mc_scoring),
                state_view={'mc_score': mc_scoring.get('ang_meas_dist_relation'), 'score_tag': 'ang_meas_dist_relation'}
            )
            ScaffoldAlert(
                GUIDELINE_ROOT / "GuidelineDotplotSeq6.vue",
                event_next_callback=lambda *args: component_state.transition_next(),
                event_back_callback=lambda *args: component_state.transition_previous(),
                can_advance=component_state.can_transition(next=True),
                show=component_state.is_current_step(Marker.dot_seq6),
                event_mc_callback=lambda event: mc_callback(event = event, local_state = LOCAL_STATE, set_score=set_mc_scoring),
                state_view={'mc_score': mc_scoring.get('ang_meas_consensus_2'), 'score_tag': 'ang_meas_consensus_2'}
            )
            ScaffoldAlert(
                GUIDELINE_ROOT / "GuidelineDotplotSeq7.vue",
                event_next_callback=lambda *args: component_state.transition_next(),
                event_back_callback=lambda *args: component_state.transition_previous(),
                can_advance=component_state.can_transition(next=True),
                show=component_state.is_current_step(Marker.dot_seq7),
            )


        with rv.Col():
            solara.Markdown("blah blah")



