import solara


@solara.component
def UserInputs(user_params, on_change=None):
    """Initialize user inputs for configurable model parameters.
    Currently supports :class:`solara.SliderInt`, :class:`solara.SliderFloat`,
    :class:`solara.Select`, and :class:`solara.Checkbox`.

    Props:
        user_params: dictionary with options for the input, including label,
        min and max values, and other fields specific to the input type.
        on_change: function to be called with updated inputs.
    """
    with solara.Card(title="Model Parameters"):
        for name, options in user_params.items():
            # label for the input is "label" from options or name
            label = options.get("label", name)
            input_type = options.get("type")

            def change_handler(value, name=name):
                user_params[name]["value"] = value

            if input_type == "SliderInt":
                solara.SliderInt(
                    label,
                    value=options.get("value"),
                    on_value=change_handler,
                    min=options.get("min"),
                    max=options.get("max"),
                    step=options.get("step"),
                )
            elif input_type == "SliderFloat":
                solara.SliderFloat(
                    label,
                    value=options.get("value"),
                    on_value=change_handler,
                    min=options.get("min"),
                    max=options.get("max"),
                    step=options.get("step"),
                )
            elif input_type == "Select":
                solara.Select(
                    label,
                    value=options.get("value"),
                    on_value=change_handler,
                    values=options.get("values"),
                )
            elif input_type == "Checkbox":
                solara.Checkbox(
                    label=label,
                    value=options.get("value"),
                )
            else:
                msg = f"{input_type} is not a supported input type"
                raise ValueError(msg)

        solara.Button("Save and Reset", on_click=lambda: on_change(user_params))
