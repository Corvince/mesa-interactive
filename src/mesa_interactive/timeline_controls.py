from typing import Callable

import ipywidgets as widgets
import solara


@solara.component
def TimelineControls(
    play_interval: int,
    on_step: Callable[[int], None],
    on_reset: Callable[[], None],
    current_step: int,
    max_step: int,
):
    playing = solara.use_reactive(value=False)

    def on_value_play(_):
        if playing.value:
            on_step(current_step + 1)

    def change_step(value):
        return lambda: on_step(max(0, value))

    def reset():
        playing.value = False
        on_reset()

    with solara.Card(title="Model Controls"), solara.Column(
        gap="40px",
    ):
        with solara.Row(gap="2px", style={"align-items": "center"}):
            with solara.Tooltip("Reset the model"):
                solara.Button(icon_name="mdi-reload", color="primary", on_click=reset)
            with solara.Tooltip("Step backward to the beginning"):
                solara.Button(
                    icon_name="mdi-skip-backward",
                    color="primary",
                    on_click=change_step(0),
                )
            with solara.Tooltip("Step backward"):
                solara.Button(
                    label="-1",
                    color="primary",
                    on_click=change_step(current_step - 1),
                )
            widgets.Play(
                value=0,
                interval=play_interval,
                show_repeat=False,
                on_value=on_value_play,
                playing=playing.value,
                on_playing=playing.set,
                layout=widgets.Layout(height="36px"),
            )
            widgets.Button(description="hi")
            with solara.Tooltip("Step forward"):
                solara.Button(
                    label="+1",
                    color="primary",
                    on_click=change_step(current_step + 1),
                )
            with solara.Tooltip("Step forward to the end"):
                solara.Button(
                    icon_name="mdi-skip-forward",
                    color="primary",
                    on_click=change_step(max_step),
                )
        solara.SliderInt(
            label="Timeline (current step)",
            value=current_step,
            min=0,
            max=max_step,
            thumb_label="always",
            step=1,
            on_value=on_step,
        )
