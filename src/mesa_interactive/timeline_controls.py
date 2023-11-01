import time
from typing import Callable

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

    def play_simulation():
        if playing.value:
            on_step(current_step + 1)
            time.sleep(play_interval / 1000)

    def change_step(value):
        return lambda: on_step(max(0, value))

    def reset():
        playing.value = False
        on_reset()

    solara.use_thread(
        play_simulation,
        dependencies=[playing.value, current_step],
    )

    def handle_click_start_stop():
        playing.value = not playing.value

    with solara.Card(title="Model Controls"), solara.Column(
        gap="40px",
    ):
        with solara.Row(gap="2px", style={"align-items": "center"}):
            with solara.Tooltip("Reset the model"):
                solara.Button(icon_name="mdi-reload", color="primary", on_click=reset)
            with solara.Tooltip("Play / Pause simulation"):
                solara.Button(
                    icon_name="mdi-play-pause",
                    color="primary",
                    on_click=handle_click_start_stop,
                )
            with solara.Tooltip("Step backward to the beginning"):
                solara.Button(
                    icon_name="mdi-skip-backward",
                    color="primary",
                    disabled=playing.value,
                    on_click=change_step(0),
                )
            with solara.Tooltip("Step backward"):
                solara.Button(
                    icon_name="mdi-step-backward",
                    color="primary",
                    disabled=playing.value,
                    on_click=change_step(current_step - 1),
                )
            with solara.Tooltip("Step forward"):
                solara.Button(
                    icon_name="mdi-step-forward",
                    color="primary",
                    disabled=playing.value,
                    on_click=change_step(current_step + 1),
                )
            with solara.Tooltip("Step forward to the end"):
                solara.Button(
                    icon_name="mdi-skip-forward",
                    color="primary",
                    disabled=playing.value,
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
