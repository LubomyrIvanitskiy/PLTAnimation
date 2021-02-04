from animation import Block, AnimationBuilder
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt


class Rotation(Block):

    def __init__(self, start_angle, deltas, axes, *args, **kwargs):
        super(Rotation, self).__init__(*args, **kwargs)
        self.start_angle = start_angle
        self.deltas = deltas
        self.axes = axes

    def on_frame(self, progress, last_patches, **kwargs):
        self.axes.view_init(
            self.start_angle[0] + self.deltas[0] * progress,
            self.start_angle[1] + self.deltas[1] * progress
        )
        return None


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

X, Y, Z = axes3d.get_test_data(0.05)

ax.plot_wireframe(X, Y, Z, rstride=10, cstride=10)

builder = AnimationBuilder()
builder.add_block(Rotation(start_angle=(20, 10), deltas=(0, 360), axes=ax, duration=50))
anim = builder.build_animation(fig)
plt.show()
