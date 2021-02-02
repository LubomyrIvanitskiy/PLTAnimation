from matplotlib.collections import PathCollection, PolyCollection
from matplotlib.lines import Line2D

import abc


class Block:

    def __init__(self, duration, ax, start=None, clear_after_last=False):
        self.start = start
        self.duration = duration
        self.ax = ax
        self.last_artists = None
        self.clear_after_last = clear_after_last

    def is_last_frame(self, i):
        return i == self.duration - 1

    @abc.abstractmethod
    def provide_data(self, i, duration, frames_passed):
        pass

    @abc.abstractmethod
    def draw_figure(self, i, data, ax, last_artists):
        pass

    def update_figure(self, i, data, ax, last_artists):
        """
        Override this if you don't want to redraw plot and just update data instead
        """
        return self.draw_figure(i, data, ax, last_artists)

    def _plot(self, frames_passed):
        i = frames_passed - self.start
        data = self.provide_data(i, self.duration, frames_passed)

        has_previous_artists = self.last_artists is not None

        if has_previous_artists:
            artists = self.update_figure(i, data, self.ax, self.last_artists)
        else:
            artists = self.draw_figure(i, data, self.ax, self.last_artists)

        self.last_artists = artists
        if self.is_last_frame(i) and self.clear_after_last:
            self.clear()
        return self.last_artists

    def is_time(self, frames_passed):
        # if duration==0 we have deal with timeless actions and need to handle them as well
        res = self.duration == 0 and frames_passed == self.start
        res |= self.start <= frames_passed < self.start + self.duration

        return res

    def clear(self):
        has_previous_artists = self.last_artists is not None
        if has_previous_artists:
            if self.last_artists in self.ax.lines:
                self.ax.lines.remove(self.last_artists)
            elif self.last_artists in self.ax.collections:
                self.ax.collections.remove(self.last_artists)


class AnimationHandler:
    """
    Class for creating actions and stacking them together to be handled sequentially when animation is running
    """

    def __init__(self, interval):
        self.frames = 0
        self.interval = interval
        self.blocks = []
        self.time_ticks = []
        self.dead_blocks_count = 0

    def add_block(self, block):
        if not block.start:
            block.start = self.frames
            self.frames += block.duration
        else:
            action_end = block.start + block.duration
            if action_end > self.frames:
                self.frames = action_end

        self.blocks.append(block)

    def update(self, frames_passed):
        artists = None
        for block_index, block in enumerate(self.blocks[self.dead_blocks_count:]):
            if block.is_time(frames_passed):
                if artists is None:
                    artists = []
                result = block._plot(frames_passed)
                if result:
                    artists.append(result)
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
    has_previous_artists = last_artists is not None and isinstance(last_artists, PathCollection)
    if has_previous_artists:
        ax.collections.remove(last_artists)

    if has_previous_artists and not pen.is_updated:
        path = last_artists
        points = list(zip(x, y))
        path.set_offsets(points)
    else:
        path = ax.scatter(x, y, **pen.wargs)
    return path


def _plot_line(i, duration, frames_passed, ax, last_artists=None, data_provider=None, pen=None):
    x, y = data_provider(i, duration, frames_passed)

    has_previous_artists = last_artists is not None and isinstance(last_artists, Line2D)
    if has_previous_artists:
        ax.lines.remove(last_artists)

    if has_previous_artists and not pen.is_updated:
        line = last_artists
        line.set_data(x, y)
    else:
        line, = ax.plot(x, y, **pen.wargs)
        pen.reset_is_updated()
    return line


def _fill_between(i, duration, frames_passed, ax, last_artists=None, data_provider=None, pen=None):
    x, y1, y2 = data_provider(i, duration, frames_passed)
    # The best way is to redraw because updating vertices is too sophisticated especially if some interpolation
    # techniques are used
    if last_artists is not None:
        ax.collections.clear.remove(last_artists)
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
