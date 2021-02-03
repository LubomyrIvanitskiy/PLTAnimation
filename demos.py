import abc

import html_utils
import animation_utils
import numpy as np
import matplotlib.pyplot as plt


def blocks_demo():
    fig, axes = plt.subplots(1, 1)
    axes.set_ylim((-1.2, 1.2))

    t = np.linspace(0, 10, 100)

    animation_handler = animation_utils.AnimationHandler(interval=100)

    class Line(animation_utils.LineBlock):

        def provide_data(self, i, duration, frames_passed):
            return t, np.sin(t * i / duration)

    class Scat(animation_utils.ScatterBlock):

        def provide_data(self, i, duration, frames_passed):
            return t, np.sin(t * i / duration)

    class Fill(animation_utils.FillBlock):

        def provide_data(self, i, duration, frames_passed):
            return t, np.zeros_like(t), np.sin(t * i / duration)

    animation_handler.add_block(Line(duration=20, ax=axes, start=0, clear_after_last=True))
    animation_handler.add_block(Scat(duration=20, ax=axes, start=5))
    animation_handler.add_block(Fill(duration=20, ax=axes, start=10))

    ani = animation_handler.build_animation(fig)
    html_utils.open_html(html_utils.get_media_table([html_utils.get_html_video(ani), ""]))


# blocks_demo()


def add_sin_demo():
    fig, axes = plt.subplots(1, 1)
    axes.set_ylim((-4.2, 4.2))

    h_count = 5
    t = np.linspace(0, 10, 100)
    A = np.ones((h_count,))
    w = np.arange(1, h_count + 1)
    b = np.zeros((h_count,))

    hs = [A[i] * np.sin(w[i] * t + b[i]) for i in range(h_count)]

    animation_handler = animation_utils.AnimationHandler(interval=100)

    class Intro(animation_utils.FillBlock):

        def __init__(self, h, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.h = h

        def provide_data(self, i, duration, frames_passed):
            return t, np.zeros_like(t), self.h

        def draw_figure(self, i, data, ax, last_artists, **kwargs):
            line = super().draw_figure(i, data, ax, last_artists, **kwargs)
            line.set_alpha(i / self.duration)
            return line

        def update_figure(self, i, data, ax, last_artists):
            line = super().update_figure(i, data, ax, last_artists)
            line.set_alpha(i / self.duration)
            return line

    class Gone(animation_utils.FillBlock):

        def __init__(self, h, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.h = h

        def provide_data(self, i, duration, frames_passed):
            return t, np.zeros_like(t), self.h

        def draw_figure(self, i, data, ax, last_artists, **kwargs):
            line = super().draw_figure(i, data, ax, last_artists, **kwargs)
            line.set_alpha(1 - i / self.duration)
            return line

        def update_figure(self, i, data, ax, last_artists):
            line = super().update_figure(i, data, ax, last_artists)
            line.set_alpha(1 - i / self.duration)
            return line

    class Transform(animation_utils.FillBlock):

        def __init__(self, h, base, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.h = h
            self.base = base

        def provide_data(self, i, duration, frames_passed):
            return t, np.zeros_like(t), (i / (self.duration-1)) * self.base + self.h

    frame_duration = 20
    oldest_block = animation_handler.add_block(Intro(hs[0], frame_duration, axes))
    for index in range(1, len(hs)):
        h = hs[index]
        base = np.sum(hs[:index], axis=0)
        new_block = animation_handler.add_block(Intro(h, frame_duration, axes))
        block = animation_handler.add_block(
            Transform(h, np.sum(hs[:index], axis=0), frame_duration, axes, predcessor=new_block))
        animation_handler.add_block(
            Gone(base, frame_duration, axes, start=block.start, clear_after_last=True, predcessor=oldest_block))
        oldest_block = block

    ani = animation_handler.build_animation(fig)
    html_utils.open_html(html_utils.get_media_table([html_utils.get_html_video(ani), ""]))


add_sin_demo()
