from PIL import Image, ImageDraw


def rounded_rectangle(draw: ImageDraw, xy, r, fill=None, outline=None):
    draw.rectangle(
        [(xy[0][0], xy[0][1] + r), (xy[1][0], xy[1][1] - r)],
        fill=fill, outline=outline
    )
    draw.rectangle(
        [(xy[0][0] + r, xy[0][1]), (xy[1][0] - r, xy[1][1])],
        fill=fill, outline=outline
    )
    draw.pieslice(
        [xy[0], (xy[0][0] + r * 2, xy[0][1] + r * 2)],
        180, 270, fill=fill, outline=outline
    )
    draw.pieslice(
        [(xy[1][0] - r * 2, xy[1][1] - r * 2), xy[1]],
        0, 90, fill=fill, outline=outline
    )
    draw.pieslice(
        [(xy[0][0], xy[1][1] - r * 2), (xy[0][0] + r * 2, xy[1][1])],
        90, 180, fill=fill, outline=outline
    )
    draw.pieslice(
        [(xy[1][0] - r * 2, xy[0][1]), (xy[1][0], xy[0][1] + r * 2)],
        270, 360, fill=fill, outline=outline
    )


def interpolate(f_co, t_co, interval):
    det_co =[(t - f) / interval for f , t in zip(f_co, t_co)]
    for i in range(interval):
        yield [round(f + det * i) for f, det in zip(f_co, det_co)]


def gradient_background(size, from_color, to_color):
    gradient = Image.new('RGBA', size, color=0)
    draw = ImageDraw.Draw(gradient)

    for i, color in enumerate(interpolate(from_color, to_color, gradient.width * 2)):
        draw.line([(i, 0), (0, i)], tuple(color), width=1)

    return gradient
