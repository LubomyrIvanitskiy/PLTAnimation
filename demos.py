import html_utils
import animation
import numpy as np
import matplotlib.pyplot as plt
from template_blocks import *


def blocks_demo(axes, builder=None):
    axes.set_ylim((-1.2, 1.2))

    t = np.linspace(0, 10, 100)

    if not builder:
        builder = animation.AnimationBuilder(interval=100)

    class Line(LineBlock):

        def provide_data(self, i, duration, frames_passed):
            return t, np.sin(t * self.get_progress(i))

    class Scat(ScatterBlock):

        def provide_data(self, i, duration, frames_passed):
            return t, np.sin(t * self.get_progress(i))

    class Fill(FillBlock):

        def provide_data(self, i, duration, frames_passed):
            return t, np.zeros_like(t), np.sin(t * self.get_progress(i))

    builder.add_block(Line(duration=20, ax=axes, start=0, clear_after_last=True))
    builder.add_block(Scat(duration=20, ax=axes, start=5))
    builder.add_block(Fill(duration=20, ax=axes, start=10))

    return builder


def add_sin_demo(axes, builder=None):
    axes.set_ylim((-4.2, 4.2))

    h_count = 5
    t = np.linspace(0, 10, 100)
    A = np.ones((h_count,))
    w = np.arange(1, h_count + 1)
    b = np.zeros((h_count,))

    hs = [A[i] * np.sin(w[i] * t + b[i]) for i in range(h_count)]

    if not builder:
        builder = animation.AnimationBuilder(interval=100)

    class Intro(FillBlock):

        def __init__(self, h, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.h = h

        def provide_data(self, i, duration, frames_passed):
            return t, np.zeros_like(t), self.h

        def draw_figure(self, i, data, ax, last_artists, **kwargs):
            line = super().draw_figure(i, data, ax, last_artists, **kwargs)
            line.set_alpha(self.get_progress(i))
            return line

        def update_figure(self, i, data, ax, last_artists):
            line = super().update_figure(i, data, ax, last_artists)
            line.set_alpha(self.get_progress(i))
            return line

    class Gone(FillBlock):

        def __init__(self, h, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.h = h

        def provide_data(self, i, duration, frames_passed):
            return t, np.zeros_like(t), self.h

        def draw_figure(self, i, data, ax, last_artists, **kwargs):
            line = super().draw_figure(i, data, ax, last_artists, **kwargs)
            line.set_alpha(1 - self.get_progress(i))
            return line

        def update_figure(self, i, data, ax, last_artists):
            line = super().update_figure(i, data, ax, last_artists)
            line.set_alpha(1 - self.get_progress(i))
            return line

    class Transform(FillBlock):

        def __init__(self, h, base, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.h = h
            self.base = base

        def provide_data(self, i, duration, frames_passed):
            return t, np.zeros_like(t), self.get_progress(i) * self.base + self.h

    frame_duration = 20
    oldest_block = builder.add_block(Intro(hs[0], frame_duration, axes, start=0))
    for index in range(1, len(hs)):
        h = hs[index]
        base = np.sum(hs[:index], axis=0)
        new_block = builder.add_block(Intro(h, frame_duration, axes))
        block = builder.add_block(
            Transform(h, np.sum(hs[:index], axis=0), frame_duration, axes, predcessor=new_block))
        builder.add_block(
            Gone(base, frame_duration, axes, start=block.start, clear_after_last=True, predcessor=oldest_block))
        oldest_block = block

    return builder


def surface_3d_demo(ax, builder=None):
    t = np.linspace(0, 10, 100)

    zlims = (-1.2, 1.2)
    ylims = (-1.2, 1.2)
    tlims = (0, np.max(t))
    ax.set_zlim(*zlims)
    ax.set_ylim(*ylims)
    ax.set_xlim(*tlims)

    class LineRealShadow(Line3DBlock):

        def provide_data(self, i, duration, frames_passed):
            return t, np.zeros_like(t) + zlims[1], np.real(np.exp(1j * t * self.get_progress(i)) * np.sin(t))

    class LineImagShadow(Line3DBlock):

        def provide_data(self, i, duration, frames_passed):
            return t, np.imag(np.exp(1j * t * self.get_progress(i)) * np.sin(t)), np.zeros_like(t) - ylims[1]

    class ComplexLine(Line3DBlock):

        def provide_data(self, i, duration, frames_passed):
            return t, np.real(np.exp(1j * t * self.get_progress(i)) * np.sin(t)), np.imag(
                np.exp(1j * t * self.get_progress(i)) * np.sin(t))

    class ComplexSurface(Surface3DBlock):

        def provide_data(self, i, duration, frames_passed):
            y = np.arange(-1.1, 1.1, 0.1)
            X, Y = np.meshgrid(t, y)
            R = np.exp(1j * X * self.get_progress(i)) * Y
            return X, np.real(R), np.imag(R)

        def draw_figure(self, i, data, ax, last_artists, **kwargs):
            artists = super().draw_figure(i, data, ax, last_artists, **kwargs)
            artists.set_alpha(0.3)
            artists.set_color("grey")
            return artists

    block_duration = 50
    if not builder:
        builder = animation.AnimationBuilder(interval=100)
    builder.add_block(
        ProjectionRotation(initial_angle=(15, 0), angle_delta=(0, 180), duration=block_duration, ax=ax, start=0))
    builder.add_block(ComplexLine(block_duration, ax, start=0))
    builder.add_block(LineRealShadow(block_duration, ax, start=0))
    builder.add_block(LineImagShadow(block_duration, ax, start=0))
    builder.add_block(ComplexSurface(block_duration, ax, start=0))

    return builder


def progress_demo(axes, builder=None):
    axes.set_ylim((-1.2, 1.2))
    axes.set_xlim((0, 10))

    t = np.linspace(0, 10, 100)

    class Progress(ScatterBlock):

        def provide_data(self, i, duration, frames_passed):
            return t[:i + 2], np.sin(t[:i + 2])

    if not builder:
        builder = animation.AnimationBuilder(interval=100)
    builder.add_block(Progress(duration=100, ax=axes, start=0))

    return builder


def demo_all():
    fig = plt.figure(figsize=(8, 8))
    ax1 = fig.add_subplot(2, 2, 1)
    ax2 = fig.add_subplot(2, 2, 2)
    ax3 = fig.add_subplot(2, 2, 3)
    ax4 = fig.add_subplot(2, 2, 4, projection='3d')

    builder = blocks_demo(ax1)
    builder = add_sin_demo(ax2, builder)
    builder = progress_demo(ax3, builder)
    builder = surface_3d_demo(ax4, builder)
    ani = builder.build_animation(fig)
    # html_utils.open_html(html_utils.get_js_html(ani))
    html_utils.open_html(html_utils.get_html_video(ani))



demo_all()
