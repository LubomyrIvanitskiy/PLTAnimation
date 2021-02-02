import html_utils
import animation_utils
import numpy as np
import matplotlib.pyplot as plt

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
            wargs={"alpha": i * 1.0 / duration, "color": "purple"},
            reset=False
        )


animation_handler.add_episode(Episode1(0, 30, axes))
# animation_handler.add_episode(Episode1(5, 30, axes))

animation_handler.hold(15, axes)
# animation_handler.add_episode(Episode2(10, 30, axes))

ani = animation_handler.build_animation(fig)
html_utils.open_html(html_utils.get_media_table([html_utils.get_html_video(ani), ""]))
