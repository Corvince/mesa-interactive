import solara

from mesa_interactive.util import Slide


@solara.component
def UserInputs(model_parameters, on_change=None):
    for param in model_parameters:
        value = model_parameters[param]

        def change_handler(value, name=param):
            param = model_parameters[name]
            if isinstance(param, Slide):
                model_parameters[name].value = value
            elif isinstance(param, list):
                model_parameters[name][0] = value
            else:
                model_parameters[name] = value

        if isinstance(value, bool):
            solara.Checkbox(label=param, value=value, on_value=change_handler)
        elif isinstance(value, Slide):
            if isinstance(value.step, int):
                solara.SliderInt(
                    label=param,
                    value=value.value,
                    min=value.start,
                    max=value.stop,
                    step=value.step,
                    on_value=change_handler,
                )
            else:
                solara.SliderFloat(
                    label=param,
                    value=value.value,
                    min=value.start,
                    max=value.stop,
                    step=value.step,
                    on_value=change_handler,
                )
        elif isinstance(value, list):
            solara.Select(
                label=param, value=value[0], values=value, on_value=change_handler
            )
        elif isinstance(value, float):
            solara.InputFloat(param, value=value, on_value=change_handler)
        elif isinstance(value, int):
            solara.InputInt(param, value=value, on_value=change_handler)
        else:
            solara.InputText(param, value=value, on_value=change_handler)

    solara.Button(
        "Save and Reset", color="primary", on_click=lambda: on_change(model_parameters)
    )
