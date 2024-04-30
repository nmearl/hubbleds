# Stage 6 (prodata)
import solara

from cosmicds.components import ScaffoldAlert
from cosmicds import load_custom_vue_components

from glue_jupyter.app import JupyterApplication


from reacton import ipyvuetify as rv
from solara import Reactive

from pathlib import Path

from ...data_management import *
from ...state import GLOBAL_STATE, LOCAL_STATE, mc_callback
# import for type definitions


from .component_state import ComponentState, Marker

# the guidelines in the current files parent directory
GUIDELINE_ROOT = Path(__file__).parent / "guidelines"

# create glue app with the global data collection and session
gjapp = JupyterApplication(GLOBAL_STATE.data_collection, GLOBAL_STATE.session)

# intitialize the component state
component_state = ComponentState()

    
# create the Page for the current stage
@solara.component
def Page():
    
    # NM: Custom vue-only components have to be registered in the Page element
    #  currently, otherwise they will not be available in the front-end 
    load_custom_vue_components() # currently this just loads the ScaffoldAlert component
    
    # NM: Solara's reactivity is often tied to the _context_ of the Page it's
    #  being rendered in. Currently, in order to trigger subscribed callbacks,
    #  state connections need to be initialized _inside_ a Page.
    component_state.setup()
    
    
    mc_scoring, set_mc_scoring  = solara.use_state(LOCAL_STATE.mc_scoring.value)
        

    
    solara.Markdown(
        f"""
        Current Step: {component_state.current_step.value}

        Next step: {Marker.next(component_state.current_step.value)}

        Can advance: {component_state.can_transition(next=True)}

        mc-scoring: {mc_scoring}

        """
    )
    
    
    with rv.Row():
        ScaffoldAlert(
            GUIDELINE_ROOT / "guideline_professional_data0.vue",
            event_next_callback=lambda *args: component_state.transition_next(),
            can_advance=component_state.can_transition(next=True),
            show=component_state.is_current_step(Marker.pro_dat0),
        )
        s = ScaffoldAlert(
            GUIDELINE_ROOT / "guideline_professional_data1.vue",
            event_next_callback=lambda *args: component_state.transition_next(),
            event_back_callback=lambda *args: component_state.transition_previous(),
            can_advance=component_state.can_transition(next=True),
            show=component_state.is_current_step(Marker.pro_dat1),
            event_mc_callback=lambda event: mc_callback(event = event, local_state = LOCAL_STATE, set_score=set_mc_scoring),
            state_view={'mc_score': mc_scoring.get('pro-dat1'), 'score_tag': 'pro-dat1'}
        )
        ScaffoldAlert(
            GUIDELINE_ROOT / "guideline_professional_data2.vue",
            event_next_callback=lambda *args: component_state.transition_next(),
            event_back_callback=lambda *args: component_state.transition_previous(),
            can_advance=component_state.can_transition(next=True), 
            show=component_state.is_current_step(Marker.pro_dat2),
            event_mc_callback=lambda event: mc_callback(event = event, local_state = LOCAL_STATE, set_score=set_mc_scoring),
            state_view={'mc_score': mc_scoring.get('pro-dat2'), 'score_tag': 'pro-dat2'}
            
        )
        ScaffoldAlert(
            GUIDELINE_ROOT / "guideline_professional_data3.vue",
            event_next_callback=lambda *args: component_state.transition_next(),
            event_back_callback=lambda *args: component_state.transition_previous(),
            can_advance=component_state.can_transition(next=True),
            show=component_state.is_current_step(Marker.pro_dat3),
            event_mc_callback=lambda event: mc_callback(event = event, local_state = LOCAL_STATE, set_score=set_mc_scoring),
            state_view={'mc_score': mc_scoring.get('pro-dat3'), 'score_tag': 'pro-dat3'}
        )
        ScaffoldAlert(
            GUIDELINE_ROOT / "guideline_professional_data4.vue",
            event_next_callback=lambda *args: component_state.transition_next(),
            event_back_callback=lambda *args: component_state.transition_previous(),
            can_advance=component_state.can_transition(next=True),
            show=component_state.is_current_step(Marker.pro_dat4),
            event_mc_callback=lambda event: mc_callback(event = event, local_state = LOCAL_STATE, set_score=set_mc_scoring),
            state_view={'mc_score': mc_scoring.get('pro-dat4'), 'score_tag': 'pro-dat4'}
        )
        ScaffoldAlert(
            GUIDELINE_ROOT / "guideline_professional_data5.vue",
            event_next_callback=lambda *args: component_state.transition_next(),
            event_back_callback=lambda *args: component_state.transition_previous(),
            can_advance=component_state.can_transition(next=True),
            show=component_state.is_current_step(Marker.pro_dat5),
        )
        ScaffoldAlert(
            GUIDELINE_ROOT / "guideline_professional_data6.vue",
            event_next_callback=lambda *args: component_state.transition_next(),
            event_back_callback=lambda *args: component_state.transition_previous(),
            can_advance=component_state.can_transition(next=True),
            show=component_state.is_current_step(Marker.pro_dat6),
            event_mc_callback=lambda event: mc_callback(event = event, local_state = LOCAL_STATE, set_score=set_mc_scoring),
            state_view={
                'hst_age': component_state.hst_age, 
                'class_age': component_state.class_age,
                'mc_score': mc_scoring.get('pro-dat6'), 
                'score_tag': 'pro-dat4'
                }
        )
        ScaffoldAlert(
            GUIDELINE_ROOT / "guideline_professional_data7.vue",
            event_next_callback=lambda *args: component_state.transition_next(),
            event_back_callback=lambda *args: component_state.transition_previous(),
            can_advance=component_state.can_transition(next=True),
            show=component_state.is_current_step(Marker.pro_dat7),
            event_mc_callback=lambda event: mc_callback(event = event, local_state = LOCAL_STATE, set_score=set_mc_scoring),
            state_view={'mc_score': mc_scoring.get('pro-dat7'), 'score_tag': 'pro-dat7'}
            
        )
        ScaffoldAlert(
            GUIDELINE_ROOT / "guideline_professional_data8.vue",
            event_next_callback=lambda *args: component_state.transition_next(),
            event_back_callback=lambda *args: component_state.transition_previous(),
            can_advance=component_state.can_transition(next=True),
            show=component_state.is_current_step(Marker.pro_dat8),
        )
        ScaffoldAlert(
            GUIDELINE_ROOT / "guideline_professional_data9.vue",
            event_next_callback=lambda *args: component_state.transition_next(),
            event_back_callback=lambda *args: component_state.transition_previous(),
            can_advance=component_state.can_transition(next=True),
            show=component_state.is_current_step(Marker.pro_dat9),
            event_mc_callback=lambda event: mc_callback(event = event, local_state = LOCAL_STATE, set_score=set_mc_scoring),
            state_view={'mc_score': mc_scoring.get('pro-dat9'), 'score_tag': 'pro-dat'}
        )
        ScaffoldAlert(
            GUIDELINE_ROOT / "guideline_story_finish.vue",
            event_next_callback=lambda *args: component_state.transition_next(),
            event_back_callback=lambda *args: component_state.transition_previous(),
            can_advance=component_state.can_transition(next=True),
            show=component_state.is_current_step(Marker.sto_fin1),
        )
        ScaffoldAlert(
            GUIDELINE_ROOT / "guideline_story_finish2.vue",
            event_next_callback=lambda *args: component_state.transition_next(),
            event_back_callback=lambda *args: component_state.transition_previous(),
            can_advance=component_state.can_transition(next=True),
            show=component_state.is_current_step(Marker.sto_fin2),
        )
        ScaffoldAlert(
            GUIDELINE_ROOT / "guideline_story_finish3.vue",
            event_next_callback=lambda *args: component_state.transition_next(),
            event_back_callback=lambda *args: component_state.transition_previous(),
            can_advance=component_state.can_transition(next=True),
            show=component_state.is_current_step(Marker.sto_fin3),
        )
    
    