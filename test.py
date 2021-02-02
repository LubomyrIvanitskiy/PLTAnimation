import html_utils
import plt_utils
import animation_utils
import numpy as np
import matplotlib.pyplot as plt

from animation_utils import get_draw2D_action

fig, axes = plt.subplots(1, 1)
axes.set_ylim((-1.2, 1.2))

t = np.linspace(0, 10, 100)


def increase_frequency_data_provider(i, duration):
    print(f"inc. i={i}, dur={duration}")
    return t, np.sin(t * i / duration)


def decrease_frequency_data_provider(i, duration):
    print(f"dec. i={i}, dur={duration}")
    return t, np.sin(t * (1 - i / duration))


animation_handler = animation_utils.AnimationHandler(interval=200)

animation_handler.add_action(
    action_lambda=get_draw2D_action(increase_frequency_data_provider, type="scatter"),
    duration=30,
    ax=axes
)

animation_handler.hold(hold_duration=15, ax=axes)
animation_handler.clear(ax=axes)


animation_handler.add_action(
    action_lambda=get_draw2D_action(decrease_frequency_data_provider, type="line"),
    duration=30,
    ax=axes
)

ani = animation_handler.build_animation(fig)
html_utils.open_html(html_utils.get_media_table([html_utils.get_html_video(ani), ""]))
