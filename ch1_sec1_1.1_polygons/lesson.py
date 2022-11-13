import numpy as np

from helpers import RUS_TEMPLATE, Common
from helpers.text_utils import create_tex_group, write_tex_group, straight_forward_proof, fade_out_objects
from helpers.dot_utils import get_random_walk, get_dot_title_updater, get_random_move, get_dot_updater, \
    get_optimal_title_loc
from helpers.line_utils import get_line_updater
from helpers.animations import get_fade_out_moving, get_indicate_moving
from typing import Optional
from manim import *


FONT_SIZE = DEFAULT_FONT_SIZE / 1.5
SEGMENT_DEF_TEXTS = [
    [
        r'\raggedright \textbf{Отрезок} \textendash\ часть прямой, заключенная между двумя точками. '
        r'\textsl{В большинстве случаев нас будут интересовать только} ', r'\textsl{\textbf{невырожденные}}',
        r'\textsl{ отрезки, т.е. такие, у которых начало и конец не совпадают.}'
    ],
    r'\raggedright \emph{Пример:}'
]


# Segment
class Scene1(Common):
    @staticmethod
    def meta_construct(self: Scene):
        segment_def = create_tex_group(
            SEGMENT_DEF_TEXTS, LEFT, font_size=FONT_SIZE, tex_template=RUS_TEMPLATE
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(UL)
        write_tex_group(segment_def, self, buf_time=DEFAULT_WAIT_TIME / 2)

        non_singular_mark = SurroundingRectangle(
            segment_def[0][1]
        )

        a_dot = Dot(ORIGIN)
        b_dot = Dot(ORIGIN)
        a_title = Tex('A', font_size=FONT_SIZE, tex_template=RUS_TEMPLATE)
        b_title = Tex('B', font_size=FONT_SIZE, tex_template=RUS_TEMPLATE)

        line = Line(color=GREEN, start=a_dot.get_center(), end=b_dot.get_center())

        always(a_title.next_to, a_dot, direction=DOWN * 0.8)
        always(b_title.next_to, b_dot, direction=DOWN * 0.8)
        line.add_updater(get_line_updater(a_dot, b_dot))

        brace = Brace(line, direction=line.copy().rotate(PI / 2).get_unit_vector())
        brace.add_updater(lambda z: z.become(Brace(line, direction=line.copy().rotate(PI / 2).get_unit_vector())))

        brace_text = Tex('Отрезок', font_size=FONT_SIZE, tex_template=RUS_TEMPLATE).center()
        brace_text.add_updater(
            lambda z: z.become(
                Tex('Отрезок', font_size=FONT_SIZE, tex_template=RUS_TEMPLATE).center().move_to(
                    brace.get_center() + line.copy().rotate(PI / 2).get_unit_vector() / 3
                ).rotate(
                    np.arctan2(line.get_unit_vector()[1], line.get_unit_vector()[0])
                )
            )
        )

        self.play(Create(line), Create(a_dot))
        self.add(b_dot)

        self.play(
            LaggedStart(
                AnimationGroup(a_dot.animate.move_to(2 * LEFT), b_dot.animate.move_to(2 * RIGHT)),
                AnimationGroup(Write(a_title), Write(b_title)),
                FadeIn(brace), Write(brace_text),
                lag_ratio=0.2
            ),
            run_time=DEFAULT_WAIT_TIME * 2.5
        )

        self.play(Create(non_singular_mark))

        a_random_walk = get_random_walk(a_dot, 7, (-4, -2, -0.6, 1.8))
        b_random_walk = get_random_walk(b_dot, 7, (0.6, -2, 4, 1.8))
        for a_r_step, b_r_step in zip(a_random_walk, b_random_walk):
            self.play(
                AnimationGroup(a_dot.animate.move_to(a_r_step), b_dot.animate.move_to(b_r_step)),
                run_time=DEFAULT_WAIT_TIME * 1.25
            )


POLYLINE_DEF_TEXTS = [
    [
        r'\raggedright \textbf{Ломаная} \textendash\ это последовательность отрезков $A_1A_2$, $A_2A_3$,... '
        r'\textendash\ начало каждого следующего совпадает с концом предыдущего. При этом точки ',
        r'$A_1,A_2,A_3,\ldots$', r' называются \textbf{вершинами} ломаной, '
        r'а отрезки ', r'$A_1A_2$, $A_2A_3$,...', r' \textendash\ \textbf{звеньями} ломаной.'
    ],
    r'\raggedright \emph{Пример:}'
]


# Polyline
class Scene2(Common):
    # noinspection PyTypeChecker
    @staticmethod
    def meta_construct(self: Scene):
        polyline_def = create_tex_group(
            POLYLINE_DEF_TEXTS, LEFT, font_size=FONT_SIZE, tex_template=RUS_TEMPLATE
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(UL)
        write_tex_group(polyline_def, self, buf_time=DEFAULT_WAIT_TIME / 2)

        num = 4
        dots = [Dot(ORIGIN).set_z_index(1) for _ in range(num)]
        dots_titles = [Tex(f'$A_{idx + 1}$', font_size=FONT_SIZE, tex_template=RUS_TEMPLATE) for idx in range(num)]
        lines = [
            Line(prev.get_center(), nxt.get_center(), color=GREEN) for prev, nxt in zip(dots, dots[1:])
        ]
        brace = Brace(VGroup(*dots), buff=1)
        brace_text = Tex('Ломаная', font_size=FONT_SIZE, tex_template=RUS_TEMPLATE)

        for title, dot in zip(dots_titles, dots):
            always(title.next_to, dot, direction=DOWN * 0.8)
        for line, prev, nxt in zip(lines, dots, dots[1:]):
            line.add_updater(get_line_updater(prev, nxt))
        brace.add_updater(lambda z: z.become(Brace(VGroup(*dots), buff=1)))
        always(brace_text.next_to, brace, DOWN)

        self.play(*(list(map(Create, lines)) + list(map(Create, dots))))

        buff = RIGHT * 1.75
        leftest = (num // 2) * (-buff) + int(num % 2 == 0) * buff / 2
        self.play(
            LaggedStart(
                AnimationGroup(*[dot.animate.move_to(leftest + idx * buff) for idx, dot in enumerate(dots)]),
                AnimationGroup(*list(map(Write, dots_titles))),
                FadeIn(brace), Write(brace_text),
                lag_ratio=0.2
            ),
            run_time=DEFAULT_WAIT_TIME * 2.5
        )

        link_def = Underline(polyline_def[0][3], color=RED, buff=SMALL_BUFF / 2)
        indicate_lines = [
            line.copy().set_stroke(width=line.stroke_width * 2).set_color(RED)
            for line, prev, nxt in zip(lines, dots, dots[1:] + dots[:1])
        ]
        self.play(
            LaggedStart(*[Create(line) for line in indicate_lines], lag_ratio=DEFAULT_WAIT_TIME * 3 / num),
            run_time=DEFAULT_WAIT_TIME * 2,
        )
        self.play(
            *[Transform(line, link_def) for line in indicate_lines],
            run_time=DEFAULT_WAIT_TIME * 2,
        )
        self.remove(*indicate_lines)
        self.play(
            Uncreate(link_def)
        )

        vertices_def = SurroundingRectangle(polyline_def[0][1])
        vertices_boxes = [SurroundingRectangle(title) for title in dots_titles]
        for vertex_box, title in zip(vertices_boxes, dots_titles):
            always(vertex_box.move_to, title)

        small_buff = 0.5
        steps = 3
        random_walks = np.array(
            [
                get_random_walk(
                    dot, steps, (dot.get_center()[0] - small_buff, -1.5, dot.get_center()[0] + small_buff, 1.5),
                    min_r=small_buff
                )
                for dot in dots
            ]
        )
        random_walks = random_walks.transpose((1, 0, 2))

        additional_as: list[Optional[AnimationGroup]] = [None] * len(random_walks)
        additional_as[0] = AnimationGroup(Create(vertices_def))
        vertices_def_cps = [vertices_def.copy() for _ in vertices_boxes]
        additional_as[1] = AnimationGroup(*list(map(Transform, vertices_def_cps, vertices_boxes)))
        additional_as[steps] = AnimationGroup(*list(map(Uncreate, vertices_boxes + [vertices_def])))

        for random_walk, additional_anim in zip(random_walks, additional_as):
            self.play(
                *(
                    [
                        AnimationGroup(
                            *[dot.animate.move_to(walk) for dot, walk in zip(dots, random_walk)],
                            run_time=DEFAULT_WAIT_TIME * 2
                        )
                    ] +
                    ([additional_anim] if additional_anim else [])
                ),
            )
            if additional_anim is additional_as[1]:
                self.remove(*vertices_def_cps)
                self.add(*vertices_boxes)


POLYGON_DEF_TEXTS = [
    [
        r'\raggedright \textbf{Многоугольник} \textendash\ это конечная замкнутая ломаная без самопересечений, '
        r'т.е. такая, которая состоит из конечного числа отрезков (их не менее трёх), и каждая вершина которой ',
        r'принадлежит ровно двум отрезкам', r' (и, как следствие, является их концами).'
    ],
    r' emph{Пример:}'
]


# Polyline
class Scene3(Common):
    # noinspection PyTypeChecker
    @staticmethod
    def meta_construct(self: Scene):
        polygon_def = create_tex_group(
            POLYGON_DEF_TEXTS, LEFT, font_size=FONT_SIZE, tex_template=RUS_TEMPLATE
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(UL)
        write_tex_group(polygon_def, self, buf_time=DEFAULT_WAIT_TIME / 2)

        num = 5
        origin = DOWN
        dots = [Dot(origin).set_z_index(1) for _ in range(num)]
        dots_titles = [Tex(f'$A_{idx + 1}$', font_size=FONT_SIZE, tex_template=RUS_TEMPLATE) for idx in range(num)]
        lines = [
            Line(prev.get_center(), nxt.get_center(), color=GREEN) for prev, nxt in zip(dots, dots[1:] + dots[:1])
        ]
        brace = Brace(VGroup(*dots), buff=1, direction=RIGHT)
        brace_text = Tex('Многоугольник', font_size=FONT_SIZE, tex_template=RUS_TEMPLATE)

        for title, dot in zip(dots_titles, dots):
            title.add_updater(get_dot_title_updater(dot, origin))
        for line, prev, nxt in zip(lines, dots, dots[1:] + dots[:1]):
            line.add_updater(get_line_updater(prev, nxt))
        brace.add_updater(lambda z: z.become(Brace(VGroup(*dots), buff=1, direction=RIGHT)))
        always(brace_text.next_to, brace, RIGHT)

        r = 2
        vertices_p = regular_vertices(num, radius=r)[0]
        rot = np.identity(3)
        rot[0][0] = -1

        self.play(*(list(map(Create, lines)) + list(map(Create, dots))))
        self.play(
            LaggedStart(
                AnimationGroup(
                    *[dot.animate.move_to(rot.dot(pos) + origin) for pos, dot in zip(vertices_p, dots)]
                ),
                AnimationGroup(*list(map(Write, dots_titles))),
                FadeIn(brace), Write(brace_text),
                lag_ratio=0.2
            ),
            run_time=DEFAULT_WAIT_TIME * 2.5
        )

        link_def = Underline(polygon_def[0][1], color=RED, buff=SMALL_BUFF / 2)
        indicate_lines = [
            line.copy().set_stroke(width=line.stroke_width * 2).set_color(RED)
            for line, prev, nxt in zip(lines, dots, dots[1:] + dots[:1])
        ]
        self.play(
            LaggedStart(*[Create(line) for line in indicate_lines], lag_ratio=DEFAULT_WAIT_TIME * 3 / num),
            run_time=DEFAULT_WAIT_TIME * 2,
        )
        self.play(
            *[Transform(line, link_def) for line in indicate_lines],
            run_time=DEFAULT_WAIT_TIME * 2,
        )
        self.remove(*indicate_lines)
        self.play(
            Uncreate(link_def)
        )

        small_buff = 0.7
        steps = 3
        random_walks = np.array(
            [
                get_random_walk(
                    dot, steps, (dot.get_center()[0] - small_buff, dot.get_center()[1] - small_buff,
                                 dot.get_center()[0] + small_buff, dot.get_center()[1] + small_buff),
                    min_r=small_buff
                )
                for dot in dots
            ]
        )
        random_walks = random_walks.transpose((1, 0, 2))

        additional_as: list[Optional[AnimationGroup]] = [None] * len(random_walks)
        for random_walk, additional_anim in zip(random_walks, additional_as):
            self.play(
                *(
                    [
                        AnimationGroup(
                            *[dot.animate.move_to(walk) for dot, walk in zip(dots, random_walk)],
                            run_time=DEFAULT_WAIT_TIME * 2
                        )
                    ] + ([additional_anim] if additional_anim else [])
                ),
            )


EXAMPLE_1_TEXTS = [
    [r'\textbf{Пример.} Найдите сумму внутренних углов выпуклого ', r'$n$-угольника.'],
    r'\emph{Решение:}'
]
EXAMPLE_1_SOL_TEXTS = [
    r'\raggedright $PA_1,PA_2,\ldots,PA_n$ целиком лежат внутри многоугольника (ввиду его выпуклости)'
]


# Example 1
class Scene4(Common):
    # noinspection PyTypeChecker
    @staticmethod
    def meta_construct(self: Scene):
        example_1 = create_tex_group(
            EXAMPLE_1_TEXTS, LEFT, font_size=FONT_SIZE, tex_template=RUS_TEMPLATE
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(UL)
        self.add(example_1)
        # write_tex_group(example_1, self, buf_time=DEFAULT_WAIT_TIME / 2)

        num = 6
        r = 2
        origin = ORIGIN.copy()
        vertices_p = regular_vertices(num, radius=r)[0]
        rot = np.identity(3)
        rot[0][0] = -1

        dots = [Dot(rot.dot(pos) + origin).set_z_index(1) for pos in vertices_p]
        dots_titles = [
            Tex(f'$A_{idx + 1}$', font_size=FONT_SIZE, tex_template=RUS_TEMPLATE) for idx in range(min(num, 3))
        ] + [
            Tex('$A_{...}$', font_size=FONT_SIZE, tex_template=RUS_TEMPLATE) for _ in range(min(num, 3), num - 1)
        ] + [
            Tex('$A_n$', font_size=FONT_SIZE, tex_template=RUS_TEMPLATE)
        ]
        lines = [
            Line(prev.get_center(), nxt.get_center(), color=GREEN) for prev, nxt in zip(dots, dots[1:] + dots[:1])
        ]

        for title, dot in zip(dots_titles, dots):
            title.add_updater(get_dot_title_updater(dot, origin, fixed=True))
        for line, prev, nxt in zip(lines, dots, dots[1:] + dots[:1]):
            line.add_updater(get_line_updater(prev, nxt))

        buff = 0.4
        small_buff = 0.2
        for dot in dots:
            dot.move_to(
                get_random_move(
                    dot.get_center(), small_buff, 2,
                    (dot.get_center()[0] - buff, dot.get_center()[1] - buff,
                     dot.get_center()[0] + buff, dot.get_center()[1] + buff)
                )
            )

        task_cps = [example_1[0][1].copy() for _ in dots]
        self.play(
            *list(map(Transform, task_cps, dots))
        )
        self.remove(*task_cps)
        self.add(*dots)

        total_len = sum(map(lambda x: x.get_length(), lines))
        for line, title in zip(lines, dots_titles):
            self.play(Create(line), Write(title), run_time=4 * DEFAULT_WAIT_TIME * line.get_length() / total_len)

        p_dot = Dot().set_z_index(1).move_to(get_random_move(origin, 0, 2, (-buff, -buff, buff, buff)))
        optimal_pos = get_optimal_title_loc(p_dot, dots) / 3
        p_title = Tex(f'$P$', font_size=FONT_SIZE, tex_template=RUS_TEMPLATE).center().next_to(p_dot, optimal_pos)
        p_lines = [Line(p_dot.get_center(), dot.get_center(), color=RED) for dot in dots]

        always(p_title.next_to, p_dot, optimal_pos)
        for line, dot in zip(p_lines, dots):
            line.add_updater(get_line_updater(p_dot, dot))

        self.play(Succession(Create(p_dot), Write(p_title)))
        self.play(*list(map(Create, p_lines)))

        origin_shift = 4 * LEFT
        origin += origin_shift
        self.play(*[dot.animate.shift(origin_shift) for dot in (dots + [p_dot])])

        solution_1 = create_tex_group(
            EXAMPLE_1_SOL_TEXTS, LEFT, font_size=FONT_SIZE, tex_template=RUS_TEMPLATE
        ).arrange(DOWN, aligned_edge=LEFT).next_to(example_1[-1], DOWN).to_edge(RIGHT)

        self.play(
            Succession(*[line.animate.fade(0.5) for line in p_lines]),
            Write(solution_1[0])
        )


if __name__ == '__main__':
    with tempconfig({'quality': 'medium_quality', 'preview': True, 'media_dir': 'media'}):
        scene = Scene4()
        scene.render()
