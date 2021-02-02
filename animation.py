from animation_utils import AnimationHandler
from plt_utils import two_color_fill, setup_ax, draw_arrow_with_text, clear_axes


def show_transformation_animation(f, title_prefix="", figsize=(10, 5), transformations=["amp", "freq", "phase"],
                                  annotate=True):
    fig, ax = plt.subplots(figsize=figsize)
    t = np.linspace(0, 4 * np.pi, 500)
    line1, line2 = two_color_fill(t, np.sin(t), ax)

    start = 10

    A = 1
    p = 0
    w = 1

    def plot_sine(ax, t=t, A=A, w=w, p=p, title=""):
        setup_ax(ax, title)
        two_color_fill(t, f(A, t, w, p), ax)
        if annotate:
            draw_arrow_with_text(ax, [np.pi / 2 / w - p, 0], [np.pi / 2 / w - p, A], 'A')
            draw_arrow_with_text(ax, [-p, 0], [2 * np.pi / w - p, 0], '$1/\omega$')
            draw_arrow_with_text(ax, [0, 0], [-p, 0], '$\phi$')

    frames = 45*len(transformations)
    animation_handler = AnimationHandler(frames=frames, interval=100)

    ### CHANGE FREQUENCY ###
    if "freq" in transformations:
        animation_handler.add_action(
            action=lambda i: plot_sine(ax, w=(start + i) / 10,
                                       title=f"{title_prefix}Зміна частоти, $\omega$={((start + i) / 10):0.2f}"),
            duration=15
        )
        animation_handler.add_action(
            action=lambda i: plot_sine(ax, w=(15 + start - i) / 10,
                                       title=f"{title_prefix}Зміна частоти, $\omega$={((15 + start - i) / 10):0.2f}"),
            duration=15
        )
        animation_handler.hold(15)

    ### CHANGE AMPLITUDE ###
    if "amp" in transformations:
        animation_handler.add_action(
            action=lambda i: plot_sine(ax, A=(15 - i) / 15,
                                       title=f"{title_prefix}Зміна амплітуди, A={((15 - i) / 15):0.2f}"),
            duration=15
        )
        animation_handler.add_action(
            action=lambda i: plot_sine(ax, A=1 - (15 - i) / 15,
                                       title=f"{title_prefix}Зміна амплітуди, A={(1 - (15 - i) / 15):0.2f}"),
            duration=15
        )
        animation_handler.hold(15)

    ### CHANGE PHASE ###
    if "phase" in transformations:
        animation_handler.add_action(
            action=lambda i: plot_sine(ax, p=-i * np.pi / 15,
                                       title=f"{title_prefix}Зміна фази, $\phi$={(i * np.pi / 15):0.2f}"),
            duration=15
        )
        animation_handler.add_action(
            action=lambda i: plot_sine(ax, p=-(np.pi - i * np.pi / 15),
                                       title=f"{title_prefix}Зміна фази, $\phi$={(1 - i * np.pi / 15):0.2f}"),
            duration=15
        )
        animation_handler.hold(15)

    ani = animation_handler.build_animation()
    return ani


#############

fig, ax = plt.subplots(figsize=(10, 5))
N = 100
t = np.linspace(0, 2 * np.pi, N)

base = np.zeros(t.shape[0])

add_duration = 10
transform_duration = 20
replace_duration = 10
tact_duration = add_duration + transform_duration + replace_duration
h_count = 10

As = np.ones((h_count,))
As[np.arange(1, h_count, 2)] = -1
ws = np.arange(1, h_count + 1)
bs = np.zeros((h_count,))


def create_hs_lambda(A, w, b, i):
    return lambda t: A * np.sin(w * t + b)


hs = [create_hs_lambda(A, w, b, i) for i, (A, w, b) in enumerate(zip(As, ws, bs))]

result_plot = np.sum([hs[i](t) for i in range(len(hs))], axis=1)
plt.plot(result_plot)
plt.show()

ylim = (-max(As) * h_count, max(As) * h_count)
print(f"ylim = {ylim}")


def add_new_sin(t, f, i, duration, title=""):
    global base
    setup_ax(ax, title, ylim=ylim)
    ax.plot(t, base, c="black")
    ax.plot(t, np.zeros(t.shape[0]), linestyle="dotted", c="blue")
    ax.plot(t, f(t), alpha=i / duration, c="blue")


def transform_sin(t, f, i, duration, title=""):
    global base
    setup_ax(ax, title, ylim=ylim)
    ax.plot(t, base, c="black")
    # ax.plot(t, (i/duration)*base+np.zeros(t.shape[0])+(max(base)-max(base)*i/duration), linestyle="dotted", c="blue")
    # ax.plot(t, (i/duration)*base+f(t)+(max(base)-max(base)*i/duration), c="blue")
    ax.plot(t, (i / duration) * base + np.zeros(t.shape[0]), linestyle="dotted", c="blue")
    ax.plot(t, (i / duration) * base + f(t), c="blue")


def change_base(t, f, i, duration, title=""):
    global base
    setup_ax(ax, title, ylim=ylim)
    ax.plot(t, base, alpha=1 - i / duration, c="black")
    ax.plot(t, base + f(t), c=(0, 0, 1 - i / duration))
    if i == duration:
        base = base + f(t)


animation_handler = AnimationHandler(frames=h_count * tact_duration, interval=50)


def create_add_action(index):
    return lambda i: add_new_sin(t, hs[index], i, add_duration)


def create_transform_action(index):
    return lambda i: transform_sin(t, hs[index], i, transform_duration)


def create_replace_action(index):
    return lambda i: change_base(t, hs[index], i, replace_duration)


for k in range(h_count):
    animation_handler.add_action(
        action=create_add_action(k),
        duration=add_duration
    )

    animation_handler.add_action(
        action=create_transform_action(k),
        duration=transform_duration
    )

    animation_handler.add_action(
        action=create_replace_action(k),
        duration=replace_duration
    )



ani = animation_handler.build_animation()

###########

import numpy as np
import matplotlib.pyplot as plt

default_colors = ["blue", "green", "red", "grey", "orange", "pink"]


def animate_complex_plane(t,
                          signal_func,
                          complex_freq,
                          frames,
                          mode,
                          speed_factor=1,
                          draw_tape=False,
                          fixed_angle=None,
                          title=False,
                          draw_zero=False,
                          fig_size=(6, 6),
                          colors=default_colors,
                          sequentually=False,
                          fade_out=True,
                          limits=None):
    if not hasattr(signal_func, '__iter__'):
        signal_func = [signal_func]

    chunk_size = 1
    if sequentually:
        chunk_size = frames / len(signal_func)
        speed_factor *= len(signal_func)

    from matplotlib import animation, rc

    fig = plt.figure(figsize=fig_size)

    ax = plt.axes(projection='3d')
    if not limits:
        ax.set_zlim(-1.2, 1.2)
        ax.set_ylim(-1.2, 1.2)
        ax.set_xlim(0, np.max(t))
    else:
        ax.set_zlim(limits[0], limits[1])
        ax.set_ylim(limits[2], limits[3])
        ax.set_xlim(limits[4], limits[5])

    def draw_shadows(f):
        complex_sin = np.exp(1j * complex_freq * t) * f(t)
        real_proj = np.real(complex_sin)
        imag_proj = np.imag(complex_sin)
        line, = ax.plot(t, real_proj, np.zeros((len(t),)) - 1, linewidth=1, label="Real part cos(w)", c="orange");
        line, = ax.plot(t, np.zeros((len(t),)) + 1, imag_proj, linewidth=1, label="Imaginary part sin(w)", c="blue");
        return line

    def draw_base(f):
        complex_sin = np.exp(1j * complex_freq * t) * f(t)
        complex_sin_line, = ax.plot(t, np.real(complex_sin), np.imag(complex_sin), linewidth=0.5, label="Complex sin",
                                    c="black");
        return complex_sin_line

    def draw_zero():
        line, = ax.plot(t, np.zeros((len(t),)), np.zeros((len(t),)), linewidth=1, label="Time axis", c="grey");
        return line

    plt.legend()

    def plot_tape(ax, intensity):
        y = np.arange(-1.1, 1.1, 0.1)
        X, Y = np.meshgrid(t, y)
        R = np.exp(1j * X * intensity) * Y
        surf = ax.plot_surface(X, np.real(R), np.imag(R), alpha=0.4, color="lightgray",
                               linewidth=0, antialiased=False)
        return surf

    def init():
        ax.collections.clear()
        return []

    def updatefig_hor(angle):
        a = angle * speed_factor
        if a <= 90:
            ax.view_init(0, -a)
        line = draw_base(signal_func[-1])
        line = draw_shadows(signal_func[-1])
        if draw_zero:
            draw_zero()
        return line

    def updatefig_ver(angle):
        a = angle * speed_factor
        if a <= 90:
            ax.view_init(a, 0)
        line = draw_base(signal_func[-1])
        line = draw_shadows(signal_func[-1])
        if draw_zero:
            draw_zero()
        return line

    def updatefig_progress(i):
        ax.collections.clear()
        ax.lines.clear()
        # draw last signal shadows
        if draw_zero:
            draw_zero()

        if sequentually:
            upper_f_index = int(i // chunk_size)
            line = draw_shadows(signal_func[upper_f_index])
            i = int(i % chunk_size)
        else:
            upper_f_index = len(signal_func) - 1
            line = draw_shadows(signal_func[-1])

        for f_index, f in enumerate(signal_func[:upper_f_index + 1]):
            complex_sin = np.exp(1j * complex_freq * t) * f(t)
            if f_index == upper_f_index:
                upper = min(i * speed_factor, len(t))
            else:
                upper = len(t)
            if fade_out:
                alpha = (f_index + 1) / (upper_f_index + 1)
            else:
                alpha = 1
            complex_sin_line, = ax.plot(t[:upper], np.real(complex_sin)[:upper], np.imag(complex_sin)[:upper],
                                        linewidth=1, label="Complex sin", alpha=alpha, c=colors[f_index]);
            ax.scatter([t[upper - 1]], [np.real(complex_sin)[upper - 1]], [np.imag(complex_sin)[upper - 1]],
                       c=colors[f_index], alpha=alpha);

        if draw_tape:
            surf = plot_tape(ax, complex_freq)
        else:
            surf = None
        if fixed_angle:
            ax.view_init(fixed_angle[0], fixed_angle[1])

        return complex_sin_line, surf

    def twist(i):
        ax.collections.clear()
        ax.lines.clear()
        line = None

        if fixed_angle:
            ax.view_init(fixed_angle[0], fixed_angle[1])
        if draw_zero:
            draw_zero()

        twist_intensity = 1.0 * i / 20

        for f in signal_func:
            complex_sin = np.exp(1j * t * (complex_freq * twist_intensity)) * f(t)
            complex_sin_line, = ax.plot(t, np.real(complex_sin), np.imag(complex_sin), linewidth=1, label="Complex sin",
                                        c="blue");
            t0 = np.mean(t)
            dot = np.exp(1j * t0 * (complex_freq * twist_intensity)) * f(t0)
            ax.scatter([t0], [np.real(dot)], [np.imag(dot)], label="dot", c="orange");

        if draw_tape:
            surf = plot_tape(ax, twist_intensity)
        else:
            surf = None
        if title:
            plt.title(f"Амплітудна модуляція (комплексне скурчування) різною частотою\ne^i{twist_intensity:.2f}*signal")

        return surf, complex_sin_line

    if mode == "progress":
        update_func = updatefig_progress
    elif mode == "vertical":
        update_func = updatefig_ver
    elif mode == "horisontal" or mode == "horizontal":
        update_func = updatefig_hor
    elif mode == "twist":
        update_func = twist

    ani = animation.FuncAnimation(fig, update_func, init_func=init, frames=frames, interval=150, blit=False)
    video = ani.to_html5_video()
    return video

#############
