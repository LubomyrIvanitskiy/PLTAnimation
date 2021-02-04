import abc


class Block:

    def __init__(self, duration, start=None, predecessor_block=None, **kwargs):
        self.start = start
        self.duration = duration
        self.predecessor_block = predecessor_block
        self._last_patches = None

    @abc.abstractmethod
    def on_frame(self, progress, last_patches, **kwargs):
        pass

    def finish(self, last_patches):
        pass

    def _draw(self, frames_passed):
        frames_since_start = frames_passed - self.start
        progress = self.get_progress(frames_since_start)

        if self._last_patches is None and self.predecessor_block is not None:
            self._last_patches = self.predecessor_block._last_patches

        patches = self.on_frame(progress, self._last_patches)

        self._last_patches = patches
        if frames_since_start == self.duration - 1:
            self.finish(self._last_patches)
        return self._last_patches

    def is_alive(self, frames_passed):
        # if duration==0 we have deal with timeless actions and need to handle them as well
        res = self.duration == 0 and frames_passed == self.start
        res |= self.start <= frames_passed < self.start + self.duration

        return res

    def get_progress(self, i):
        return (i + 1) / self.duration if self.duration > 0 else 1


class AnimationBuilder:
    """
    Class for creating actions and stacking them together to be handled sequentially when animation is running
    """

    def __init__(self, interval=100):
        self.frames = 0
        self.interval = interval
        self.blocks = []
        self.dead_blocks_count = 0

    def add_block(self, block):
        if block.start is None:
            block.start = self.frames
            self.frames += block.duration
        else:
            action_end = block.start + block.duration
            if action_end > self.frames:
                self.frames = action_end

        self.blocks.append(block)
        return block

    def update(self, frames_passed):
        patches = None
        for block_index, block in enumerate(self.blocks[self.dead_blocks_count:]):
            if block.is_alive(frames_passed):
                if patches is None:
                    patches = []
                result = block._draw(frames_passed)
                if result:
                    if type(result) is tuple:
                        patches.extend(result)
                    else:
                        patches.append(result)
        return patches

    def build_animation(self, fig, blit=False):
        from matplotlib import animation
        ani = animation.FuncAnimation(
            fig=fig,
            func=self.update,
            frames=self.frames,
            interval=self.interval,
            blit=blit)
        return ani
