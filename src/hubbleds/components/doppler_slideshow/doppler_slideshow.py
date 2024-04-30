import solara
import reacton.ipyvuetify as rv
from ipyvuetify import VuetifyTemplate
from ...utils import IMAGE_BASE_URL


@solara.component_vue("SlideshowDopplerCalc5.vue")
def DopplerSlideshow(
    dialog,
    titles,
    step,
    length,
    lambda_obs,
    lambda_rest,
    max_step_completed_5,
    failed_validation_5,
    interact_steps_5,
    student_vel,
    student_c,
    student_vel_calc,
    event_set_student_vel_calc,
    event_next_callback,
):
    pass
