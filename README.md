# Mesa Interactive

[![PyPi](https://img.shields.io/pypi/v/mesa_interactive.svg)](https://pypi.python.org/pypi/mesa_interactive)

## Overview

Mesa Interactive is a specialized Python package designed to provide dynamic visualization and interaction capabilities for Mesa models. It extends the functionalities of the [Mesa framework](https://github.com/projectmesa/mesa) for agent-based modeling.

## Quick Installation

To quickly install the package, open your terminal and run:

```bash
pip install mesa_interactive
```

## Tutorial: Visualizing the Schelling Segregation Model

This section provides a step-by-step walkthrough to visualize a Schelling Segregation model using Mesa Interactive.

### Prerequisites

Ensure that you have `mesa-models` installed. If not, run the following command:

```bash
pip install -U -e git+https://github.com/projectmesa/mesa-examples#egg=mesa-models
```

### Importing Dependencies

Import the essential libraries as follows:

```python
import solara
from mesa_models.schelling.model import Schelling

from mesa_interactive import MesaInteractive, slide, static
from mesa_interactive.components import create_chart, create_grid, create_markdown
```

### Building Components

1. **Instructions**: Add Markdown instructions. We use the _static_ helper function, since it doesn't rely on model parameters.

```python
Instructions = static(solara.Markdown("Click on an agent to switch its type."))
```

####

2. **GridView**: Construct a grid view, enabling a `switch_agent_type` function on agent click.

```python
def switch_agent_type(model, x, y):
    agent = model.grid.get_cell_list_contents([(x, y)])[0]
    agent.type = 1 - agent.type

GridView = create_grid(color="type", on_click=switch_agent_type)
```

3. **HappyCount**: Display the number of satisfied agents via a Markdown component.

```python
HappyCount = create_markdown(
    lambda model: f"**Happy Agents: {model.happy} of {len(model.schedule.agents)}**"
)
```

4. **HappyChart**: Implement a time-series chart to track the number of happy agents.

```python
HappyChart = create_chart(variables=["happy"], "Happy Agents")
```

### Configuring Model Parameters

Define user-adjustable model parameters using default values and the _slide_ helper functions. It works like the built-in _range_ function but supports arbitrary steps and a default value.

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

2. To render your visulazation save your python file as `app.py` and from a terminal run

```
solara run app.py
```

Alternatively you can but everything in a Jupyter notebook and simply call

```python
page
```

to show the visualization.

Now you have built a fully interactive visualization for the Schelling Segregation model!
