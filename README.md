# Mesa Interactive

## Overview

Mesa Interactive is a specialized Python package designed to provide dynamic visualization and interaction capabilities for Mesa models. It extends the functionalities of the [Mesa framework](https://github.com/projectmesa/mesa) for agent-based modeling.

## Quick Installation

To quickly install the package, open your terminal and run:

```bash
pip install mesa_interactive
```

## Example: Visualizing a Schelling Segregation Model

This section provides a step-by-step walkthrough to visualize a Schelling Segregation model using Mesa Interactive.

### Prerequisites

Ensure that you have `mesa-models` installed. If not, run the following command:

```bash
pip install -U -e git+https://github.com/projectmesa/mesa-examples#egg=mesa-models
```

### Importing Dependencies

Load the essential libraries as follows:

```python
import solara
from mesa_interactive import slide, static
from mesa_interactive.components import create_chart, create_grid, create_markdown
from mesa_interactive.interactive import MesaInteractive
from mesa_models.schelling.model import Schelling
```

### Defining Custom Functions

1. **Switch Agent Type**: Create a function to toggle an agent's type when clicked on the grid.

```python
def switch_agent_type(model, x, y):
    agent = model.grid.get_cell_list_contents([(x, y)])[0]
    agent.type = 1 - agent.type
```

### Building Components

1. **GridView**: Construct a grid view, enabling the `switch_agent_type` function on agent click.

```python
GridView = create_grid("type", on_click=switch_agent_type)
```

2. **Instructions**: Add Markdown instructions. These are static and don't rely on model parameters.

```python
Instructions = static(solara.Markdown("Click on an agent to switch its type."))
```

3. **HappyCount**: Display the number of satisfied agents via a Markdown component.

```python
HappyCount = create_markdown(
    lambda model: f"**Happy Agents: {model.happy} of {len(model.schedule.agents)}**"
)
```

4. **HappyChart**: Implement a time-series chart to track the number of happy agents.

```python
HappyChart = create_chart("happy", "Happy Agents")
```

### Configuring Model Parameters

Define user-adjustable model parameters using sliders:

```python
model_params = {
    "width": 20,
    "height": 20,
    "density": slide(0, 1, 0.1, default=0.65),
    "minority_pc": slide(0, 1, 0.05, default=0.2),
    "homophily": slide(0, 8, 1, default=3),
}
```

### Creating the Interactive Page

1. Initialize the Mesa Interactive interface with the Schelling model, model parameters, and assembled components.

```python
page = MesaInteractive(
    Schelling,
    model_params,
    components=[HappyCount, Instructions, GridView, HappyChart],
    name="Schelling",
    show_dataframe="model",
)
```

2. To render and display all the components, simply call:

```python
page
```

Now you have a fully interactive visualization for the Schelling Segregation model!
