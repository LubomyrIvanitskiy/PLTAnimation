import abc

import html_utils
import animation_utils
import numpy as np
import matplotlib.pyplot as plt


def simple_demo():
    fig, axes = plt.subplots(1, 1)
    axes.set_ylim((-1.2, 1.2))

    t = np.linspace(0, 10, 100)

    animation_handler = animation_utils.AnimationHandler(interval=100)

    class Episode1(animation_utils.Episode):

        def get_plot_type(self):
            return "line"

        def provide_data(self, i, duration, frames_passed):
            return t, np.sin(t * i / duration)

        def update_figure(self, i, duration, frames_passed, ax, pen):
            pen.update_with_wargs(
                wargs={"alpha": i * 1.0 / duration, "color": "purple"},
                reset=False
            )

    class Episode2(animation_utils.Episode):

        def get_plot_type(self):
            return "scatter"

        def provide_data(self, i, duration, frames_passed):
            return t, np.sin(t * i / duration)

        def update_figure(self, i, duration, frames_passed, ax, pen):
            pen.update_with_wargs(
                wargs={"alpha": i * 1.0 / duration, "color": (1.0 / duration, 0, 1.0 / duration)},
                reset=False
            )

    animation_handler.add_episode(Episode1(duration=30, ax=axes, start=0))
    animation_handler.add_episode(Episode1(duration=30, ax=axes, start=5))

    animation_handler.hold(15, axes)
    animation_handler.add_episode(Episode2(duration=30, ax=axes, start=10))

    ani = animation_handler.build_animation(fig)
    html_utils.open_html(html_utils.get_media_table([html_utils.get_html_video(ani), ""]))


# simple_demo()

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

    class Appearance(animation_utils.Episode):

        def __init__(self, h, duration, ax, start=None):
            super().__init__(duration, ax, start)
            self.h = h

        def get_plot_type(self):
            return "line"

        def provide_data(self, i, duration, frames_passed):
            return t, self.h

        def update_figure(self, i, duration, frames_passed, ax, pen):
            pen.update_with_wargs(
                wargs={"alpha": i * 1.0 / duration},
                reset=False
            )

    class Transformation(animation_utils.Episode):

        def __init__(self, base, h, duration, ax, start=None):
            super().__init__(duration, ax, start)
            self.base = base
            self.h = h

        def get_plot_type(self):
            return "line"

        def provide_data(self, i, duration, frames_passed):
            return t, (i / duration) * self.base + h

        def update_figure(self, i, duration, frames_passed, ax, pen):
            pen.update_with_wargs(
                wargs={"alpha": i * 1.0 / duration},
                reset=False
            )

    class Disappear(animation_utils.Episode):

        def __init__(self, h, duration, ax, start=None):
            super().__init__(duration, ax, start)
            self.h = h

        def get_plot_type(self):
            return "line"

        def provide_data(self, i, duration, frames_passed):
            return t, h

        def update_figure(self, i, duration, frames_passed, ax, pen):
            pen.update_with_wargs(
                wargs={"alpha": i * (1 - 1.0 / duration)},
                reset=False
            )

    frame_duration = 20
    for i, h in enumerate(hs):
        # if i > 0:
        #     animation_handler.add_episode(Disappear(start=i * frame_duration, duration=frame_duration, ax=axes, h=hs[i-1]))
        animation_handler.add_episode(Appearance(start=i * frame_duration, duration=frame_duration, ax=axes, h=h))
        animation_handler.add_episode(
            Transformation(duration=frame_duration, ax=axes, base=np.sum(hs[:i], axis=0),
                           h=h))
    ani = animation_handler.build_animation(fig)
    html_utils.open_html(html_utils.get_media_table([html_utils.get_html_video(ani), ""]))


# add_sin_demo()

def blocks_demo():
    fig, axes = plt.subplots(1, 1)
    axes.set_ylim((-1.2, 1.2))

    t = np.linspace(0, 10, 100)

    class LineBlock(animation_utils.Block):

        def provide_data(self, i, duration, frames_passed):
            return t, np.sin(t * i / duration)

        def draw_figure(self, i, data, ax, last_artists):
            x, y = data
            line, = ax.plot(x, y)
            return line

        def update_figure(self, i, data, ax, last_artists):
            if last_artists is None:
                return super().update_figure(data, ax, last_artists)
            x, y = data
            last_artists.set_data(x, y)
            last_artists.set_alpha(i / self.duration)
            return last_artists

    class ScatterBlock(animation_utils.Block):

        def provide_data(self, i, duration, frames_passed):
            return t, np.sin(t * i / duration)

        def draw_figure(self, i, data, ax, last_artists):
            x, y = data
            path = ax.scatter(x, y)
            return path

        def update_figure(self, i, data, ax, last_artists):
            if last_artists is None:
                return super().update_figure(data, ax, last_artists)
            path = last_artists
            x, y = data
            points = list(zip(x, y))
            path.set_offsets(points)

            return path

    class FillBlock(animation_utils.Block):

        def provide_data(self, i, duration, frames_passed):
            return t, np.zeros_like(t), np.sin(t * i / duration)

        def draw_figure(self, i, data, ax, last_artists):
            x, y1, y2 = data
            self.clear()
            poly_collection = ax.fill_between(x, y1, y2, color="red")
            return poly_collection

    animation_handler = animation_utils.AnimationHandler(interval=100)

    animation_handler.add_block(LineBlock(duration=20, ax=axes, start=0, clear_after_last=True))
    animation_handler.add_block(ScatterBlock(duration=20, ax=axes, start=5))
    animation_handler.add_block(FillBlock(duration=20, ax=axes, start=10))

    ani = animation_handler.build_animation(fig)
    html_utils.open_html(html_utils.get_media_table([html_utils.get_html_video(ani), ""]))


blocks_demo()
