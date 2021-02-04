import html_utils
from animation import *
from template_blocks import *

import matplotlib.pyplot as plt
import numpy as np

builder = AnimationBuilder(100)

X = np.linspace(-8, 8, 200)
Y = np.linspace(-8, 8, 200)
X, Y = np.meshgrid(X, Y)


class MyBlock(Surface3DBlock):

    def provide_data(self, i, duration, frames_passed):
        R = np.sqrt(X ** 2 + Y ** 2)
        Z = 4*np.sin(R * ((i / duration) * 5))

        return X, Y, Z

    def on_frame(self, i, data, ax, last_artists, **kwargs):
        surface = super().on_frame(i, data, ax, last_artists, **kwargs)
        surface.set_alpha(0.3)
        return surface

    def update_figure(self, i, data, ax, last_artists, **kwargs):
        surface = super().update_figure(i, data, ax, last_artists, **kwargs)
        surface.set_alpha(0.3)
        return surface


fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(1, 1, 1, projection='3d')
ax.set_ylim((-10, 10))
ax.set_xlim((-10, 10))
ax.set_zlim((-10, 10))

builder.add_block(MyBlock(50, ax))
# builder.add_block(
#     ProjectionRotation(initial_angle=(15, 0), angle_delta=(0, 180), duration=20, ax=ax, start=0))

a = builder.build_animation(fig)
html_utils.open_html(html_utils.get_html_video(a))
