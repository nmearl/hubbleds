from solara import Reactive
import solara
import enum
from ...utils import HUBBLE_ROUTE_PATH, HST_KEY_AGE
from ...decorators import computed_property
import dataclasses
from cosmicds.utils import API_URL
from ...state import GLOBAL_STATE
from ...data_models.student import StudentMeasurement
from contextlib import closing

class Marker(enum.Enum):
    pro_dat0 = enum.auto()
    pro_dat1 = enum.auto()
    pro_dat2 = enum.auto()
    pro_dat3 = enum.auto()
    pro_dat4 = enum.auto()
    pro_dat5 = enum.auto()
    pro_dat6 = enum.auto()
    pro_dat7 = enum.auto()
    pro_dat8 = enum.auto()
    pro_dat9 = enum.auto()
    sto_fin1 = enum.auto()
    sto_fin2 = enum.auto()
    sto_fin3 = enum.auto()
    
    @staticmethod
    def next(step):
        return Marker(step.value + 1)
    
    @staticmethod
    def previous(step):
        return Marker(step.value - 1)
    
@dataclasses.dataclass
class ComponentState:
    current_step: Reactive[Marker] = dataclasses.field(default=Reactive(Marker.pro_dat0))
    
    hst_age: float = dataclasses.field(default=HST_KEY_AGE) # a constant value
    
    # TODO: I don't think our_age is used anywhere
    our_age: Reactive[float] = dataclasses.field(default=Reactive(0.0))
    class_age: Reactive[float] = dataclasses.field(default=Reactive(0.0))
    
    ages_within: Reactive[float] = dataclasses.field(default=Reactive(0.15))
    allow_too_close_correct: Reactive[bool] = dataclasses.field(default=Reactive(False))
    
    def __post__init(self):
        pass
    
    def setup(self):
        pass
    
    def is_current_step(self, step: Marker):
        return self.current_step.value == step
    
    def can_transition(self, step: Marker = None, next = False, prev = False):
        if next:
            step = Marker.next(self.current_step.value)
        elif prev:
            step = Marker.previous(self.current_step.value)
        
        print(f"Checking if can transition from {self.current_step.value.name} to {step.name}.")
        
        if hasattr(self, f"{step.name}_gate"):
            return getattr(
                self, 
                f"{step.name}_gate"
                )().value
        
        print(f"No gate exists for step {step.name}, allowing anyway.")
        return True
    
    def transition_to(self, step: Marker, force = False):
        if self.can_transition(step) or force:
            self.current_step.set(step)
            print(f"Transitioned to {step.name}.")
        else:
            print(
                f"Conditions not met to transition from "
                f"{self.current_step.value.name} to {step.name}."
            )
    
    def transition_next(self):
        next_marker = Marker.next(self.current_step.value)
        self.transition_to(next_marker)
        
    def transition_previous(self):
        previous_marker = Marker.previous(self.current_step.value)
        self.transition_to(previous_marker)
        
    
    # def pro_dat0_gate(self):
    #     return True
    
    # @computed_property
    # def pro_dat1_gate(self):
    #     return True
    
    # @computed_property
    # def pro_dat2_gate(self):
    #     return True
    
    # @computed_property
    # def pro_dat3_gate(self):
    #     return True
    
    # @computed_property
    # def pro_dat4_gate(self):
    #     return True
    
    # @computed_property
    # def pro_dat5_gate(self):
    #     return True
    
    # @computed_property
    # def pro_dat6_gate(self):
    #     return True
    
    # @computed_property
    # def pro_dat7_gate(self):
    #     return True
    
    # @computed_property
    # def pro_dat8_gate(self):
    #     return True
    
    # @computed_property
    # def pro_dat9_gate(self):
    #     return True
    
    # @computed_property
    # def sto_fin1_gate(self):
    #     return True
    
    # @computed_property
    # def sto_fin2_gate(self):
    #     return True
    
    # @computed_property
    # def sto_fin3_gate(self):
    #     return True
    
    