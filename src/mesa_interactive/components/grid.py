import json
from typing import Callable

import altair as alt
import mesa
import solara


def get_agent_data_from_coord_iter(agents_per_coordinate):
    for agents, (x, y) in agents_per_coordinate:
        if agents:  # Checking if the list is non-empty
            if agents not isinstance(list):
                agents = [agents]
            for agent in agents:
                agent_data = json.loads(
                    json.dumps(agent.__dict__, skipkeys=True, default=str)
                )
                agent_data["x"] = x
                agent_data["y"] = y
                agent_data.pop("model", None)
                agent_data.pop("pos", None)
                yield agent_data

def create_grid(
    color: str | None = None,
    on_click: Callable[[mesa.Model, mesa.space.Coordinate], None] | None = None,
) -> Callable[[mesa.Model], solara.component]:
    return lambda model: Grid(model, color, on_click)


def Grid(model, color=None, on_click=None):
    if color is None:
        color = "unique_id:N"

    if color[-2] != ":":
        color = color + ":N"

    data = solara.reactive(
        list(get_agent_data_from_coord_iter(model.grid.coord_iter()))
    )

    def update_data():
        data.value = list(get_agent_data_from_coord_iter(model.grid.coord_iter()))

    def click_handler(datum):
        if datum is None:
            return
        on_click(model, datum["x"], datum["y"])
        update_data()

    default_tooltip = [f"{key}:N" for key in data.value[0]]
    chart = (
        alt.Chart(alt.Data(values=data.value))
        .mark_rect()
        .encode(
            x=alt.X("x:N", scale=alt.Scale(domain=list(range(model.grid.width)))),
            y=alt.Y(
                "y:N",
                scale=alt.Scale(domain=list(range(model.grid.height - 1, -1, -1))),
            ),
            color=color,
            tooltip=default_tooltip,
        )
    )
    return solara.FigureAltair(chart, on_click=click_handler)
