from dataclasses import dataclass
from functools import total_ordering

import solara


def slide(start, stop=0, step=1, default=None):
    return Slide(start, stop, step, default)


@total_ordering
@dataclass
class Slide:
    start: int | float
    stop: int | float
    step: int | float
    value: int | float | None

    def __post_init__(self):
        if self.stop == 0:
            self.stop = self.start
            self.start = 0

        if self.value is None:
            self.value = self.start + (self.stop - self.start) / 2

    def __float__(self):
        return float(self.value)

    def __eq__(self, other):
        if isinstance(other, (Slide, int, float)):
            return self.value == float(other)
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, (Slide, int, float)):
            return self.value < float(other)
        return NotImplemented


def static(component):
    """prepend func with a wrapper that is called with model as first argument"""

    @solara.component
    def wrapper(model):
        return component

    return wrapper
