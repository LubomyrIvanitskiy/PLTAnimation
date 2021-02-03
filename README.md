# PLTAnimation

Library for making simple animations with matplotlib plots and creating video from them.

The main class is `animation.Block` which represents a part of animation with it's own *start_time*, *duration* e.t.c and the `animation.AnimationBuilder` that compounds that blocks together and create the animation.

There is also the `template_blocks.py` module that has already predefined some types of animation blocks, so you can extend either one of the template class or create your own custom block extending `animation.Block` class directly.

In order to create an animation block you need to extend one of the Block classes and override 3 method:

1. `provide_data`() - provide data to be plotted (like numpy arrays for each axis)
2. `draw_figure`() - having an plt axes and data you can draw the data on the axes whatever you want, and then return matplotlib artists
3. `update_figure`() - if you don't want your animation to be fully re-drawn on each new frame you can override this method and provide your custom behaviour (like update artist positions only). For some examples see: `demo.py`
