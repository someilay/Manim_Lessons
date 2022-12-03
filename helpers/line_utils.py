from manim import *


def get_line_updater(prev: Dot, nxt: Dot, z_index: int = 0, **kwargs) -> Callable[[Mobject], None]:
    return lambda z: z.become(
        Line(
            prev.get_center(), nxt.get_center(),
            color=kwargs.get('color', z.color),
            stroke_width=kwargs.get('stroke_width', z.stroke_width),
            fill_opacity=kwargs.get('fill_opacity', z.fill_opacity),
            stroke_opacity=kwargs.get('stroke_opacity', z.stroke_opacity),
            background_stroke_opacity=kwargs.get('background_stroke_opacity', z.background_stroke_opacity)
        )
    ).set_z_index(z_index)


def norm_line_updater(first: Dot, second: Dot, third: Dot, z_index: int = 0, **kwargs):
    def updater(line: Line) -> Line:
        intersection = find_intersection(
            [first.get_center()],
            [rotate_vector(third.get_center() - second.get_center(), PI/2)],
            [second.get_center()],
            [third.get_center() - second.get_center()]
        )[0]
        return line.become(
            Line(
                first.get_center(), intersection,
                color=kwargs.get('color', line.color),
                stroke_width=kwargs.get('stroke_width', line.stroke_width),
                fill_opacity=kwargs.get('fill_opacity', line.fill_opacity),
                stroke_opacity=kwargs.get('stroke_opacity', line.stroke_opacity),
                background_stroke_opacity=kwargs.get('background_stroke_opacity', line.background_stroke_opacity)
            )
        ).set_z_index(z_index)
    return updater


def get_angle_updater(first: Dot, second: Dot, third: Dot, z_index: int = 0, **kwargs) -> Callable[[Mobject], None]:
    return lambda z: z.become(
        Angle.from_three_points(
            first.get_center(), second.get_center(), third.get_center(),
            color=kwargs.get('color', z.color),
            elbow=kwargs.get('elbow', z.elbow),
            radius=kwargs.get('radius', z.radius if hasattr(z, 'radius') else None)
        )
    ).set_z_index(z_index)
