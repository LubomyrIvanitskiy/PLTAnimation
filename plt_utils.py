from typing import Union, Type, List

import numpy as np
from matplotlib.artist import Artist
from matplotlib.collections import PolyCollection, PathCollection
from matplotlib.lines import Line2D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3D


def pure_text_label_plot(ax, text, color="black", fontsize=30):
    """
    Clear all ax ticks and ad single text label
    :param ax: subplot
    :param text: label to be shown in the center of the subplot
    :param color: text color
    :param fontsize: font size
    """
    ax.axis("off")
    ax.text(0.5, 0.5, text,
            fontsize=fontsize,
            color=color,
            horizontalalignment='center',
            verticalalignment='center')


def setup_ax(ax, title, legend=[""], ylim=(-1, 1)):
    """
    Setup subplot title legend and ylim at once
    :param ax:
    :param title:
    :param legend:
    :param ylim: a tuple with bottom/upper y limits
    :return:
    """
    ax.set_title(title)
    ax.set_xlabel("x")
    ax.set_ylim(ylim[0], ylim[1])
    ax.legend(legend)


def clear_axes(axes):
    """
    Clear all artists drawn on subplots
    :param axes: axes object returned from plt.subplots
    """
    flat_op = getattr(axes, "flat", None)
    if callable(flat_op):
        for ax in axes.flat:
            ax.finish()
    else:
        try:
            axes.finish()
        except Exception:
            pass


def draw_cross_like_axises(axes):
    """
    Draw axises crossed in the center of the screen
    :param axes: axes object returned by plt.subplots
    :return:
    """
    for ax in axes:
        ax.spines['left'].set_position('zero')
        ax.spines['right'].set_color('none')
        ax.spines['bottom'].set_position('zero')
        ax.spines['top'].set_color('none')
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')


def two_color_fill(x, y, ax):
    """
    Draw a plot with area under (negative) and above zero (positive) filled with different colors
    :param x: independent data
    :param y: dependent data
    :param ax: subplot from plt.subplots
    :return: '.PolyCollection`
            A `.PolyCollection` containing the plotted polygons of negative and positive plots
    """
    ax.plot(x, y, color="gray", alpha=.5)
    line1 = ax.fill_between(x, 0, y.clip(min=0), color="pink", alpha=.5)
    line2 = ax.fill_between(x, 0, y.clip(max=0), color="blue", alpha=.3)
    return line1, line2


def fill_color_difference(x, y1, y2, ax, colors=["blue", "pink"]):
    """
        Draw two plots with filled area between them.
        Where y1>y2 (positive area) the color is 'colors[0]'
        Where y2>y1 (negative area) the color is 'colors[1]'
        :param x: independent data
        :param y: dependent data
        :param ax: subplot from plt.subplots
        :param colors: (Optional) override default colors for positive and negative areas
        :return: '.PolyCollection`
                A `.PolyCollection` containing the plotted polygons of negative and positive plots
        """
    line1 = ax.fill_between(x, y1, [y2[i] if y2[i] > y1[i] else y1[i] for i in range(len(y1))], color=colors[0],
                            alpha=.2)
    line2 = ax.fill_between(x, y2, [y1[i] if y1[i] > y2[i] else y2[i] for i in range(len(y1))], color=colors[1],
                            alpha=.2)
    return line1, line2


def draw_arrow_with_text(ax, xyfrom, xyto, text=None):
    """
    :param ax: subplot returned by plt.subplots
    :param xyfrom: (x, y) tuple - arrow start
    :param xyto: (x, y) tuple - arrow end
    :param text: text to be located under the arrow
    """
    if text is None:
        text = str(np.sqrt((xyfrom[0] - xyto[0]) ** 2 + (xyfrom[1] - xyto[1]) ** 2))
    ax.annotate("", xyfrom, xyto, arrowprops=dict(arrowstyle='<->'))
    ax.text((xyto[0] + xyfrom[0]) / 2, (xyto[1] + xyfrom[1]) / 2, text, fontsize=16)


# Helper methods to update already existing plot instead of fully redrawing it

def update_line(line_patch: Union[Line2D, Line3D], x, y, z=None) -> Union[Line2D, Line3D]:
    if z is not None:
        line_patch.set_data_3d(x, y, z)
    else:
        line_patch.set_data(x, y)
    return line_patch


def update_scatter(scatter_patch: PathCollection, x, y, z=None) -> PathCollection:
    if z is not None:
        scatter_patch._offsets3d = (x, y, z)
    else:
        points = list(zip(x, y))
        scatter_patch.set_offsets(points)
    return scatter_patch


def copy_fillbetween_vertices(from_fill_between_patch: PolyCollection, to_fill_between_patch: PolyCollection):
    to_fill_between_patch.get_paths()[0].vertices = from_fill_between_patch.get_paths()[0].vertices
    return to_fill_between_patch


def copy_surface3d_vertices(from_surface_patch: Poly3DCollection, to_surface_patch: Poly3DCollection):
    to_surface_patch._vec = from_surface_patch._vec
    to_surface_patch._segslices = from_surface_patch._segslices
    return to_surface_patch


def remove_patches(axes, patches: List[Type[Artist]]):
    for patch in patches:
        if patch in axes.lines:
            axes.lines.remove(patch)
        elif patch in axes.collections:
            axes.collections.remove(patch)
