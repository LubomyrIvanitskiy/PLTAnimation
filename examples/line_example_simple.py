import matplotlib.pyplot as plt
import numpy as np

import html_utils
from animation import *


class Plot(Block):

    def __init__(self, func, ax, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ax = ax
        self.func = func

    def on_frame(self, progress, last_patches, **kwargs):
        # clear last patch
        if last_patches in self.ax.lines:
            self.ax.lines.remove(last_patches)

        x = np.linspace(0, 10, 1000)
        y = self.func(x, progress)
        patch = self.ax.plot(x, y, color="blue")[0]
        return patch


fig, ax = plt.subplots(1, 1)
ax.set_ylim((-1.2, 1.2))
ax.set_title("Amplitude modulation example")
ax.set_xlabel("t")
builder = AnimationBuilder()

builder.add_block(
    Plot(
        func=lambda x, progress: np.sin(10 * x) * np.sin(x * progress),
        ax=ax, duration=20, start=0
    )
)

anim = builder.build_animation(fig)
html_utils.open_html(html_utils.get_html_video(anim))
