import string
from .app import renderer
from .core import Color
from .shape import square
from .shape import rect_mode
from .color import no_stroke
from .color import fill
from .structure import open_context
from .constants import CENTER
from .constants import RIGHT
from .constants import BOTTOM
from .constants import MIDDLE
from .constants import CORNER


class CText(object):

    def __init__(self, x, y, chars):
        self.x = x
        self.y = y
        self.chars = chars
        self.fill_color = Color('', 0, 0)


def text(text, x, y):
    matrix = _get_char_matrix(text)
    height = len(matrix)
    width = len(matrix[0]) if height > 0 else 0

    if renderer.text_align_x == RIGHT:
        x -= width
    elif renderer.text_align_x == CENTER:
        x -= width / 2

    if renderer.text_align_y == BOTTOM:
        y -= height
    elif renderer.text_align_y == MIDDLE:
        y -= height / 2

    with open_context():
        rect_mode(CORNER)
        _, fg, bg = renderer.fill_color
        no_stroke()
        for i, chars in enumerate(matrix):
            for j, ch in enumerate(chars):
                fill(ch, fg, bg)
                x0 = x + j * renderer.text_size
                y0 = y + i * (renderer.text_size + renderer.text_leading - 1)
                square(x0, y0, renderer.text_size - 1)


def text_width(text):
    matrix = _get_char_matrix(text)
    if len(matrix) > 0:
        return len(matrix[0]) * renderer.text_size
    return 0


def text_height(text):
    matrix = _get_char_matrix(text)
    return len(matrix) * renderer.text_size


def text_align(align_x=None, align_y=None):
    if align_x != None:
        renderer.text_align_x = align_x

    if align_y != None:
        renderer.text_align_y = align_y


def text_leading(leading):
    renderer.text_leading = leading


def text_size(size):
    renderer.text_size = size


def _get_char_matrix(text):
    lines = [line for line in text.split(
        '\n') if not line in string.whitespace]
    max_width = max([len(line) for line in lines])
    matrix = [[line[i] if i < len(line) else ' ' for i in range(
        max_width)] for line in lines]
    return matrix
