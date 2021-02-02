from matplotlib.collections import PathCollection, PolyCollection
from matplotlib.lines import Line2D


class Action:

    def __init__(self, action, start, duration, ax, pen=None):
        self.action = action
        self.start = start
        self.pen = pen
        self.duration = duration
        self.ax = ax
        self.last_artists = None

    def __call__(self, frames_passed):
        if self.pen:
            self.pen.on_update(frames_passed - self.start, frames_passed=frames_passed, duration=self.duration,
                               ax=self.ax)
        self.last_artists = self.action(frames_passed - self.start, frames_passed=frames_passed,
                                        duration=self.duration,
                                        ax=self.ax, last_artists=self.last_artists, pen=self.pen)
        return self.last_artists

    def is_time(self, frames_passed):
        # if duration==0 we have deal with timeless actions and need to handle them as well
        res = self.duration == 0 and frames_passed == self.start
        res |= self.start <= frames_passed < self.start + self.duration

        return res


class Pen:
    """
    Class that holds wargs for plotting figures
    """

    def __init__(self, default_wargs={"color": "red"}, handle_update=None):
        self.wargs = default_wargs
        self.handle_update = handle_update
        self.is_updated = False

    def update_with_wargs(self, wargs, reset=False):
        if reset:
            self.wargs = wargs
        else:
            self.wargs.update(wargs)

    def on_update(self, i, duration, frames_passed, ax):
        if self.handle_update:
            self.handle_update(i, duration, frames_passed, ax, self)
            self.is_updated = True

    def reset_is_updated(self):
        self.is_updated = False


class AnimationHandler:
    """
    Class for creating actions and stacking them together to be handled sequentially when animation is running
    """

    def __init__(self, interval):
        self.frames = 0
        self.interval = interval
        self.actions = []
        self.time_ticks = []
        self.dead_actions_count = 0

    def add_action(self, action_lambda, duration, ax, pen=None, start=None):
        if not start:
            start = self.frames
            self.frames += duration
        else:
            action_end = start + duration
            if action_end > self.frames:
                self.frames = action_end
        action = Action(action_lambda, start, duration, ax, pen)
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
        prev_action = self.actions[-1]

        def draw_last_frame(i, duration, frames_passed, ax, last_artists, pen=None):
            return prev_action.action(prev_action.duration, prev_action.duration, frames_passed, ax, last_artists, pen)

        start = self.frames
        self.frames += hold_duration
        action = Action(action=draw_last_frame,
                        start=start,
                        duration=hold_duration,
                        ax=ax,
                        pen=Pen(
                            prev_action.pen.wargs,
                            handle_update=lambda i, duration, frames_passed, ax, pen:
                            prev_action.pen.on_update(prev_action.duration, prev_action.duration, frames_passed, ax)
                        )
                        )
        self._add_action(action)

    def clear(self, ax):
        """
        Stack a frame for number of iterations = duration
        """
        assert len(self.actions) > 0

        def clear(i, duration, frames_passed, ax, last_artists, pen=None):
            ax.lines.clear()
            ax.collections.clear()
            return None

        action = Action(action=clear, start=self.frames, duration=0, ax=ax)
        self._add_action(action)

    def update(self, frames_passed):
        artists = None
        for action_index, action in enumerate(self.actions[self.dead_actions_count:]):
            if action.is_time(frames_passed):
                if artists is None:
                    artists = []
                result = action(frames_passed)
                if result:
                    artists.append(result)
            # else:
            #     self.dead_actions_count = action_index
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

def _plot_scatter(i, duration, frames_passed, ax, last_artists=None, data_provider=None, pen=None):
    x, y = data_provider(i, duration, frames_passed)
    if last_artists is not None and isinstance(last_artists, PathCollection) and not pen.is_updated:
        path = last_artists
        points = list(zip(x, y))
        path.set_offsets(points)
    else:
        ax.collections.clear()
        path = ax.scatter(x, y, **pen.wargs)
    return path


def _plot_line(i, duration, frames_passed, ax, last_artists=None, data_provider=None, pen=None):
    x, y = data_provider(i, duration, frames_passed)
    if last_artists is not None and isinstance(last_artists, Line2D) and not pen.is_updated:
        line = last_artists
        line.set_data(x, y)
    else:
        ax.lines.clear()
        line, = ax.plot(x, y, **pen.wargs)
        pen.reset_is_updated()
    return line


def _fill_between(i, duration, frames_passed, ax, last_artists=None, data_provider=None, pen=None):
    x, y1, y2 = data_provider(i, duration, frames_passed)
    # The best way is to redraw because updating vertices is too sophisticated especially if some interpolation
    # techniques are used
    ax.collections.clear()
    wargs = pen.wargs if pen else {"color": "blue"}
    poly_collection = ax.fill_between(x, y1, y2, **wargs)
    return poly_collection


def get_draw2D_action(data_provider, type="line"):
    """
    :param data_provider: a function that get frame_index and return x and y to be drawn with axes.plot() function
    :param type: line, scatter, fill_between
    :return: Action for drawing animation
    """

    def get_action(method):
        return lambda i, duration, frames_passed, ax, last_artists, pen: method(i, duration, frames_passed, ax,
                                                                                last_artists,
                                                                                data_provider,
                                                                                pen)

    if type == "scatter":
        return get_action(_plot_scatter)
    if type == "fill_between":
        return get_action(_fill_between)
    else:
        return get_action(_plot_line)
