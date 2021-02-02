import html_utils
import plt_utils
import animation_utils
import numpy as np
import matplotlib.pyplot as plt

from animation_utils import get_draw2D_action

fig, axes = plt.subplots(1, 1)
axes.set_ylim((-1.2, 1.2))

t = np.linspace(0, 10, 100)


def increase_frequency_data_provider_for_fill(i, duration, frames_passed):
    return t, np.zeros_like(t), np.sin(t * i / duration)


def increase_frequency_data_provider(i, duration, frames_passed):
    return t, np.sin(t * i / duration)


def decrease_frequency_data_provider(i, duration, frames_passed):
    return t, np.sin(t * (1 - i / duration))


pen = animation_utils.Pen(
    default_wargs={"color": "green", "alpha": 0.5},
    handle_update=lambda i, duration, frames_passed, ax, pen: pen.update_with_wargs(wargs={"alpha": i * 1.0 / duration},
                                                                                    reset=False)
)
animation_handler = animation_utils.AnimationHandler(interval=50)

animation_handler.add_action(
    action_lambda=get_draw2D_action(increase_frequency_data_provider_for_fill, type="fill_between"),
    duration=30,
    ax=axes,
    pen=pen
)

animation_handler.hold(hold_duration=15, ax=axes)
animation_handler.clear(ax=axes)

animation_handler.add_action(
    action_lambda=get_draw2D_action(decrease_frequency_data_provider, type="line"),
    pen=animation_utils.Pen(),
    start=10,
    duration=30,
    ax=axes
)

ani = animation_handler.build_animation(fig)
html_utils.open_html(html_utils.get_media_table([html_utils.get_html_video(ani), ""]))

# import abc
#
#
# class Episode:
#
#     def __init__(self, duration, ax):
#         self.duration = duration
#         self.ax = ax
#
#     @abc.abstractmethod
#     def provide_data(self, i, duration, frames_passed):
#         pass
#
#     @abc.abstractmethod
#     def update_figure(self, i, duration, frames_passed, ax, pen: animation_utils.Pen):
#         pass
#
# class Episode1(Episode):
#
#     def provide_data(i, duration, frames_passed):
#         return t, np.zeros_like(t), np.sin(t * i / duration)
#
#     def update_figure(i, duration, frames_passed, ax, pen):
#         pen.update_with_wargs(wargs={"alpha": i * 1.0 / duration},
#                               reset=False)