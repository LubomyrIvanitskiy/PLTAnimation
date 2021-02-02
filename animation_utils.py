from matplotlib.collections import PathCollection
from matplotlib.lines import Line2D


class Action:

    def __init__(self, action, duration, ax):
        self.action = action
        self.duration = duration
        self.ax = ax

    def __call__(self, i, last_artists):
        return self.action(i, duration=self.duration, ax=self.ax, last_artists=last_artists)


class AnimationHandler:
    """
    Class for creating actions and stacking them together to be handled sequentially when animation is running
    """

    def __init__(self, interval):
        self.frames = 0
        self.interval = interval
        self.last_artists = None
        self.actions = []
        self.time_ticks = []
        self.timeless_actions = {}

    def _register_timeless_action(self, i, action):
        """
        Register actions that has no duration
        :param i: time
        :return:
        """
        actions = self.timeless_actions[i] if i in self.timeless_actions else []
        actions.append(action)
        self.timeless_actions[i] = actions

    def add_action(self, action_lambda, duration, ax):
        self.frames += duration
        action = Action(action_lambda, duration, ax)
        assert action.duration >= 1
        self._add_action(action)

    def _add_action(self, action):
        self.actions.append(action)
        if len(self.time_ticks) == 0:
            self.time_ticks.append(action.duration)
        else:
            self.time_ticks.append(self.time_ticks[-1] + action.duration)

    def hold(self, hold_duration, ax):
        """
        Stack a frame for number of iterations = duration
        """
        assert len(self.actions) > 0
        prev_prev_tick = self.time_ticks[-2] if len(self.time_ticks) > 1 else 0
        prev_action = self.actions[-1]
        prev_tick = self.time_ticks[-1]
        prev_action_duration = prev_tick - prev_prev_tick

        def draw_last_frame(i, duration, ax, last_artists):
            return prev_action.action(prev_action_duration, prev_action_duration, ax, last_artists)

        self.frames += hold_duration
        action = Action(draw_last_frame, hold_duration, ax)
        self._add_action(action)

    def clear(self, ax):
        """
        Stack a frame for number of iterations = duration
        """
        assert len(self.actions) > 0

        def clear(i, duration, ax, last_artists):
            ax.lines.clear()
            ax.collections.clear()
            return []

        action = Action(clear, 0, ax)
        self._register_timeless_action(self.frames, action)

    def update(self, global_tick):
        prev_time_tick = 0
        artists = []
        for action, time_tick in zip(self.actions, self.time_ticks):
            # Handle timeless actions
            if global_tick in self.timeless_actions:
                timeless_actions = self.timeless_actions[global_tick]
                for ta in timeless_actions:
                    ta(global_tick - prev_time_tick, self.last_artists)
            if global_tick < time_tick:
                # pass relative i
                self.last_artists = action(global_tick - prev_time_tick, self.last_artists)
                artists.append(self.last_artists)
                return artists
            else:
                prev_time_tick = time_tick
        return artists

    def build_animation(self, fig):
        from matplotlib import animation
        ani = animation.FuncAnimation(
            fig=fig,
            func=self.update,
            frames=self.frames,
            interval=self.interval,
            blit=True)
        return ani


# <<< Helper methods >>>

def _plot_scatter(i, duration, ax, last_artists=None, data_provider=None):
    x, y = data_provider(i, duration)
    if last_artists is not None and isinstance(last_artists, PathCollection):
        path = last_artists
        points = list(zip(x, y))
        path.set_offsets(points)
    else:
        ax.collections.clear()
        path = ax.scatter(x, y, c="blue")
    return path


def _plot_line(i, duration, ax, last_artists=None, data_provider=None):
    x, y = data_provider(i, duration)
    if last_artists is not None and isinstance(last_artists, Line2D):
        line = last_artists
        line.set_data(x, y)
    else:
        ax.lines.clear()
        line, = ax.plot(x, y, c="blue")
    return line


def get_draw2D_action(data_provider, type="line"):
    """
    :param data_provider: a function that get frame_index and return x and y to be drawn with axes.plot() function
    :param type: line, scatter
    :return: Action for drawing animation
    """
    if type == "scatter":
        return lambda i, duration, ax, last_artists: _plot_scatter(i, duration, ax, last_artists,
                                                                   data_provider)
    else:
        return lambda i, duration, ax, last_artists: _plot_line(i, duration, ax, last_artists,
                                                                data_provider)
