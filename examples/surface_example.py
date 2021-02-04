import matplotlib.pyplot as plt
import numpy as np

import html_utils
import plt_utils
from animation import *
from template_blocks import *


class Surface(Block):

    def __init__(self, axes, duration, **kwargs):
        super().__init__(duration, **kwargs)
        X = np.linspace(-8, 8, 10)
        Y = np.linspace(-8, 8, 10)
        self.X, self.Y = np.meshgrid(X, Y)
        self.axes = axes

    def on_frame(self, progress, last_patches, **kwargs):
        plt_utils.remove_patches(self.axes, last_patches)
        R = np.sqrt(self.X ** 2 + self.Y ** 2)
        Z = np.sin(R * progress)
        surface = self.axes.plot_surface(self.X, self.Y, Z, color="green")
        return surface


fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(1, 1, 1, projection='3d')
ax.set_ylim((-10, 10))
ax.set_xlim((-10, 10))
ax.set_zlim((-10, 10))

builder = AnimationBuilder()
builder.add_block(Surface(axes=ax, duration=50))
a = builder.build_animation(fig)
html_utils.open_html(html_utils.get_html_video(a))
