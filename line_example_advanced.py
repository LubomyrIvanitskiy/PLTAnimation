import plt_utils
from animation import *
import html_utils

import numpy as np
import matplotlib.pyplot as plt

"""
This example shows how to extend Block class to create efficient animation
Instead of clearing and re-drawing a line on each frame use plt_utils.update_line 
to update only line data and keep rest params the same.

Also here is recommended way to how you can customize you plt.plot output by passing plt_kwargs as the constructor arg

"""


class Line(Block):

    def __init__(self, func, ax, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.plt_kwargs = kwargs["plt_kwargs"] if "plt_kwargs" in kwargs else {}
        self.t = np.linspace(0, 10, 100)
        self.ax = ax
        ax.set_ylim((-1.2, 1.2))
        self.func = func

    def on_frame(self, progress, last_patches, **kwargs):
        y = self.func(self.t, progress)
        if last_patches is None:
            line, = self.ax.plot(self.t, y, **self.plt_kwargs)
            self.ax.legend(loc="upper right")
        else:
            line = plt_utils.update_line(last_patches, self.t, y)
        return line

    def finish(self, last_patches):
        # Remove all patches to allow next block to draw on clean canvas
        plt_utils.remove_patches(self.ax, [last_patches])


fig, ax = plt.subplots(1, 1)
builder = AnimationBuilder()

builder.add_block(Line(
    func=lambda x, progress: np.sin(10 * x) * np.sin(x * progress),
    ax=ax, duration=20, start=0,
    plt_kwargs={"alpha": 1, "linestyle": "dotted", "label": "sin(10 * x) * sin(x * progress)"})
)

builder.add_block(Line(
    func=lambda x, progress: np.sin(x + 3 * progress),
    ax=ax, duration=20, start=0,
    plt_kwargs={"alpha": 0.6, "color": "purple", "label": "sin(x + 3 * progress)"})
)

builder.add_block(Line(
    func=lambda x, progress: progress * np.sin(x),
    ax=ax, duration=20, start=0,
    plt_kwargs={"alpha": 0.9, "label": "progress * sin(x)"})
)

builder.add_block(Line(
    func=lambda x, progress: progress + 0.5 * np.sin(x) - 0.5,
    ax=ax, duration=20, start=0,
    plt_kwargs={"alpha": 0.2, "label": "progress + 0.5 * sin(x) - 0.5"})
)

anim = builder.build_animation(fig)
html_utils.open_html(html_utils.get_html_video(anim))
