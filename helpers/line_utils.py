from manim import *


def get_line_updater(prev: Dot, nxt: Dot, **kwargs) -> Callable[[Mobject], None]:
    return lambda z: z.become(
        Line(
            prev.get_center(), nxt.get_center(),
            color=kwargs.get('color', z.color),
            stroke_width=kwargs.get('stroke_width', z.stroke_width),
        )
    ).set_z_index(0)
