import dataclasses
from cosmicds.state import GlobalState
from solara import Reactive

from typing import TypedDict
class MCScore(TypedDict):
    tag: str
    score: float = None
    choice: int = None
    tries: int = 0
    wrong_attempts: int = 0

@dataclasses.dataclass
class LocalState:
    debug_mode: Reactive[bool] = dataclasses.field(default=Reactive(False))
    title: Reactive[str] = dataclasses.field(default=Reactive("Hubble's Law"))
    measurements: Reactive[dict] = dataclasses.field(default=Reactive({}))
    calculations: Reactive[dict] = dataclasses.field(default=Reactive({}))
    validation_failure_counts: Reactive[dict] = dataclasses.field(default=Reactive({}))
    has_best_fit_galaxy: Reactive[bool] = dataclasses.field(default=Reactive(False))
    enough_students_ready: Reactive[bool] = dataclasses.field(default=Reactive(False))
    started: Reactive[bool] = dataclasses.field(default=Reactive(False))
    class_data_students: Reactive[list] = dataclasses.field(default=Reactive([]))
    class_data_info: Reactive[dict] = dataclasses.field(default=Reactive({}))
    mc_scoring : Reactive[dict[str, MCScore]]  = dataclasses.field(default=Reactive({
        # 'pro-dat1': {'tag': 'pro-dat1', 'score': 0.0, 'choice': 1, 'tries': 1, 'wrong_attempts': 0},
        }))


GLOBAL_STATE = GlobalState()
LOCAL_STATE = LocalState()




# create handlers for mc_radiogroup
def onInitResponse(local_state , tag: str, set_score: callable = None): 
    print("onInitResponse")
    # print(tag not in component_state.mc_scoring.value.keys())
    if tag not in local_state.mc_scoring.value.keys():
        print("adding tag", tag)
        mc_scoring = local_state.mc_scoring.value
        mc_scoring.update({tag:MCScore(tag=tag)})
        local_state.mc_scoring.set(mc_scoring)
        set_score(mc_scoring)
    else:
        print("tag already exists")
    

def on_mc_score(local_state, set_score, data):
    print("on_mc_score")
    mc_scoring = local_state.mc_scoring.value
    mc_scoring[data['tag']] = MCScore(**data)
    local_state.mc_scoring.set(mc_scoring)
    set_score(mc_scoring)
    
def mc_callback(event, local_state, set_score: callable = None):
    # mc-initialize-callback returns data which is a string
    if event[0] == 'mc-initialize-response':
        return onInitResponse(local_state = local_state, tag = event[1], set_score = set_score)
    # mc-score event returns a data which is an mc-score dictionary
    elif event[0] == 'mc-score':
        return on_mc_score(local_state=local_state, data = event[1], set_score = set_score)
    else:
        print(f"Unknown event in mc_callback: <<{event}>> ")
    
