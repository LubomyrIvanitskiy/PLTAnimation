import matplotlib.pyplot as plt
import numpy as np

import html_utils
import plt_utils
from animation import *
from template_blocks import *


class ComplexPlane(Block):

    def __init__(self, func, axes, duration, **kwargs):
        super().__init__(duration, **kwargs)
        self.t = np.linspace(0, 10, 1000)
        self.lim = 2
        ax.set_xlim((0, 10))
        ax.set_ylim((-self.lim, self.lim))
        ax.set_zlim((-self.lim, self.lim))
        ax.set_xlabel("Time")
        ax.set_ylabel("Imaginary")
        ax.set_zlabel("Real")
        self.func = func
        self.axes = axes

    def on_frame(self, progress, last_patches, **kwargs):
        plt_utils.remove_patches(self.axes, last_patches)

        y = self.func(self.t, progress)
        real_part = np.real(y)
        imag_part = np.imag(y)

        upper_bound = int(progress * len(self.t))

        real_shadow, = self.axes.plot(self.t[:upper_bound], np.zeros_like(self.t[:upper_bound]) + self.lim,
                                      real_part[:upper_bound], color="grey", alpha=0.6,
                                      linestyle="dashed")
        imag_shadow, = self.axes.plot(self.t[:upper_bound], imag_part[:upper_bound],
                                      np.zeros_like(self.t[:upper_bound]) - self.lim, color="grey", alpha=0.6,
                                      linestyle="dashed")
        line, = self.axes.plot(self.t[:upper_bound], imag_part[:upper_bound], real_part[:upper_bound], color="blue", label="e^(3i*x)")
        self.axes.legend()
        return line, real_shadow, imag_shadow


fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot(1, 1, 1, projection='3d')

builder = AnimationBuilder()
builder.add_block(ComplexPlane(
    func=lambda x, progress: np.exp(3j * x),
    axes=ax, duration=50))
a = builder.build_animation(fig)
html_utils.open_html(html_utils.get_html_video(a))
