import pygments
from pygments.lexers import get_lexer_by_name
from pygments.styles import get_style_by_name
from pygments.formatters import ImageFormatter
from PIL import Image, ImageDraw
from io import BytesIO
from util import rounded_rectangle, gradient_background


class Highlight:

    font_size = 16
    font_name = 'Liberation Mono'
    line_pad = 5
    line_numbers = False
    style = 'default'

    background_color = ''
    highlight_color = ''

    formatter = None
    lexer = None
    code_style = None

    # Color for window frame.
    window_frame_color = '#e2e1e3'
    bg_from_color = (48, 113, 227)
    bg_to_color = (27, 62, 122)
    close_circle = '#fa4b4b'
    maximize_circle = '#fab339'
    minimize_circle = '#2fc242'

    def __init__(self, lexer, style='default', **kwargs):
        self.lexer = get_lexer_by_name(lexer)
        self.code_style = get_style_by_name(style)

        if 'window_frame_color' in kwargs.keys():
            if bool(kwargs['window_frame_color']):
                self.window_frame_color = kwargs['window_frame_color']

        if 'bg_from_color' in kwargs.keys():
            if bool(kwargs['bg_from_color']):
                self.bg_from_color = kwargs['bg_from_color']

        if 'bg_to_color' in kwargs.keys():
            if bool(kwargs['bg_to_color']):
                self.bg_to_color = kwargs['bg_to_color']

        if 'close_circle' in kwargs.keys():
            if bool(kwargs['close_circle']):
                self.close_circle = kwargs['close_circle']

        if 'maximize_circle' in kwargs.keys():
            if bool(kwargs['maximize_circle']):
                self.maximize_circle = kwargs['maximize_circle']

        if 'minimize_circle' in kwargs.keys():
            if bool(kwargs['minimize_circle']):
                self.minimize_circle = kwargs['minimize_circle']

        if 'font_size' in kwargs.keys():
            if bool(kwargs['font_size']):
                self.font_size = kwargs['font_size']

        if 'font_name' in kwargs.keys():
            if bool(kwargs['font_name']):
                self.font_name = kwargs['font_name']

        if 'line_pad' in kwargs.keys():
            if bool(kwargs['line_pad']):
                self.line_pad = kwargs['line_pad']

        if 'line_numbers' in kwargs.keys():
            self.line_numbers = kwargs['line_numbers']

        if 'background_color' in kwargs.keys():
            if bool(kwargs['background_color'].strip()):
                self.code_style.background_color = kwargs['background_color']

        if 'highlight_color' in kwargs.keys():
            if bool(kwargs['highlight_color'].strip()):
                self.code_style.highlight_color = kwargs['highlight_color']

        self.formatter = ImageFormatter(
            font_size=self.font_size,
            font_name=self.font_name,
            line_pad=self.line_pad,
            line_numbers=self.line_numbers,
            style=self.code_style,
        )

    @staticmethod
    def get_value(key, kwargs, default):
        if key in kwargs.keys():
            return kwargs[key]
        else:
            return default

    def prepare_code(self, code: list, **kwargs) -> str:
        """
        Preparing the source code by concatenating lines of code.
        :param code: Source code separated by \n
        :param fake_line_numbers: Add line number as text on the left side. TODO: Change bg color directly in pygments
        :param show_title_in_code: Is it allowed to add a question as the first comment
        :param title: Put this comment in the first line.
        :param comment_char: The character with which to start the comment.
        :return: Full source code as string.
        """

        fake_line_numbers = self.get_value('fake_line_numbers', kwargs, False)
        show_title_in_code = self.get_value('show_title_in_code', kwargs, False)
        title = self.get_value('title', kwargs, False)
        comment_char = self.get_value('comment_char', kwargs, '#')

        if title and show_title_in_code:
            code.insert(0, f'{comment_char} {title}\n')

        content = ''
        total_numbers = len(str(len(code)))

        for n, line in enumerate(code, start=1):
            spaces = ' ' * (total_numbers - len(str(n)))
            if len(code) >= 4:
                if fake_line_numbers:
                    content += f'{spaces}{n}| {line}'
                else:
                    content += line
            else:
                content += line

        return content

    def to_image(self, source_code):
        return Image.open(BytesIO(pygments.highlight(source_code, self.lexer, self.formatter)))

    def to_macos_frame(self, source_code):
        img = Image.open(BytesIO(pygments.highlight(source_code, self.lexer, self.formatter)))

        size = (img.size[0] + 10, img.size[1] + 65)
        code_frame = Image.new("RGBA", size)

        margin_for_window = 100
        background = gradient_background(
            (size[0] + margin_for_window, size[1] + margin_for_window), from_color=self.bg_from_color,
            to_color=self.bg_to_color
        )

        draw = ImageDraw.Draw(code_frame)
        rounded_rectangle(
            draw, ((0, 0), size), 20, fill=self.window_frame_color
        )

        corner_left = 15
        corner_bottom = 35
        for color in [self.close_circle, self.maximize_circle, self.minimize_circle]:
            draw.ellipse((corner_left, 15, corner_bottom, 35), fill=color, outline=color)
            corner_left += 30
            corner_bottom += 30

        code_frame.paste(
            img, (5, 50)
        )

        background.paste(code_frame, (int(margin_for_window / 2), int(margin_for_window / 2)), mask=code_frame)
        return background

    @staticmethod
    def to_bytes(image):
        with BytesIO() as output:
            image.save(output, format='PNG')
            data = output.getvalue()

        return data
