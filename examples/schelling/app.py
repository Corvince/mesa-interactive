from mesa_interactive import slide
from mesa_interactive.components.charts import create_chart
from mesa_interactive.components.grid import create_grid
from mesa_interactive.components.markdown import create_markdown
from mesa_interactive.interactive import MesaInteractive
from model import Schelling


def switch_agent_type(model, x, y):
    agent = model.grid.get_cell_list_contents([(x, y)])[0]
    agent.type = 1 - agent.type


GridView = create_grid("type", on_click=switch_agent_type)
HappyCount = create_markdown(
    lambda model: f"Happy Agents: {model.happy} of {len(model.schedule.agents)}"
)
HappyChart = create_chart({"happy"}, "Happy Agents")


model_params = {
    "width": 20,
    "height": 20,
    "density": slide(0, 1, 0.1, default=0.65),
    "minority_pc": slide(0, 1, 0.05, default=0.2),
    "homophily": slide(0, 8, 1, default=3),
}

page = MesaInteractive(
    Schelling,
    model_params,
    components=[HappyCount, GridView, HappyChart],
    name="Schelling",
)
page
