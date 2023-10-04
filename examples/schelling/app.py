from mesa_interactive.mesa_interactive import MesaInteractive
from mesa_interactive.components.charts import make_chart
from mesa_interactive.components.markdown import make_markdown
from model import Schelling
from mesa_interactive.components.vega_grid import make_grid


def on_click(model, x, y):
    agent = model.grid.get_cell_list_contents([(x, y)])[0]
    agent.type = 1 - agent.type


GridView = make_grid("type:N", click_handler=on_click)
HappyCount = make_markdown(
    lambda model: f"Happy Agents: {model.happy} of {len(model.schedule.agents)}"
)
HappyChart = make_chart({"happy"}, "Happy Agents")


model_params = {
    "density": {
        "type": "SliderFloat",
        "value": 0.8,
        "label": "Agent density",
        "min": 0.1,
        "max": 1.0,
        "step": 0.1,
    },
    "minority_pc": {
        "type": "SliderFloat",
        "value": 0.2,
        "label": "Fraction minority",
        "min": 0.0,
        "max": 1.0,
        "step": 0.05,
    },
    "homophily": {
        "type": "SliderInt",
        "value": 3,
        "label": "Homophily",
        "min": 0,
        "max": 8,
        "step": 1,
    },
    "width": 20,
    "height": 20,
}

page = MesaInteractive(
    Schelling,
    model_params,
    components=[HappyCount, GridView, HappyChart],
    name="Schelling",
)
page  # noqa
