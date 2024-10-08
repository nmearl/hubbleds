import solara
from hubbleds.state import LOCAL_STATE, GLOBAL_STATE, get_multiple_choice, mc_callback
from .component_state import COMPONENT_STATE, Marker
from hubbleds.remote import LOCAL_API
from glue_jupyter import JupyterApplication
import asyncio
from pathlib import Path
from cosmicds.components import ScaffoldAlert, StateEditor
import reacton.ipyvuetify as rv
from hubbleds.base_component_state import (
    transition_to,
    transition_previous,
    transition_next,
)
from hubbleds.components import (
    SelectionTool,
    DataTable,
    DopplerSlideshow,
    SpectrumViewer,
    SpectrumSlideshow,
    DotplotViewer,
    ReflectVelocitySlideshow,
    DotplotTutorialSlideshow,
)
from hubbleds.state import GalaxyData, StudentMeasurement

# from solara.lab import Ref
from solara.toestand import Ref
from cosmicds.logger import setup_logger
from ...data_management import (
    EXAMPLE_GALAXY_SEED_DATA,
    DB_VELOCITY_FIELD,
    EXAMPLE_GALAXY_MEASUREMENTS,
    DB_MEASWAVE_FIELD,
)
import numpy as np
from glue.core import Data
from hubbleds.utils import models_to_glue_data, velocity_from_wavelengths, v2w, w2v, sync_reactives

logger = setup_logger("STAGE")

GUIDELINE_ROOT = Path(__file__).parent / "guidelines"


@solara.lab.computed
def selected_example_measurement():
    return LOCAL_STATE.value.get_example_measurement(
        COMPONENT_STATE.value.selected_example_galaxy
    )


@solara.lab.computed
def selected_measurement():
    return LOCAL_STATE.value.get_measurement(COMPONENT_STATE.value.selected_galaxy)

def is_wavelength_poorly_measured(measwave, restwave, z, tolerance = 0.5):
    z_meas =  (measwave - restwave) / restwave
    fractional_difference = (((z_meas - z) / z)** 2)**0.5
    return fractional_difference > tolerance

@solara.component
def Page():
    loaded_component_state = solara.use_reactive(False)
    router = solara.use_router()

    async def _load_component_state():
        # Load stored component state from database, measurement data is
        #   considered higher-level and is loaded when the story starts.
        LOCAL_API.get_stage_state(GLOBAL_STATE, LOCAL_STATE, COMPONENT_STATE)

        total_galaxies = Ref(COMPONENT_STATE.fields.total_galaxies)

        if len(LOCAL_STATE.value.measurements) != total_galaxies.value:
            logger.error(
                "Detected mismatch between stored measurements and current "
                "recorded number of galaxies."
            )
            total_galaxies.set(len(LOCAL_STATE.value.measurements))

        logger.info("Finished loading component state.")
        loaded_component_state.set(True)

    solara.lab.use_task(_load_component_state)
    # solara.use_memo(_load_component_state)

    async def _write_component_state():
        if not loaded_component_state.value:
            return

        # Listen for changes in the states and write them to the database
        LOCAL_API.put_stage_state(GLOBAL_STATE, LOCAL_STATE, COMPONENT_STATE)

        logger.info("Wrote component state to database.")

    solara.lab.use_task(_write_component_state, dependencies=[COMPONENT_STATE.value])

    def _glue_setup() -> JupyterApplication:
        # NOTE: use_memo has to be part of the main page render. Including it
        #  in a conditional will result in an error.
        gjapp = JupyterApplication(
            GLOBAL_STATE.value.glue_data_collection, GLOBAL_STATE.value.glue_session
        )

        if EXAMPLE_GALAXY_SEED_DATA not in gjapp.data_collection:
            example_seed_data = LOCAL_API.get_example_seed_measurement(LOCAL_STATE, which='first')
            data = Data(
                label=EXAMPLE_GALAXY_SEED_DATA,
                **{
                    k: np.asarray([r[k] for r in example_seed_data])
                    for k in example_seed_data[0].keys()
                }
            )
            gjapp.data_collection.append(data)
        else:
            data = gjapp.data_collection[EXAMPLE_GALAXY_SEED_DATA]
        return gjapp

    gjapp = solara.use_memo(_glue_setup)

    def _state_callback_setup():
        # We want to minize duplicate state handling, but also keep the states
        #  independent. We'll set up observers for changes here so that they
        #  automatically keep the states in sync.
        measurements = Ref(LOCAL_STATE.fields.measurements)
        total_galaxies = Ref(COMPONENT_STATE.fields.total_galaxies)
        measurements.subscribe_change(
            lambda *args: total_galaxies.set(len(measurements.value))
        )

    solara.use_memo(_state_callback_setup)

    # Load selected galaxy spectrum data in the background to avoid hitched
    #  in the front-end user experience.
    async def _load_example_spectrum():
        if selected_example_measurement.value is None:
            return False

        return selected_example_measurement.value.galaxy.spectrum_as_data_frame

    example_spec_data_task = solara.lab.use_task(
        _load_example_spectrum,
        dependencies=[COMPONENT_STATE.value.selected_example_galaxy],
    )

    async def _load_spectrum():
        if selected_measurement.value is None:
            return False

        return selected_measurement.value.galaxy.spectrum_as_data_frame

    spec_data_task = solara.lab.use_task(
        _load_spectrum,
        dependencies=[COMPONENT_STATE.value.selected_galaxy],
    )
    
    def add_link(from_dc_name, from_att, to_dc_name, to_att):
        if isinstance(from_dc_name, Data):
            from_dc = from_dc_name
        else:
            from_dc = gjapp.data_collection[from_dc_name]

        if isinstance(to_dc_name, Data):
            to_dc = to_dc_name
        else:
            to_dc = gjapp.data_collection[to_dc_name]
        gjapp.add_link(from_dc, from_att, to_dc, to_att)
    

    def add_example_measurements_to_glue():
        print('in add_example_measurements_to_glue')
        if len(LOCAL_STATE.value.example_measurements) > 0:
            print('has example measurements')
            example_measurements_glue = models_to_glue_data(
                LOCAL_STATE.value.example_measurements,
                label=EXAMPLE_GALAXY_MEASUREMENTS,
            )
            example_measurements_glue.style.color = "red"
            if EXAMPLE_GALAXY_MEASUREMENTS in gjapp.data_collection:
                existing = gjapp.data_collection[EXAMPLE_GALAXY_MEASUREMENTS]
                existing.update_values_from_data(example_measurements_glue)
                use_this = existing
            else:
                gjapp.data_collection.append(example_measurements_glue)
                use_this = gjapp.data_collection[EXAMPLE_GALAXY_MEASUREMENTS]
            use_this.style.color = "red"
    
            egsd = gjapp.data_collection[EXAMPLE_GALAXY_SEED_DATA]
            add_link(
                egsd,
                DB_VELOCITY_FIELD,
                use_this,
                "velocity_value",
            )
            add_link(
                egsd,
                DB_MEASWAVE_FIELD,
                use_this,
                "obs_wave_value",
            )

    add_example_measurements_to_glue()


    # Flag to show/hide the selection tool. TODO: we shouldn't need to be
    #   doing this here; revisit in the future and implement proper handling
    #   in the ipywwt package itself.
    show_selection_tool, set_show_selection_tool = solara.use_state(False)

    async def _delay_selection_tool():
        await asyncio.sleep(3)
        set_show_selection_tool(True)

    solara.lab.use_task(_delay_selection_tool)

    def _fill_galaxies():
        dummy_measurements = LOCAL_API.get_dummy_data()
        measurements = []
        for measurement in dummy_measurements:
            measurements.append(StudentMeasurement(student_id=GLOBAL_STATE.value.student.id,
                                                   galaxy=measurement.galaxy,
                                                   obs_wave_value=measurement.obs_wave_value,
                                                   velocity_value=measurement.velocity_value,
                                                   ang_size_value=measurement.ang_size_value,
                                                   est_dist_value=measurement.est_dist_value))
        Ref(LOCAL_STATE.fields.measurements).set(measurements)

    def _fill_lambdas():
        dummy_measurements = LOCAL_API.get_dummy_data()
        measurements = []
        for measurement in dummy_measurements:
            measurements.append(StudentMeasurement(student_id=GLOBAL_STATE.value.student.id,
                                                   obs_wave_value=measurement.obs_wave_value,
                                                   galaxy=measurement.galaxy))
        Ref(LOCAL_STATE.fields.measurements).set(measurements)

    def _fill_stage1_go_stage3():
        dummy_measurements = LOCAL_API.get_dummy_data()
        measurements = []
        for measurement in dummy_measurements:
            measurements.append(StudentMeasurement(student_id=GLOBAL_STATE.value.student.id,
                                                   obs_wave_value=measurement.obs_wave_value,
                                                   galaxy=measurement.galaxy,
                                                   velocity_value=measurement.velocity_value))
        Ref(LOCAL_STATE.fields.measurements).set(measurements)
        router.push("03-distance-measurements")

    def _select_random_galaxies():
        need = 5 - len(LOCAL_STATE.value.measurements)
        if need <= 0:
            return
        galaxies = LOCAL_API.get_galaxies(LOCAL_STATE)
        sample = np.random.choice(galaxies, size=need, replace=False)
        new_measurements = [StudentMeasurement(student_id=GLOBAL_STATE.value.student.id,
                                               galaxy=galaxy)
                             for galaxy in sample]
        measurements = LOCAL_STATE.value.measurements + new_measurements
        Ref(LOCAL_STATE.fields.measurements).set(measurements)
    
    def num_bad_velocities():
        measurements = Ref(LOCAL_STATE.fields.measurements)
        num = 0
        for meas in measurements.value:
            if meas.obs_wave_value is None or meas.rest_wave_value is None:
                # Skip measurements with missing data cuz they have not been attempted
                continue
            elif is_wavelength_poorly_measured(meas.obs_wave_value, meas.rest_wave_value, meas.galaxy.z):
                num += 1
        
        has_multiple_bad_velocities = Ref(COMPONENT_STATE.fields.has_multiple_bad_velocities)
        has_multiple_bad_velocities.set(num > 1)
        return num
    
    def set_obs_wave_total():
        obs_wave_total = Ref(COMPONENT_STATE.fields.obs_wave_total)
        measurements = LOCAL_STATE.value.measurements
        num = 0
        for meas in measurements:
            print(meas)
            if meas.obs_wave_value is not None:
                num += 1
        obs_wave_total.set(num)
    
    sync_wavelength_line = solara.use_reactive(6565.0)
    sync_velocity_line = solara.use_reactive(8000.0)
    spectrum_bounds = solara.use_reactive([])
    dotplot_bounds = solara.use_reactive([])
    max_spectrum_bounds = solara.use_reactive([])
    ## ----- Make sure we are initialized in the correct state ----- ##
    def sync_example_velocity_to_wavelength(velocity):
        print('====================', velocity)
        if len(LOCAL_STATE.value.example_measurements) > 0:
            lambda_rest = LOCAL_STATE.value.example_measurements[0].rest_wave_value
            lambda_obs = v2w(velocity, lambda_rest)
            print('lambda_obs:', lambda_obs)
            return lambda_obs
    
    def sync_example_wavelength_to_velocity(wavelength):
        print('====================', wavelength)
        if len(LOCAL_STATE.value.example_measurements) > 0:
            lambda_rest = LOCAL_STATE.value.example_measurements[0].rest_wave_value
            velocity = w2v(wavelength, lambda_rest)
            print('velocity:', velocity)
            return velocity
    
    def sync_spectrum_to_dotplot_range(value):
        print('sync_spectrum_to_dotplot_range')
        lambda_rest = LOCAL_STATE.value.example_measurements[0].rest_wave_value
        return [w2v(v, lambda_rest) for v in value]
    
    def sync_dotplot_to_spectrum_range(value):
        print('sync_dotplot_to_spectrum_range')
        lambda_rest = LOCAL_STATE.value.example_measurements[0].rest_wave_value
        return [v2w(v, lambda_rest) for v in value]
            
    def _initialize_state(isloaded):
        if (not isloaded):
            return
        
        if COMPONENT_STATE.value.current_step == Marker.sel_gal2:
            if COMPONENT_STATE.value.total_galaxies == 5:
                transition_to(COMPONENT_STATE, Marker.sel_gal3, force=True)
        
        if Marker.is_at_or_after(COMPONENT_STATE.value.current_step, Marker.cho_row1):
            COMPONENT_STATE.value.selected_example_galaxy = 1576 # id of the first example galaxy
        
        if (len(LOCAL_STATE.value.example_measurements) > 0):
            meas = LOCAL_STATE.value.example_measurements[0].rest_wave_value
            sync_wavelength_line.set(meas)
            new_vel = sync_example_wavelength_to_velocity(meas)
            if new_vel:
                sync_velocity_line.set(new_vel)
    
    loaded_component_state.subscribe(_initialize_state)
    
    def _sync_setup():
        sync_reactives(
            sync_wavelength_line, sync_velocity_line,
            sync_example_wavelength_to_velocity, sync_example_velocity_to_wavelength
        )

        sync_reactives(
            spectrum_bounds, dotplot_bounds,
            sync_spectrum_to_dotplot_range, sync_dotplot_to_spectrum_range
        )
    
    solara.use_memo(_sync_setup)
    
    @solara.lab.computed
    def dotplot_reset_bounds():
        return [sync_example_wavelength_to_velocity(w) for w in max_spectrum_bounds.value] #type: ignore
    
    def print_selected_galaxy(galaxy):
        print('selected galaxy is now:', galaxy)
    Ref(COMPONENT_STATE.fields.selected_galaxy).subscribe(print_selected_galaxy)

    def print_selected_example_galaxy(galaxy):
        print('selected example galaxy is now:', galaxy)
    Ref(COMPONENT_STATE.fields.selected_example_galaxy).subscribe(print_selected_example_galaxy)
    
    speech = Ref(GLOBAL_STATE.fields.speech)
    
    with solara.Row():
        with solara.Column():
            StateEditor(Marker, COMPONENT_STATE, LOCAL_STATE, LOCAL_API, show_all=True)
        with solara.Column():
            solara.Button(label="Fill default vel & dist measurements", on_click=_fill_galaxies)
            solara.Button(label="Choose 5 random galaxies", on_click=_select_random_galaxies)

    with rv.Row():
        with rv.Col(cols=4):
            ScaffoldAlert(
                GUIDELINE_ROOT / "GuidelineIntro.vue",
                event_next_callback=lambda _: transition_next(COMPONENT_STATE),
                can_advance=COMPONENT_STATE.value.can_transition(next=True),
                show=COMPONENT_STATE.value.is_current_step(Marker.mee_gui1),
                speech=speech.value,
            )
            ScaffoldAlert(
                GUIDELINE_ROOT / "GuidelineSelectGalaxies1.vue",
                event_next_callback=lambda _: transition_next(COMPONENT_STATE),
                event_back_callback=lambda _: transition_previous(COMPONENT_STATE),
                can_advance=COMPONENT_STATE.value.can_transition(next=True),
                show=COMPONENT_STATE.value.is_current_step(Marker.sel_gal1),
                speech=speech.value,
            )
            ScaffoldAlert(
                GUIDELINE_ROOT / "GuidelineSelectGalaxies2.vue",
                event_next_callback=lambda _: transition_next(COMPONENT_STATE),
                event_back_callback=lambda _: transition_previous(COMPONENT_STATE),
                can_advance=COMPONENT_STATE.value.can_transition(next=True),
                show=COMPONENT_STATE.value.is_current_step(Marker.sel_gal2),
                state_view={
                    "total_galaxies": COMPONENT_STATE.value.total_galaxies,
                    "selected_galaxy": bool(COMPONENT_STATE.value.selected_galaxy),
                },
                speech=speech.value,
            )
            ScaffoldAlert(
                GUIDELINE_ROOT / "GuidelineSelectGalaxies3.vue",
                event_next_callback=lambda _: transition_next(COMPONENT_STATE),
                event_back_callback=lambda _: transition_previous(COMPONENT_STATE),
                can_advance=COMPONENT_STATE.value.can_transition(next=True),
                show=COMPONENT_STATE.value.is_current_step(Marker.sel_gal3),
                state_view={
                    "total_galaxies": COMPONENT_STATE.value.total_galaxies,
                    "selected_galaxy": bool(COMPONENT_STATE.value.selected_galaxy),
                },
                speech=speech.value,
            )
            ScaffoldAlert(
                GUIDELINE_ROOT / "GuidelineSelectGalaxies4.vue",
                event_next_callback=lambda _: transition_next(COMPONENT_STATE),
                event_back_callback=lambda _: transition_previous(COMPONENT_STATE),
                can_advance=COMPONENT_STATE.value.can_transition(next=True),
                show=COMPONENT_STATE.value.is_current_step(Marker.sel_gal4),
                speech=speech.value,
            )

        with rv.Col(cols=8):
            
            show_snackbar = Ref(LOCAL_STATE.fields.show_snackbar)
            async def snackbar_off(value = None):
                if show_snackbar.value:
                    await asyncio.sleep(3)
                    show_snackbar.set(False)
            solara.lab.use_task(snackbar_off, dependencies=[show_snackbar])
            
            def _galaxy_added_callback(galaxy_data: GalaxyData):
                already_exists = galaxy_data.id in [
                    x.galaxy_id for x in LOCAL_STATE.value.measurements
                ]

                if already_exists:
                    return

                if len(LOCAL_STATE.value.measurements) == 5:
                    show_snackbar = Ref(LOCAL_STATE.fields.show_snackbar)
                    snackbar_message = Ref(LOCAL_STATE.fields.snackbar_message)

                    show_snackbar.set(True)
                    snackbar_message.set(
                        "You've already selected 5 galaxies. Continue forth!"
                    )
                    logger.info("Attempted to add more than 5 galaxies.")
                    return

                logger.info("Adding galaxy `%s` to measurements.", galaxy_data.id)

                measurements = Ref(LOCAL_STATE.fields.measurements)

                measurements.set(
                    measurements.value
                    + [
                        StudentMeasurement(
                            student_id=GLOBAL_STATE.value.student.id,
                            galaxy=galaxy_data,
                        )
                    ]
                )
                
                
            total_galaxies = Ref(COMPONENT_STATE.fields.total_galaxies)
            def advance_on_total_galaxies(value):
                if COMPONENT_STATE.value.current_step == Marker.sel_gal2:
                    if value == 1:
                        transition_to(COMPONENT_STATE, Marker.sel_gal3)
            total_galaxies.subscribe(advance_on_total_galaxies)

            def _galaxy_selected_callback(galaxy_data: GalaxyData | None):
                if galaxy_data is None:
                    return

                selected_galaxy = Ref(COMPONENT_STATE.fields.selected_galaxy)
                selected_galaxy.set(galaxy_data.id)
            

            show_example_data_table = COMPONENT_STATE.value.current_step_between(
            Marker.cho_row1, Marker.dot_seq12
            )
            if show_example_data_table:
                selection_tool_galaxy = selected_example_measurement
            else:
                selection_tool_galaxy= selected_measurement
            
            SelectionTool(
                show_galaxies=COMPONENT_STATE.value.current_step_in(
                    [Marker.sel_gal2, Marker.not_gal_tab, Marker.sel_gal3]
                ),
                galaxy_selected_callback=_galaxy_selected_callback,
                galaxy_added_callback=_galaxy_added_callback,
                selected_measurement=(
                    selection_tool_galaxy.value.dict()
                    if selection_tool_galaxy.value is not None
                    else None
                ),
            )
            
            if show_snackbar.value:
                solara.Info(label=LOCAL_STATE.value.snackbar_message)        

    with rv.Row():
        with rv.Col(cols=4):
            ScaffoldAlert(
                GUIDELINE_ROOT / "GuidelineNoticeGalaxyTable.vue",
                event_next_callback=lambda _: transition_next(COMPONENT_STATE),
                event_back_callback=lambda _: transition_previous(COMPONENT_STATE),
                can_advance=COMPONENT_STATE.value.can_transition(next=True),
                show=COMPONENT_STATE.value.is_current_step(Marker.not_gal_tab),
                speech=speech.value,
            )
            ScaffoldAlert(
                GUIDELINE_ROOT / "GuidelineChooseRow.vue",
                event_next_callback=lambda _: transition_next(COMPONENT_STATE),
                event_back_callback=lambda _: transition_previous(COMPONENT_STATE),
                can_advance=COMPONENT_STATE.value.can_transition(next=True),
                show=COMPONENT_STATE.value.is_current_step(Marker.cho_row1),
                speech=speech.value,
            )

            def _on_validated_transition(validated):
                if validated:
                    transition_next(COMPONENT_STATE)

                show_doppler_dialog = Ref(COMPONENT_STATE.fields.show_doppler_dialog)
                show_doppler_dialog.set(validated)

            validation_4_failed = Ref(
                COMPONENT_STATE.fields.doppler_state.validation_4_failed
            )
            ScaffoldAlert(
                GUIDELINE_ROOT / "GuidelineDopplerCalc4.vue",
                event_next_callback=lambda _: transition_next(COMPONENT_STATE),
                event_back_callback=lambda _: transition_previous(COMPONENT_STATE),
                can_advance=COMPONENT_STATE.value.can_transition(next=True),
                show=COMPONENT_STATE.value.current_step_in(
                    [Marker.dop_cal4, Marker.dop_cal5]
                ),
                state_view={
                    "lambda_obs": COMPONENT_STATE.value.obs_wave,
                    "lambda_rest": (
                        selected_example_measurement.value.rest_wave_value
                        if selected_example_measurement.value is not None
                        else None
                    ),
                    "failed_validation_4": validation_4_failed.value,
                },
                event_failed_validation_4_callback=validation_4_failed.set,
                event_on_validated_transition=_on_validated_transition,
                speech=speech.value,
            )
            ScaffoldAlert(
                GUIDELINE_ROOT / "GuidelineCheckMeasurement.vue",
                event_next_callback=lambda _: transition_next(COMPONENT_STATE),
                event_back_callback=lambda _: transition_previous(COMPONENT_STATE),
                can_advance=COMPONENT_STATE.value.can_transition(next=True),
                show=COMPONENT_STATE.value.is_current_step(Marker.che_mea1),
                speech=speech.value,
            )
            ScaffoldAlert(
                GUIDELINE_ROOT / "GuidelineDotSequence12.vue",
                event_next_callback=lambda _: transition_next(COMPONENT_STATE),
                event_back_callback=lambda _: transition_previous(COMPONENT_STATE),
                can_advance=COMPONENT_STATE.value.can_transition(next=True),
                show=COMPONENT_STATE.value.is_current_step(Marker.dot_seq12),
                speech=speech.value,
                # event_remeasure_example_galaxy=lambda _: transition_to(
                #     COMPONENT_STATE, Marker.dot_seq13, force=True
                # ),
                # event_continue_to_galaxies=lambda _: transition_to(
                #     COMPONENT_STATE, Marker.rem_gal1, force=True
                # ),
            )
            # Skip for now since we aren't offering 2nd measurement.
            # ScaffoldAlert(
            #     GUIDELINE_ROOT / "GuidelineDotSequence13.vue",
            #     event_next_callback=lambda _: transition_next(COMPONENT_STATE),
            #     event_back_callback=lambda _: transition_previous(COMPONENT_STATE),
            #     can_advance=COMPONENT_STATE.value.can_transition(next=True),
            #     show=COMPONENT_STATE.value.is_current_step(Marker.dot_seq13),
            # )
            set_obs_wave_total()
            ScaffoldAlert(
                GUIDELINE_ROOT / "GuidelineRemainingGals.vue",
                event_next_callback=lambda _: transition_next(COMPONENT_STATE),
                event_back_callback=lambda _: transition_previous(COMPONENT_STATE),
                can_advance=COMPONENT_STATE.value.can_transition(next=True),
                show=COMPONENT_STATE.value.is_current_step(Marker.rem_gal1),
                state_view={
                    "obswaves_total": COMPONENT_STATE.value.obs_wave_total,
                    "has_bad_velocities": COMPONENT_STATE.value.has_bad_velocities,
                    "has_multiple_bad_velocities": COMPONENT_STATE.value.has_multiple_bad_velocities,
                    "selected_galaxy": (
                        selected_measurement.value.dict()
                        if selected_measurement.value is not None
                        else None
                    ),
                },
                speech=speech.value,
            )
            # if COMPONENT_STATE.value.is_current_step(Marker.rem_gal1):
            #     solara.Button(label="Shortcut: Fill Wavelength Measurements", on_click=_fill_lambdas)
            ScaffoldAlert(
                GUIDELINE_ROOT / "GuidelineDopplerCalc6.vue",
                event_next_callback=lambda _: transition_next(COMPONENT_STATE),
                event_back_callback=lambda _: transition_previous(COMPONENT_STATE),
                can_advance=COMPONENT_STATE.value.can_transition(next=True),
                show=COMPONENT_STATE.value.is_current_step(Marker.dop_cal6),
                speech=speech.value,
            )
            ScaffoldAlert(
                GUIDELINE_ROOT / "GuidelineReflectVelValues.vue",
                event_next_callback=lambda _: transition_next(COMPONENT_STATE),
                event_back_callback=lambda _: transition_previous(COMPONENT_STATE),
                can_advance=COMPONENT_STATE.value.can_transition(next=True),
                event_mc_callback=lambda event: mc_callback(event, LOCAL_STATE),
                show=COMPONENT_STATE.value.is_current_step(Marker.ref_vel1),
                state_view={'mc_score': get_multiple_choice(LOCAL_STATE, "reflect_vel_value"), 'score_tag': 'reflect_vel_value'},
                speech=speech.value,
            )
            ScaffoldAlert(
                GUIDELINE_ROOT / "GuidelineEndStage1.vue",
                event_next_callback=lambda _: router.push("02-distance-introduction"),
                event_back_callback=lambda _: transition_previous(COMPONENT_STATE),
                can_advance=COMPONENT_STATE.value.can_transition(next=True),
                show=COMPONENT_STATE.value.is_current_step(Marker.end_sta1),
                state_view={
                    "has_bad_velocities": COMPONENT_STATE.value.has_bad_velocities,
                    "has_multiple_bad_velocities": COMPONENT_STATE.value.has_multiple_bad_velocities,
                },
                speech=speech.value,
            )

        with rv.Col(cols=8):
            show_example_data_table = COMPONENT_STATE.value.current_step_between(
                Marker.cho_row1, Marker.dot_seq12 # TODO: change this back to dot_seq14 if we put back 2nd galaxy measurement
            )

            if show_example_data_table:
                selected_example_galaxy = Ref(
                    COMPONENT_STATE.fields.selected_example_galaxy
                )
                
                DataTable(
                    title="Example Galaxy",
                    items=[x.dict() for x in LOCAL_STATE.value.example_measurements],
                    show_select=COMPONENT_STATE.value.current_step_at_or_after(
                        Marker.cho_row1
                    ),
                    event_on_row_selected=lambda row: selected_example_galaxy.set(
                        LOCAL_STATE.value.get_example_measurement(
                            row["item"]["galaxy_id"]
                        ).galaxy_id
                    ),
                )
            else:
                selected_galaxy = Ref(COMPONENT_STATE.fields.selected_galaxy)

                def _on_table_row_selected(row):
                    galaxy_measurement = LOCAL_STATE.value.get_measurement(
                        row["item"]["galaxy_id"]
                    )
                    if galaxy_measurement is not None:
                        selected_galaxy.set(galaxy_measurement.galaxy_id)

                    obs_wave = Ref(COMPONENT_STATE.fields.obs_wave)
                    obs_wave.set(0)

                def _on_calculate_velocity():
                    for i in range(len(LOCAL_STATE.value.measurements)):
                        measurement = Ref(LOCAL_STATE.fields.measurements[i])
                        velocity = round(
                            3e5
                            * (
                                measurement.value.obs_wave_value
                                / measurement.value.rest_wave_value
                                - 1
                            )
                        )
                        measurement.set(
                            measurement.value.model_copy(
                                update={"velocity_value": velocity}
                            )
                        )

                        velocities_total = Ref(COMPONENT_STATE.fields.velocities_total)
                        velocities_total.set(velocities_total.value + 1)

                DataTable(
                    title="My Galaxies",
                    items=[x.dict() for x in LOCAL_STATE.value.measurements],
                    show_select=COMPONENT_STATE.value.current_step_at_or_after(
                        Marker.cho_row1
                    ),
                    button_icon="mdi-run-fast",
                    show_button=COMPONENT_STATE.value.is_current_step(
                        Marker.dop_cal6
                    ),
                    event_on_row_selected=_on_table_row_selected,
                    event_on_button_pressed=lambda _: _on_calculate_velocity(),
                )

    with rv.Row():
        with rv.Col(cols=4):
            ScaffoldAlert(
                GUIDELINE_ROOT / "GuidelineIntroDotplot.vue",
                event_next_callback=lambda _: transition_next(COMPONENT_STATE),
                event_back_callback=lambda _: transition_previous(COMPONENT_STATE),
                can_advance=COMPONENT_STATE.value.can_transition(next=True),
                show=COMPONENT_STATE.value.is_current_step(Marker.int_dot1),
                speech=speech.value,
            )
            ScaffoldAlert(
                GUIDELINE_ROOT / "GuidelineDotSequence01.vue",
                event_next_callback=lambda _: transition_next(COMPONENT_STATE),
                event_back_callback=lambda _: transition_previous(COMPONENT_STATE),
                can_advance=COMPONENT_STATE.value.can_transition(next=True),
                show=COMPONENT_STATE.value.is_current_step(Marker.dot_seq1),
                speech=speech.value,
            )
            ScaffoldAlert(
                GUIDELINE_ROOT / "GuidelineDotSequence02.vue",
                event_next_callback=lambda _: transition_next(COMPONENT_STATE),
                event_back_callback=lambda _: transition_previous(COMPONENT_STATE),
                can_advance=COMPONENT_STATE.value.can_transition(next=True),
                show=COMPONENT_STATE.value.is_current_step(Marker.dot_seq2),
                speech=speech.value,
            )
            # ScaffoldAlert(
            #     GUIDELINE_ROOT / "GuidelineDotSequence03.vue",
            #     event_next_callback=lambda _: transition_next(COMPONENT_STATE),
            #     event_back_callback=lambda _: transition_previous(COMPONENT_STATE),
            #     can_advance=COMPONENT_STATE.value.can_transition(next=True),
            #     show=COMPONENT_STATE.value.is_current_step(Marker.dot_seq3),
            # )
            # ScaffoldAlert(
            #     GUIDELINE_ROOT / "GuidelineDotSequence05.vue",
            #     event_next_callback=lambda _: transition_next(COMPONENT_STATE),
            #     event_back_callback=lambda _: transition_previous(COMPONENT_STATE),
            #     can_advance=COMPONENT_STATE.value.can_transition(next=True),
            #     show=COMPONENT_STATE.value.is_current_step(Marker.dot_seq5),
            # )
            ScaffoldAlert(
                GUIDELINE_ROOT / "GuidelineDotSequence06.vue",
                event_next_callback=lambda _: transition_next(COMPONENT_STATE),
                event_back_callback=lambda _: transition_previous(COMPONENT_STATE),
                can_advance=COMPONENT_STATE.value.can_transition(next=True),
                show=COMPONENT_STATE.value.is_current_step(Marker.dot_seq6),
                speech=speech.value,
            )
            ScaffoldAlert(
                GUIDELINE_ROOT / "GuidelineDotSequence07.vue",
                event_next_callback=lambda _: transition_next(COMPONENT_STATE),
                event_back_callback=lambda _: transition_previous(COMPONENT_STATE),
                can_advance=COMPONENT_STATE.value.can_transition(next=True),
                show=COMPONENT_STATE.value.is_current_step(Marker.dot_seq7),
                speech=speech.value,
            )
            ScaffoldAlert(
                GUIDELINE_ROOT / "GuidelineDotSequence08.vue",
                event_next_callback=lambda _: transition_next(COMPONENT_STATE),
                event_back_callback=lambda _: transition_previous(COMPONENT_STATE),
                can_advance=COMPONENT_STATE.value.can_transition(next=True),
                event_mc_callback=lambda event: mc_callback(event, LOCAL_STATE),
                show=COMPONENT_STATE.value.is_current_step(Marker.dot_seq8),
                state_view={
                    "mc_score": get_multiple_choice(LOCAL_STATE, "vel_meas_consensus"),
                    "score_tag": "vel_meas_consensus",
                },
                speech=speech.value,
            )
            ScaffoldAlert(
                GUIDELINE_ROOT / "GuidelineDotSequence09.vue",
                event_next_callback=lambda _: transition_next(COMPONENT_STATE),
                event_back_callback=lambda _: transition_previous(COMPONENT_STATE),
                can_advance=COMPONENT_STATE.value.can_transition(next=True),
                show=COMPONENT_STATE.value.is_current_step(Marker.dot_seq9),
                speech=speech.value,
            )

        with rv.Col(cols=8):
            if COMPONENT_STATE.value.current_step_between(
                Marker.mee_spe1, Marker.che_mea1
            ):
                show_doppler_dialog = Ref(COMPONENT_STATE.fields.show_doppler_dialog)
                step = Ref(COMPONENT_STATE.fields.doppler_state.step)
                validation_5_failed = Ref(
                    COMPONENT_STATE.fields.doppler_state.validation_5_failed
                )
                max_step_completed_5 = Ref(
                    COMPONENT_STATE.fields.doppler_state.max_step_completed_5
                )
                student_c = Ref(COMPONENT_STATE.fields.doppler_state.student_c)
                velocity_calculated = Ref(
                    COMPONENT_STATE.fields.doppler_state.velocity_calculated
                )

                def _velocity_calculated_callback(value):
                    example_measurement_index = (
                        LOCAL_STATE.value.get_example_measurement_index(
                            COMPONENT_STATE.value.selected_example_galaxy
                        )
                    )
                    example_measurement = Ref(
                        LOCAL_STATE.fields.example_measurements[
                            example_measurement_index
                        ]
                    )
                    example_measurement.set(
                        example_measurement.value.model_copy(
                            update={"velocity_value": round(value)}
                        )
                    )
                    
                    add_example_measurements_to_glue()

                DopplerSlideshow(
                    dialog=COMPONENT_STATE.value.show_doppler_dialog,
                    titles=COMPONENT_STATE.value.doppler_state.titles,
                    step=COMPONENT_STATE.value.doppler_state.step,
                    length=COMPONENT_STATE.value.doppler_state.length,
                    lambda_obs=COMPONENT_STATE.value.obs_wave,
                    lambda_rest=(
                        selected_example_measurement.value.rest_wave_value
                        if selected_example_measurement.value is not None
                        else None
                    ),
                    max_step_completed_5=COMPONENT_STATE.value.doppler_state.max_step_completed_5,
                    failed_validation_5=COMPONENT_STATE.value.doppler_state.validation_5_failed,
                    interact_steps_5=COMPONENT_STATE.value.doppler_state.interact_steps_5,
                    student_c=COMPONENT_STATE.value.doppler_state.student_c,
                    student_vel_calc=COMPONENT_STATE.value.doppler_state.velocity_calculated,
                    event_set_dialog=show_doppler_dialog.set,
                    event_set_step=step.set,
                    event_set_failed_validation_5=validation_5_failed.set,
                    event_set_max_step_completed_5=max_step_completed_5.set,
                    event_set_student_vel_calc=velocity_calculated.set,
                    event_set_student_vel=_velocity_calculated_callback,
                    event_set_student_c=student_c.set,
                    event_next_callback=lambda _: transition_next(COMPONENT_STATE),
                    event_mc_callback=lambda event: mc_callback(event, LOCAL_STATE),
                    state_view={
                        "mc_score": get_multiple_choice(
                            LOCAL_STATE, "interpret-velocity"
                        ),
                        "score_tag": "interpret-velocity",
                    },
                )

            if COMPONENT_STATE.value.current_step_between(Marker.int_dot1, Marker.dot_seq9): # TODO: Change this back to dot_seq14 if we put back 2nd galaxy measurement
                dotplot_tutorial_finished = Ref(
                    COMPONENT_STATE.fields.dotplot_tutorial_finished
                )
                
                tut_viewer_data = None
                if EXAMPLE_GALAXY_SEED_DATA in gjapp.data_collection:
                    tut_viewer_data = gjapp.data_collection[EXAMPLE_GALAXY_SEED_DATA]
                DotplotTutorialSlideshow(
                    dialog=COMPONENT_STATE.value.show_dotplot_tutorial_dialog,
                    step=COMPONENT_STATE.value.dotplot_tutorial_state.step,
                    length=COMPONENT_STATE.value.dotplot_tutorial_state.length,
                    max_step_completed=COMPONENT_STATE.value.dotplot_tutorial_state.max_step_completed,
                    dotplot_viewer=DotplotViewer(gjapp,
                                                 data=tut_viewer_data,
                                                 component_id=DB_VELOCITY_FIELD,
                                                 vertical_line_visible=False,
                                                 unit="km / s",
                                                 x_label="Velocity (km/s)",
                                                 y_label="Number"
                                                 ),
                                                 
                    event_tutorial_finished=lambda _: dotplot_tutorial_finished.set(
                        True
                    ),
                )
                
                
                
                       
                def create_dotplot_viewer():
                    if EXAMPLE_GALAXY_MEASUREMENTS in gjapp.data_collection:
                        viewer_data = [
                            gjapp.data_collection[EXAMPLE_GALAXY_MEASUREMENTS],
                            gjapp.data_collection[EXAMPLE_GALAXY_SEED_DATA],
                        ]
                    else:
                        viewer_data = [gjapp.data_collection[EXAMPLE_GALAXY_SEED_DATA]]
                    return DotplotViewer(gjapp,
                                         data=viewer_data,
                                         component_id=DB_VELOCITY_FIELD,
                                         vertical_line_visible=True, #COMPONENT_STATE.value.current_step_between(Marker.dot_seq2, Marker.dot_seq6),
                                         line_marker_at=sync_velocity_line,
                                         on_click_callback=lambda point: sync_velocity_line.set(point.xs[0]),
                                         unit="km / s",
                                         x_label="Velocity (km/s)",
                                         y_label="Number",
                                         zorder=[5,1],
                                         nbin=75,
                                         x_bounds = dotplot_bounds,
                                         reset_bounds = dotplot_reset_bounds.value
                                         )
                
                
                if EXAMPLE_GALAXY_MEASUREMENTS in gjapp.data_collection:
                    add_example_measurements_to_glue() # make sure updated measurements are in glue
                    create_dotplot_viewer()

            if COMPONENT_STATE.value.is_current_step(Marker.ref_dat1):
                show_reflection_dialog = Ref(
                    COMPONENT_STATE.fields.show_reflection_dialog
                )
                reflect_step = Ref(
                    COMPONENT_STATE.fields.velocity_reflection_state.step
                )
                reflect_max_step_completed = Ref(
                    COMPONENT_STATE.fields.velocity_reflection_state.max_step_completed
                )
                reflection_complete = Ref(COMPONENT_STATE.fields.reflection_complete)

                ReflectVelocitySlideshow(
                    length=8,
                    titles=[
                        "Reflect on your data",
                        "What would a 1920's scientist wonder?",
                        "Observed vs. rest wavelengths",
                        "How galaxies move",
                        "Do your data agree with 1920's thinking?",
                        "Do your data agree with 1920's thinking?",
                        "Did your peers find what you found?",
                        "Reflection complete",
                    ],
                    interact_steps=[2, 3, 4, 5, 6],
                    require_responses=True,
                    dialog=COMPONENT_STATE.value.show_reflection_dialog,
                    step=COMPONENT_STATE.value.velocity_reflection_state.step,
                    max_step_completed=COMPONENT_STATE.value.velocity_reflection_state.max_step_completed,
                    reflection_complete=COMPONENT_STATE.value.reflection_complete,
                    state_view={
                        "mc_score_2": get_multiple_choice(
                            LOCAL_STATE, "wavelength-comparison"
                        ),
                        "score_tag_2": "wavelength-comparison",
                        "mc_score_3": get_multiple_choice(LOCAL_STATE, "galaxy-motion"),
                        "score_tag_3": "galaxy-motion",
                        "mc_score_4": get_multiple_choice(
                            LOCAL_STATE, "steady-state-consistent"
                        ),
                        "score_tag_4": "steady-state-consistent",
                        "mc_score_5": get_multiple_choice(
                            LOCAL_STATE, "moving-randomly-consistent"
                        ),
                        "score_tag_5": "moving-randomly-consistent",
                        "mc_score_6": get_multiple_choice(
                            LOCAL_STATE, "peers-data-agree"
                        ),
                        "score_tag_6": "peers-data-agree",
                    },
                    event_set_dialog=show_reflection_dialog.set,
                    event_mc_callback=lambda event: mc_callback(event, LOCAL_STATE),
                    # These are numbered based on window-item value
                    event_set_step=reflect_step.set,
                    event_set_max_step_completed=reflect_max_step_completed.set,
                    event_on_reflection_complete=lambda _: reflection_complete.set(
                        True
                    ),
                )

    with rv.Row():
        with rv.Col(cols=4):
            ScaffoldAlert(
                GUIDELINE_ROOT / "GuidelineSpectrum.vue",
                event_next_callback=lambda _: transition_next(COMPONENT_STATE),
                event_back_callback=lambda _: transition_previous(COMPONENT_STATE),
                can_advance=COMPONENT_STATE.value.can_transition(next=True),
                show=COMPONENT_STATE.value.is_current_step(Marker.mee_spe1),
                state_view={
                    "spectrum_tutorial_opened": COMPONENT_STATE.value.spectrum_tutorial_opened
                },
                speech=speech.value,
            )

            selected_example_galaxy_data = (
                selected_example_measurement.value.galaxy.dict()
                if selected_example_measurement.value is not None
                else None
            )

            ScaffoldAlert(
                GUIDELINE_ROOT / "GuidelineRestwave.vue",
                event_next_callback=lambda _: transition_next(COMPONENT_STATE),
                event_back_callback=lambda _: transition_previous(COMPONENT_STATE),
                can_advance=COMPONENT_STATE.value.can_transition(next=True),
                show=COMPONENT_STATE.value.is_current_step(Marker.res_wav1),
                state_view={
                    "selected_example_galaxy": selected_example_galaxy_data,
                    "lambda_on": COMPONENT_STATE.value.obs_wave_tool_activated,
                    "lambda_used": COMPONENT_STATE.value.obs_wave_tool_used,
                },
                speech=speech.value,
            )
            ScaffoldAlert(
                GUIDELINE_ROOT / "GuidelineObswave1.vue",
                event_next_callback=lambda _: transition_next(COMPONENT_STATE),
                event_back_callback=lambda _: transition_previous(COMPONENT_STATE),
                can_advance=COMPONENT_STATE.value.can_transition(next=True),
                show=COMPONENT_STATE.value.is_current_step(Marker.obs_wav1),
                state_view={"selected_example_galaxy": selected_example_galaxy_data},
                speech=speech.value,
            )
            ScaffoldAlert(
                GUIDELINE_ROOT / "GuidelineObswave2.vue",
                event_next_callback=lambda _: transition_next(COMPONENT_STATE),
                event_back_callback=lambda _: transition_previous(COMPONENT_STATE),
                can_advance=COMPONENT_STATE.value.can_transition(next=True),
                show=COMPONENT_STATE.value.is_current_step(Marker.obs_wav2),
                state_view={
                    "selected_example_galaxy": selected_example_galaxy_data,
                    "zoom_tool_activate": COMPONENT_STATE.value.zoom_tool_activated,
                },
                speech=speech.value,
            )
            ScaffoldAlert(
                GUIDELINE_ROOT / "GuidelineDopplerCalc0.vue",
                event_next_callback=lambda _: transition_next(COMPONENT_STATE),
                event_back_callback=lambda _: transition_previous(COMPONENT_STATE),
                can_advance=COMPONENT_STATE.value.can_transition(next=True),
                show=COMPONENT_STATE.value.is_current_step(Marker.dop_cal0),
                speech=speech.value,
            )
            ScaffoldAlert(
                GUIDELINE_ROOT / "GuidelineDopplerCalc2.vue",
                event_next_callback=lambda _: transition_next(COMPONENT_STATE),
                event_back_callback=lambda _: transition_previous(COMPONENT_STATE),
                can_advance=COMPONENT_STATE.value.can_transition(next=True),
                show=COMPONENT_STATE.value.is_current_step(Marker.dop_cal2),
                speech=speech.value,
            )
            # ScaffoldAlert(
            #     GUIDELINE_ROOT / "GuidelineDotSequence04.vue",
            #     event_next_callback=lambda _: transition_next(COMPONENT_STATE),
            #     event_back_callback=lambda _: transition_previous(COMPONENT_STATE),
            #     can_advance=COMPONENT_STATE.value.can_transition(next=True),
            #     show=COMPONENT_STATE.value.is_current_step(Marker.dot_seq4),
            # )
            # ScaffoldAlert(
            #     GUIDELINE_ROOT / "GuidelineDotSequence10.vue",
            #     event_next_callback=lambda _: transition_next(COMPONENT_STATE),
            #     event_back_callback=lambda _: transition_previous(COMPONENT_STATE),
            #     can_advance=COMPONENT_STATE.value.can_transition(next=True),
            #     show=COMPONENT_STATE.value.is_current_step(Marker.dot_seq10),
            # )
            # ScaffoldAlert(
            #     GUIDELINE_ROOT / "GuidelineDotSequence11.vue",
            #     event_next_callback=lambda _: transition_next(COMPONENT_STATE),
            #     event_back_callback=lambda _: transition_previous(COMPONENT_STATE),
            #     can_advance=COMPONENT_STATE.value.can_transition(next=True),
            #     show=COMPONENT_STATE.value.is_current_step(Marker.dot_seq11),
            # )
            ScaffoldAlert(
                GUIDELINE_ROOT / "GuidelineReflectOnData.vue",
                event_next_callback=lambda _: transition_next(COMPONENT_STATE),
                event_back_callback=lambda _: transition_previous(COMPONENT_STATE),
                can_advance=COMPONENT_STATE.value.can_transition(next=True),
                show=COMPONENT_STATE.value.is_current_step(Marker.ref_dat1),
                speech=speech.value,
            )

        with rv.Col(cols=8):
            show_example_spectrum = COMPONENT_STATE.value.current_step_between(
                Marker.mee_spe1, Marker.che_mea1
            ) or COMPONENT_STATE.value.current_step_between(
                Marker.dot_seq6, Marker.dot_seq12 # TODO: Change this back to dot_seq14 if we put back 2nd galaxy measurement
            )

            show_galaxy_spectrum = COMPONENT_STATE.value.current_step_at_or_after(
                Marker.rem_gal1
            )

            if show_example_spectrum:
                with solara.Column():

                    def _example_wavelength_measured_callback(value):
                        example_measurement_index = (
                            LOCAL_STATE.value.get_example_measurement_index(
                                COMPONENT_STATE.value.selected_example_galaxy
                            )
                        )
                        if example_measurement_index is None:
                            return
                        
                        example_measurement = Ref(
                            LOCAL_STATE.fields.example_measurements[
                                example_measurement_index
                            ]
                        )
                        
                        if example_measurement.value.velocity_value is None:
                            example_measurement.set(
                                example_measurement.value.model_copy(
                                    update={"obs_wave_value": value}
                                )
                            )
                        else:
                            velocity = velocity_from_wavelengths(value, example_measurement.value.rest_wave_value)
                            example_measurement.set(
                                example_measurement.value.model_copy(
                                    update={"obs_wave_value": value, "velocity_value": velocity}
                                )
                            )
                        obs_wave_tool_used.set(True)
                        obs_wave = Ref(COMPONENT_STATE.fields.obs_wave)
                        obs_wave.set(value)

                    obs_wave_tool_used = Ref(COMPONENT_STATE.fields.obs_wave_tool_used)
                    obs_wave_tool_activated = Ref(
                        COMPONENT_STATE.fields.obs_wave_tool_activated
                    )
                    zoom_tool_activated = Ref(
                        COMPONENT_STATE.fields.zoom_tool_activated
                    )

                    SpectrumViewer(
                        galaxy_data=(
                            selected_example_measurement.value.galaxy
                            if selected_example_measurement.value is not None
                            else None
                        ),
                        obs_wave=COMPONENT_STATE.value.obs_wave,
                        spectrum_click_enabled=COMPONENT_STATE.value.current_step_between(
                            Marker.obs_wav1, Marker.obs_wav2
                        ) or COMPONENT_STATE.value.is_current_step(Marker.dot_seq9),
                        on_obs_wave_measured=_example_wavelength_measured_callback,
                        on_obs_wave_tool_clicked=lambda: obs_wave_tool_activated.set(
                            True
                        ),
                        on_zoom_tool_clicked=lambda: zoom_tool_activated.set(True),
                        add_marker_here=sync_wavelength_line,
                        spectrum_bounds = spectrum_bounds,
                        max_spectrum_bounds=max_spectrum_bounds
                    )

                    spectrum_tutorial_opened = Ref(
                        COMPONENT_STATE.fields.spectrum_tutorial_opened
                    )

                    SpectrumSlideshow(
                        event_dialog_opened_callback=lambda _: spectrum_tutorial_opened.set(
                            True
                        )
                    )
            elif show_galaxy_spectrum:
                with solara.Column():

                    def _wavelength_measured_callback(value):
                        measurement_index = LOCAL_STATE.value.get_measurement_index(
                            COMPONENT_STATE.value.selected_galaxy
                        )
                        if measurement_index is None:
                            return

                        has_bad_velocities = Ref(
                            COMPONENT_STATE.fields.has_bad_velocities
                        )
                        is_bad = is_wavelength_poorly_measured(
                            value,
                            selected_measurement.value.rest_wave_value,
                            selected_measurement.value.galaxy.z,
                        )
                        has_bad_velocities.set(is_bad)
                        num_bad_velocities()

                        if not is_bad:
                            measurement = Ref(
                                LOCAL_STATE.fields.measurements[measurement_index]
                            )
                            measurement.set(
                                measurement.value.model_copy(
                                    update={"obs_wave_value": value}
                                )
                            )

                            obs_wave = Ref(COMPONENT_STATE.fields.obs_wave)
                            obs_wave.set(value)
                            
                            set_obs_wave_total()
                            
                            
                        else:
                            logger.info('Wavelength measurement is bad')

                    SpectrumViewer(
                        galaxy_data=(
                            selected_measurement.value.galaxy
                            if selected_measurement.value is not None
                            else None
                        ),
                        obs_wave=COMPONENT_STATE.value.obs_wave,
                        spectrum_click_enabled=COMPONENT_STATE.value.current_step_at_or_after(
                            Marker.obs_wav1
                        ),
                        on_obs_wave_measured=_wavelength_measured_callback,
                    )

                    spectrum_tutorial_opened = Ref(
                        COMPONENT_STATE.fields.spectrum_tutorial_opened
                    )

                    SpectrumSlideshow(
                        event_dialog_opened_callback=lambda _: spectrum_tutorial_opened.set(
                            True
                        )
                    )
