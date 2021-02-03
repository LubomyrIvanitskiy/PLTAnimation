import base64
import os
import webbrowser
from io import BytesIO

from matplotlib.animation import FuncAnimation


def get_media_table(medias, column_count=2):
    """
    Get an HTML markup for table with media
    Media is any string data. It could be Base64 image, HTML5 Video or any String
    :param medias: list of media strings
    :param column_count: count of column
    :return: an html markup with table with media
    """

    html = """<html><table>"""
    for i in range(0, len(medias), column_count):
        row_builder = ["<tr>"]
        for j in range(column_count):
            row_builder.append("<td>")
            row_builder.append(medias[i + j] if i + j < len(medias) else '')
            row_builder.append("</td>")
        row_builder.append("</tr>")
        row = ''.join(row_builder)
        html += row
    html += """</table></html>"""
    return html


def get_html_image(fig):
    """
    Get image from plt figure convert it to Base64 and wrap within HTML tag
    :param fig: plot figure returned by plt.subplots
    :return: html image tag
    """
    image = BytesIO()
    fig.savefig(image, format='png')
    image_string = base64.b64encode(image.getvalue()).decode('utf-8')
    img_html = '<img src="data:image/png;base64,{}&#10;">'.format(image_string)
    return img_html


def get_js_html(animation: FuncAnimation):
    import matplotlib.pyplot as plt
    plt.rcParams['animation.ffmpeg_path'] = 'C:/FFmpeg/bin/ffmpeg.exe'
    return animation.to_jshtml()


def get_html_video(animation: FuncAnimation):
    import matplotlib.pyplot as plt
    plt.rcParams['animation.ffmpeg_path'] = 'C:/FFmpeg/bin/ffmpeg.exe'
    return animation.to_html5_video()


temporary_dir = 'tmp'
temporary_html_file = temporary_dir + os.path.sep + 'temporary_html.html'


def open_html(html):
    if not os.path.exists(temporary_dir):
        os.mkdir(temporary_dir)
    f = open(temporary_html_file, 'w')
    f.write(html)
    f.close()

    webbrowser.open_new_tab(temporary_html_file)
