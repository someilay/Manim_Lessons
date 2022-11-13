from manim import *


def get_fade_out_moving(follow: Mobject) -> Callable:
    return lambda z, alpha: z.fade(alpha).move_to(follow)


def get_indicate_moving(updater: Callable, c: str,
                        start_width: float = DEFAULT_STROKE_WIDTH,
                        goal_width: float = DEFAULT_STROKE_WIDTH * 2) -> Callable:
    return lambda z, alpha: updater(z)\
        .fade_to(c, smooth(alpha))\
        .set_stroke(width=(goal_width - start_width) * smooth(alpha) + start_width)
