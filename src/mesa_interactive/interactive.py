import copy
from typing import Literal

import solara
from mesa import Model

from mesa_interactive.timeline_controls import TimelineControls
from mesa_interactive.user_inputs import UserInputs
from mesa_interactive.util import Slide


@solara.component
def MesaInteractive(
    model_class: Model,
    model_params,
    components=None,
    *,
    name="Mesa Model",
    play_interval=0,
    show_dataframe: Literal["both", "model", "agent", "none"] = "none",
):
    """Initialize a component to visualize a model.
    Args:
        model_class: class of the model to instantiate
        model_params: parameters for initializing the model
        name: name for display
        play_interval: play interval in ms
    """

    if components is None:
        components = []

    current_step, set_current_step = solara.use_state(0)

    params, set_params = solara.use_state(create_model_parameters(model_params))

    cache, set_cache = solara.use_state([model_class(**params)])

    try:
        model = cache[current_step]
    except IndexError:
        return

    def handle_change_model_params(new_model_params):
        set_params(create_model_parameters(new_model_params))
        set_cache([model_class(**new_model_params)])
        set_current_step(0)

    def model_step():
        if not model.running:
            return

        updated_model = copy.deepcopy(model)
        updated_model.step()
        set_cache([*cache, updated_model])
        set_current_step(updated_model.schedule.steps)

    def reset_model():
        set_current_step(0)
        set_cache([model_class(**params)])

    def handle_step_timeline(step: int):
        if step == model.schedule.steps:
            return

        if step < len(cache):
            set_current_step(step)
        else:
            model_step()

    solara.Title(name)

    with solara.Sidebar():
        UserInputs(model_params, handle_change_model_params)

    TimelineControls(
        play_interval=play_interval,
        on_step=handle_step_timeline,
        on_reset=reset_model,
        current_step=current_step,
        max_step=len(cache) - 1,
    )
    with solara.Column():
        for component in components:
            component(model)

    if show_dataframe in {"both", "model"}:
        solara.DataFrame(model.datacollector.get_model_vars_dataframe())
    if show_dataframe in {"both", "agent"}:
        solara.DataFrame(model.datacollector.get_agent_vars_dataframe())


def create_model_parameters(model_params):
    return {param: _get_value(value) for param, value in model_params.items()}


def _get_value(user_param):
    if isinstance(user_param, Slide):
        return user_param.value
    if isinstance(user_param, list):
        return user_param[0]
    return user_param
