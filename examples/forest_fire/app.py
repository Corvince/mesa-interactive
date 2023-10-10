import solara
from mesa_interactive import MesaInteractive
from mesa_interactive.components.grid import create_grid
from mesa_interactive.util import slide, static
from model import ForestFire


def set_tree_on_fire(model, x, y):
    model.grid[x][y].condition = "On Fire"


grid = create_grid("condition:N", on_click=set_tree_on_fire)


app = MesaInteractive(
    ForestFire,
    {"width": 20, "height": 20, "density": slide(0, 1, 0.05, default=0.65)},
    components=[
        static(solara.Markdown("Click on a healthy tree to set it on fire!")),
        grid,
    ],
    show_dataframe="model",
)
app
