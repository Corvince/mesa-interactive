import solara
from mesa import Model
import copy
from mesa_interactive.timeline_controls import TimelineControls
from mesa_interactive.user_inputs import UserInputs


@solara.component
def MesaInteractive(
    model_class: Model,
    model_params,
    components=None,
    *,
    name="Mesa Model",
    play_interval=0,
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

    # 1. Set up model parameters
    user_params, fixed_params = split_model_params(model_params)
    initial_model_params = create_model_parameters(fixed_params, user_params)

    model, set_model = solara.use_state(model_class(**initial_model_params))
    model_cache, set_model_cache = solara.use_state({0: model})

    def handle_change_model_params(user_params):
        new_model_parameters = create_model_parameters(fixed_params, user_params)
        set_model(model_class(**new_model_parameters))
        set_model_cache({0: model})

    def do_step():
        if not model.running:
            return

        updated_model = copy.deepcopy(model)
        updated_model.step()
        set_model(updated_model)

    def handle_step_timeline(step: int):
        if step == model.schedule.steps:
            return

        set_model_cache({**model_cache, model.schedule.steps: model})

        if step in model_cache:
            previous_model = model_cache[step]
            set_model(previous_model)
        else:
            do_step()

    solara.Title(name)

    with solara.Sidebar():
        UserInputs(user_params, on_change=handle_change_model_params)

    TimelineControls(
        play_interval=play_interval,
        on_step=handle_step_timeline,
        on_reset=lambda: handle_step_timeline(0),
        current_step=model.schedule.steps,
        max_step=max(*model_cache.keys(), model.schedule.steps),
    )
    with solara.ColumnsResponsive():
        for component in components:
            component(model)


def create_model_parameters(fixed_params, user_params):
    return {**fixed_params, **{k: v["value"] for k, v in user_params.items()}}


def split_model_params(model_params):
    model_params_input = {}
    model_params_fixed = {}
    for k, v in model_params.items():
        if check_param_is_fixed(v):
            model_params_fixed[k] = v
        else:
            model_params_input[k] = v
    return model_params_input, model_params_fixed


def check_param_is_fixed(param):
    if not isinstance(param, dict):
        return True
    if "type" not in param:
        return True
