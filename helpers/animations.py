from manim import *
from typing import Optional


# ShowCreationThenFadeOut
class CreateThenFadeOut(Succession):
    def __init__(self, mobject: VMobject, remover: bool = True, **kwargs) -> None:
        super().__init__(Create(mobject), FadeOut(mobject), remover=remover, **kwargs)


def mark_line(line: Line, c: Optional[str] = YELLOW, width: Optional[int] = None, reverse: bool = False, **kwargs):
    if c is None:
        c = line.get_color()
    if width is None:
        width = line.get_stroke_width() * 2

    if reverse:
        line = Line(line.get_end(), line.get_start()).set_z_index(line.z_index)
    else:
        line = line.copy()

    return CreateThenFadeOut(line.set_stroke(c, width), **kwargs)


def get_fade_out_moving(follow: Mobject) -> Callable:
    return lambda z, alpha: z.fade(alpha).move_to(follow)


def get_indicate_moving(updater: Callable, c: str,
                        start_width: float = DEFAULT_STROKE_WIDTH,
                        goal_width: float = DEFAULT_STROKE_WIDTH * 2) -> Callable:
    return lambda z, alpha: updater(z)\
        .fade_to(c, smooth(alpha))\
        .set_stroke(width=(goal_width - start_width) * smooth(alpha) + start_width)
