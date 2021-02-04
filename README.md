# PLTAnimation

Library for making simple animations with matplotlib plots and creating video from them.

The main class is `animation.Block` which represents a part of animation with it's own *start_time*, *duration* e.t.c and the `animation.AnimationBuilder` that compounds that blocks together and create the animation.

There is also the `examples` module that has already predefined some types of animation blocks, borrow some ideas from there

In order to create an animation block you need to extend the Block class and override 2 methods:

1. `on_frame`() - having an plt axes and data you can draw the data on the axes whatever you want, and then return matplotlib artists
2. `finish`() - (Optional). Cleanup resources when the animation block has finished

**Notes**: 
* You can re-use already drawn plt artists, which are received as `last_patches` in the `on_frame`() method. 
* Also you can combine several blocks together by passing `predecessor_block` as the Block constructor. Int this case you'll receive the predecessor_block's last patches in the `on_frame`() method and then re-use it on your own.
* To store your animation as video and display in a browser, call: `html_utils.open_html(html_utils.get_html_video(anim))` (you'll need FFMpeg installed, and to specify your path in  html_utils methods, like:  `plt.rcParams['animation.ffmpeg_path'] = 'C:/FFmpeg/bin/ffmpeg.exe'`
* To store your animation as an interactive JS code, use: `html_utils.open_html(html_utils.get_js_html(anim))`
* To just see the animation, call: 'plt.show()' in the end
