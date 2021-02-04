import numpy as np
import matplotlib.pyplot as plt

import plt_utils
from animation import AnimationBuilder, Block

"""
Adding sines with different frequency
"""


class Intro(Block):

    def __init__(self, x, y, axes, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color = kwargs["color"] if "color" in kwargs else None
        self.x = x
        self.y = y
        self.axes = axes

    def on_frame(self, progress, last_patches, **kwargs):
        if last_patches is not None:
            sine, line = last_patches
            sine.set_alpha(progress)
            line.set_alpha(progress)
        else:
            sine, = self.axes.plot(self.x, self.y, alpha=progress, color=self.color if self.color else (1, 0, 0))
            line, = self.axes.plot(self.x, np.zeros_like(self.x), alpha=progress * 0.5, linestyle="dotted",
                                   color=self.color if self.color else (1, 0, 0))
        return sine, line


class Gone(Block):

    def __init__(self, axes, *args, **kwargs):
        super().__init__(*args, **kwargs)
        assert "predecessor_block" in kwargs
        self.axes = axes

    def on_frame(self, progress, last_patches, **kwargs):
        if last_patches is not None:
            sine, line = last_patches
            sine.set_alpha(1 - progress)
            line.set_alpha(1 - progress)
        return sine, line

    def finish(self, last_patches):
        plt_utils.remove_patches(self.axes, last_patches)


class Transform(Block):

    def __init__(self, x, from_y, to_y, axes, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.x = x
        self.from_y = from_y
        self.to_y = to_y
        self.axes = axes

    def on_frame(self, progress, last_patches, **kwargs):
        y = (1 - progress) * self.from_y + progress * self.to_y
        base = self.to_y - self.from_y
        zero_y = (1 - progress) * np.zeros_like(self.x) + progress * base
        if last_patches is not None:
            sine, line = last_patches
            sine.set_color((1 - progress, 0, 0))
            line.set_color((1 - progress, 0, 0))
            line.set_alpha(1 - progress)
            plt_utils.update_line(sine, self.x, y)
            plt_utils.update_line(line, self.x, zero_y)
        else:
            sine, = self.axes.plot(self.x, y, color=(1 - progress, 0, 0))
            line, = self.axes.plot(self.x, zero_y, color=(1 - progress, 0, 0), alpha=1 - progress)
        return sine, line

    def finish(self, last_patches):
        if last_patches is not None:
            sine, line = last_patches
            plt_utils.remove_patches(self.axes, line)


harmonics_count = 5

# Function parameters
t = np.linspace(0, 10, 1000)
A = np.ones((harmonics_count,))
w = np.arange(1, harmonics_count + 1)
b = np.zeros((harmonics_count,))

harmonics = [A[i] * np.sin(w[i] * t + b[i]) for i in range(harmonics_count)]

fig, axes = plt.subplots(1, 1)
axes.set_ylim((-harmonics_count, harmonics_count))
axes.set_title("Sine wave superposition")
axes.set_xlabel("t")

builder = AnimationBuilder()
frame_duration = 20

oldest_block = builder.add_block(
    Intro(t, y=harmonics[0], duration=frame_duration, axes=axes, start=0, color="black")
)

for index in range(1, len(harmonics)):
    base = np.sum(harmonics[:index], axis=0)
    new_block = builder.add_block(
        Intro(t, y=harmonics[index], duration=frame_duration, axes=axes)
    )
    transform_block = builder.add_block(
        Transform(t, harmonics[index], harmonics[index] + base, duration=frame_duration, axes=axes,
                  predecessor_block=new_block))

    gone_block = builder.add_block(
        Gone(duration=frame_duration, axes=axes, start=int(transform_block.start + frame_duration / 2),
             predecessor_block=oldest_block))
    oldest_block = transform_block
anim = builder.build_animation(fig)

plt.show()
# html_utils.open_html(html_utils.get_html_video(anim))
