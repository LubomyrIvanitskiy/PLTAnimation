import abc

from animation import Block


class LineBlock(Block):

    @abc.abstractmethod
    def provide_data(self, i, duration, frames_passed):
        pass

    def on_frame(self, i, data, ax, last_artists, **kwargs):
        x, y = data
        line, = ax.plot(x, y)
        return line

    def update_figure(self, i, data, ax, last_artists):
        if last_artists is None:
            return super().update_figure(data, ax, last_artists)
        x, y = data
        last_artists.set_data(x, y)
        return last_artists


class ScatterBlock(Block):

    @abc.abstractmethod
    def provide_data(self, i, duration, frames_passed):
        pass

    def on_frame(self, i, data, ax, last_artists, **kwargs):
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


class FillBlock(Block):

    @abc.abstractmethod
    def provide_data(self, i, duration, frames_passed):
        pass

    def on_frame(self, i, data, ax, last_artists, **kwargs):
        x, y1, y2 = data
        if 'from_update' in kwargs and kwargs.get('from_update'):
            poly_collection = ax.fill_between(x, y1, y2, color="grey", alpha=0.0)
        else:
            poly_collection = ax.fill_between(x, y1, y2)
        return poly_collection

    def update_figure(self, i, data, ax, last_artists):
        if last_artists is None:
            return super().update_figure(data, ax, last_artists)
        new_collection = self.on_frame(i, data, ax, last_artists, from_update=True)
        # Here we want to change only the vertices and keep other parameters (like size or color) the same
        last_artists.get_paths()[0].vertices = new_collection.get_paths()[0].vertices
        ax.collections.remove(new_collection)
        return last_artists


class Line3DBlock(Block):

    @abc.abstractmethod
    def provide_data(self, i, duration, frames_passed):
        pass

    def on_frame(self, i, data, ax, last_artists, **kwargs):
        x, y, z = data
        line, = ax.plot(x, y, z)
        return line

    def update_figure(self, i, data, ax, last_artists):
        if last_artists is None:
            return super().update_figure(data, ax, last_artists)
        x, y, z = data
        last_artists.set_data_3d(x, y, z)
        return last_artists

from matplotlib import cm

class Surface3DBlock(Block):

    @abc.abstractmethod
    def provide_data(self, i, duration, frames_passed):
        pass

    def on_frame(self, i, data, ax, last_artists, **kwargs):
        x, y, z = data
        surface = ax.plot_surface(x, y, z, cmap=cm.coolwarm)
        return surface

    def update_figure(self, i, data, ax, last_artists):
        if last_artists is None:
            return super().update_figure(data, ax, last_artists, for_update=True)
        new_poly3dcollection = self.on_frame(i, data, ax, last_artists, from_update=True)
        last_artists.set_verts(new_poly3dcollection._paths)
        ax.collections.remove(new_poly3dcollection)

        last_artists._vec = new_poly3dcollection._vec
        last_artists._segslices = new_poly3dcollection._segslices

        # last_artists.set_facecolor(new_poly3dcollection.get_facecolor())
        return last_artists


class ProjectionRotation(Block):

    def __init__(self, initial_angle, angle_delta, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial_angle = initial_angle
        self.angle_delta = angle_delta

    def on_frame(self, i, data, ax, last_artists, **kwargs):
        ax.view_init(self.initial_angle[0] - self.angle_delta[0] * self.get_progress(i),
                     self.initial_angle[1] - self.angle_delta[1] * self.get_progress(i))
