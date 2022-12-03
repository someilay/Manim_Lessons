from helpers import RUS_TEMPLATE, rus_template, Common
from helpers.text_utils import create_tex_group, write_tex_group, update_matrix
from helpers.dot_utils import get_random_walk, get_dot_title_updater, get_random_move, get_dot_updater, \
    get_optimal_title_loc, extended_line_updater, bisector_updater, norm_dot_updater, orthocenter_updater, \
    intersection_updater
from helpers.line_utils import get_line_updater, norm_line_updater, get_angle_updater
from helpers.animations import CreateThenFadeOut, mark_line
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
    r'\emph{Пример:}'
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
    [r'\textbf{Пример 1.} Найдите сумму внутренних углов выпуклого ', r'$n$-угольника.'],
    r'\emph{Решение:}'
]
EXAMPLE_1_SOL_TEXTS = [
    r'\raggedright $PA_1,PA_2,\ldots,PA_n$ целиком лежат внутри многоугольника (ввиду его выпуклости).',
    r'\raggedright Они делят его на $n$ треугольников: $\triangle PA_1A_2, \triangle PA_2A_3, '
    r'\ldots,\triangle PA_nA_1$.',
    [r'$360^{\circ}$', r' + ', r'сумма углов $A_1A_2A_3...A_n$', r' = ', r'$n$ $\cdot$ ', r'$180^{\circ}$'],
    r'сумма углов $A_1A_2A_3...A_n$ = $($$n$ $-2)$ $\cdot$ $180^{\circ}$'
]


# Example 1
class Scene4(Common):
    # noinspection PyTypeChecker
    @staticmethod
    def meta_construct(self: Scene):
        example_1 = create_tex_group(
            EXAMPLE_1_TEXTS, LEFT, font_size=FONT_SIZE, tex_template=RUS_TEMPLATE
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(UL)
        write_tex_group(example_1, self, buf_time=DEFAULT_WAIT_TIME / 2)

        num = 6
        r = 2
        origin = ORIGIN.copy()
        vertices_p = regular_vertices(num, radius=r)[0]
        rot = np.identity(3)
        rot[0][0] = -1

        dots = [Dot(rot.dot(pos) + origin).set_z_index(2) for pos in vertices_p]
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
            line.add_updater(get_line_updater(prev, nxt, z_index=1))

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
        # Create outer lines
        self.play(
            *list(map(Transform, task_cps, dots))
        )
        self.remove(*task_cps)
        self.add(*dots)

        total_len = sum(map(lambda x: x.get_length(), lines))
        for line, title in zip(lines, dots_titles):
            self.play(Create(line), Write(title), run_time=4 * DEFAULT_WAIT_TIME * line.get_length() / total_len)

        p_dot = Dot().set_z_index(2).move_to(get_random_move(origin, 0, 2, (-buff, -buff, buff, buff)))
        optimal_pos = get_optimal_title_loc(p_dot, dots) / 3
        p_title = Tex(f'$P$', font_size=FONT_SIZE, tex_template=RUS_TEMPLATE)\
            .set_z_index(2).center().next_to(p_dot, optimal_pos)
        p_lines = [Line(p_dot.get_center(), dot.get_center(), color=RED) for dot in dots]

        always(p_title.next_to, p_dot, optimal_pos)
        for line, dot in zip(p_lines, dots):
            line.add_updater(get_line_updater(p_dot, dot, z_index=1))

        # Create inner lines
        self.play(Succession(Create(p_dot), Write(p_title)))
        self.play(*list(map(Create, p_lines)))

        origin_shift = 4 * LEFT
        origin += origin_shift
        self.play(*[dot.animate.shift(origin_shift) for dot in (dots + [p_dot])])

        solution_1 = create_tex_group(
            EXAMPLE_1_SOL_TEXTS, LEFT, font_size=FONT_SIZE, tex_template=rus_template(256)
        ).to_edge(RIGHT)

        # Match inner lines
        self.play(
            LaggedStart(
                *[line.animate.set_opacity(0.5) for line in p_lines],
                lag_ratio=DEFAULT_WAIT_TIME * 4 / num,
                run_time=DEFAULT_WAIT_TIME * 4
            ),
            Write(solution_1[0], run_time=DEFAULT_WAIT_TIME * 2)
        )
        self.play(
            *[line.animate.set_opacity(1) for line in p_lines]
        )

        # Match triangles
        polygons = [
            Polygon(
                prev.get_center(), nxt.get_center(), p_dot.get_center(),
                color=YELLOW, stroke_width=DEFAULT_STROKE_WIDTH * 2
            ).set_z_index(2)
            for prev, nxt in zip(dots, dots[1:] + dots[:1])
        ]
        self.play(
            LaggedStart(
                *[
                    Succession(Create(polygon), FadeOut(polygon))
                    for polygon in polygons
                ],
                lag_ratio=DEFAULT_WAIT_TIME * 6 / num,
                run_time=DEFAULT_WAIT_TIME * 6
            ),
            Transform(solution_1[0], solution_1[1], run_time=DEFAULT_WAIT_TIME * 2)
        )
        self.remove(solution_1[0])
        self.add(solution_1[1])

        # Draw angles
        p_angles = [
            Angle(prev.copy(), nxt.copy(), color=YELLOW, radius=0.25).set_z_index(0)
            for prev, nxt in zip(p_lines, p_lines[1:] + p_lines[:1])
        ]
        self.play(
            AnimationGroup(
                *[Create(angle) for angle in p_angles],
            )
        )
        a_angles = [
            Angle.from_three_points(
                prev.get_start(), prev.get_end(), nxt.get_end(), color=BLUE, radius=0.25
            ).set_z_index(0)
            for prev, nxt in zip(p_lines, lines)
        ]
        self.play(
            AnimationGroup(
                *[Create(angle) for angle in a_angles],
            )
        )
        b_angles = [
            Angle.from_three_points(
                nxt.get_start(), nxt.get_end(), prev.get_start(), color=MAROON, radius=0.25
            ).set_z_index(0)
            for prev, nxt in zip(p_lines[1:] + p_lines[:1], lines)
        ]
        self.play(
            AnimationGroup(
                *[Create(angle) for angle in b_angles],
            ),
            FadeOut(solution_1[1])
        )

        buff_group = VGroup(*(a_angles + b_angles))
        self.play(
            LaggedStart(
                Transform(VGroup(*p_angles), solution_1[2][0], run_time=DEFAULT_WAIT_TIME * 2),
                Write(solution_1[2][1]),
                Transform(buff_group, solution_1[2][2], run_time=DEFAULT_WAIT_TIME * 2),
                Write(solution_1[2][3]),
                lag_ratio=DEFAULT_WAIT_TIME / 2
            )
        )
        self.remove(*p_angles)
        self.remove(buff_group)
        self.add(solution_1[2][0])
        self.add(solution_1[2][2])

        # Count angles
        sub_count = Tex(r'$1$ $\cdot$', font_size=FONT_SIZE, tex_template=RUS_TEMPLATE).next_to(solution_1[2][5], LEFT)
        for idx, polygon in enumerate(polygons):
            if 0 < idx < len(polygons) - 1:
                new_sub_count = Tex(rf'${idx + 1}$ $\cdot$', font_size=FONT_SIZE, tex_template=RUS_TEMPLATE)
                new_sub_count.next_to(solution_1[2][5], LEFT)
                self.play(
                    Transform(polygon, solution_1[2][5]),
                    Transform(sub_count, new_sub_count),
                    run_time=DEFAULT_WAIT_TIME * 1.5
                )
            elif idx == 0:
                self.play(
                    Transform(polygon, solution_1[2][5]),
                    Write(sub_count),
                    run_time=DEFAULT_WAIT_TIME * 1.5
                )
            else:
                self.play(
                    Transform(polygon, solution_1[2][5]),
                    Transform(sub_count, solution_1[2][4]),
                    run_time=DEFAULT_WAIT_TIME * 1.5
                )

        for polygon in polygons:
            self.remove(polygon)
        self.remove(sub_count)
        self.add(solution_1[2])

        self.play(
            TransformMatchingTex(
                solution_1[2], solution_1[3],
                path_arc=PI / 2,
                transform_mismatches=True,
            ),
            run_time=DEFAULT_WAIT_TIME * 1.5
        )
        self.remove(solution_1[2])
        self.add(solution_1[3])

        self.play(
            Create(SurroundingRectangle(solution_1[3])),
            AnimationGroup(*map(FadeOut, p_lines)),
            FadeOut(p_dot), FadeOut(p_title),
            run_time=DEFAULT_WAIT_TIME * 1.5
        )


EXAMPLE_2_TEXTS = [
    [r'\raggedright \textbf{Пример 1.} Доказать, что биссектриса внешнего угла при вершине ',
     r'равнобедренного треугольника', r' параллельна его основанию.'],
    r'\emph{Решение:}'
]


# Example 2
class Scene5(Common):
    @staticmethod
    def meta_construct(self: Scene):
        example_2 = create_tex_group(
            EXAMPLE_2_TEXTS, LEFT, font_size=FONT_SIZE, tex_template=RUS_TEMPLATE
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(UL)
        # self.add(example_2)
        write_tex_group(example_2, self, buf_time=DEFAULT_WAIT_TIME / 2)

        num = 3
        origin = DOWN.copy() * 2.2
        dots = [
            Dot(origin).set_z_index(2)
            for _ in range(num)
        ]
        dots_titles = [
            Tex(f'${chr(ord("A") + idx)}$', font_size=FONT_SIZE, tex_template=RUS_TEMPLATE).set_z_index(2)
            for idx in range(num)
        ]
        lines = [
            Line(prev.get_center(), nxt.get_center(), color=GREEN) for prev, nxt in zip(dots, dots[1:] + dots[:1])
        ]
        # noinspection PyTypeChecker
        lines[-1].set_color(BLUE)

        for line, prev, nxt in zip(lines, dots, dots[1:] + dots[:1]):
            line.add_updater(get_line_updater(prev, nxt, z_index=1))

        iso_word = example_2[0][1].copy()
        self.play(
            Transform(iso_word, dots[0])
        )
        self.remove(iso_word)
        self.add(*dots)
        self.wait(DEFAULT_WAIT_TIME / 2)

        # Animate construction
        self.play(
            AnimationGroup(
                *[
                    dot.animate.shift(rotate_vector(UP * 1.5, 2 * PI * (1 - idx) / 3))
                    for idx, dot in enumerate(dots)
                ]
            )
        )

        for title, dot in zip(dots_titles, dots):
            title.add_updater(get_dot_title_updater(dot, origin, fixed=True))

        self.play(
            Succession(
                *[
                    AnimationGroup(Create(line), Write(dot_title))
                    for line, dot_title in zip(lines, dots_titles)
                ]
            )
        )

        unit_scale_1 = 2.5
        unit_scale_2 = 1.5

        invis_dot_1 = Dot(fill_opacity=0)
        extended_line_updater(dots[-1], dots[-2], unit_scale_1)(invis_dot_1)
        invis_dot_1.add_updater(extended_line_updater(dots[-1], dots[-2], unit_scale_1))
        extended_line = Line(dots[-2].get_center(), invis_dot_1.get_center(), color=GREEN)
        extended_line.add_updater(get_line_updater(dots[-2], invis_dot_1, z_index=1))

        invis_dot_2 = Dot(unit_scale_1 * LEFT + dots[1].get_center(), fill_opacity=0)
        invis_dot_2.add_updater(get_dot_updater(dots[1], unit_scale_1 * LEFT))
        bisector = Line(dots[1].get_center(), invis_dot_2.get_center(), color=RED)
        bisector.add_updater(get_line_updater(dots[1], invis_dot_2, z_index=1))

        self.add(invis_dot_1, invis_dot_2)

        dots_titles[1].updaters = []
        self.play(
            Create(extended_line),
            Create(bisector),
            dots_titles[1].animate.move_to(dots[1].get_center() + UR / 4)
        )
        always(dots_titles[1].next_to, dots[1], UR / 4)

        d_dot = Dot().set_z_index(2)
        d_dot_title = Tex('$D$', font_size=FONT_SIZE, tex_template=RUS_TEMPLATE).set_z_index(2)
        extended_line_updater(dots[-1], dots[-2], unit_scale_2)(d_dot)
        d_dot.add_updater(extended_line_updater(dots[-1], dots[-2], unit_scale_2))
        always(d_dot_title.next_to, d_dot, UR / 4)

        e_dot = Dot(unit_scale_2 * LEFT + dots[1].get_center()).set_z_index(2)
        e_dot_title = Tex('$E$', font_size=FONT_SIZE, tex_template=RUS_TEMPLATE).set_z_index(2)
        e_dot.add_updater(get_dot_updater(dots[1], unit_scale_2 * LEFT))
        always(e_dot_title.next_to, e_dot, UP / 4)

        self.play(Create(d_dot), Create(e_dot), Write(d_dot_title), Write(e_dot_title))

        # Play with sizes
        self.play(dots[1].animate.shift(UP), run_time=DEFAULT_WAIT_TIME * 1.5)
        self.play(dots[1].animate.shift(DOWN), run_time=DEFAULT_WAIT_TIME * 1.5)

        self.play(
            dots[0].animate.shift(LEFT),
            dots[2].animate.shift(RIGHT),
            run_time=DEFAULT_WAIT_TIME * 1.5
        )
        self.play(
            dots[0].animate.shift(RIGHT),
            dots[2].animate.shift(LEFT),
            run_time=DEFAULT_WAIT_TIME * 1.5
        )

        self.play(
            dots[0].animate.shift(RIGHT / 3),
            dots[1].animate.shift(UP * 0.8),
            dots[2].animate.shift(LEFT / 3),
            run_time=DEFAULT_WAIT_TIME * 2
        )

        # Show proof
        ab_line = Line(lines[0].get_end(), lines[0].get_start()).set_z_index(1)\
            .set_stroke(YELLOW, DEFAULT_STROKE_WIDTH * 2)
        bc_line = lines[1].copy().set_stroke(YELLOW, DEFAULT_STROKE_WIDTH * 2)
        self.play(
            Succession(Create(ab_line), FadeOut(ab_line)),
            Succession(Create(bc_line), FadeOut(bc_line)),
        )

        a_angles = [
            Angle.from_three_points(lines[-1].get_start(), lines[0].get_start(), lines[0].get_end(), color=PURPLE),
            Angle.from_three_points(lines[1].get_start(), lines[1].get_end(), lines[-1].get_end(), color=PURPLE),
        ]
        a_angles_titles = [
            Tex(r'$\alpha$', font_size=FONT_SIZE, tex_template=RUS_TEMPLATE)
            .set_z_index(2).next_to(a_angles[0], UR / 100),
            Tex(r'$\alpha$', font_size=FONT_SIZE, tex_template=RUS_TEMPLATE)
            .set_z_index(2).next_to(a_angles[1], UL / 100),
        ]
        self.play(
            *map(Create, a_angles)
        )
        self.play(
            *map(Write, a_angles_titles)
        )

        b_angle = Angle.from_three_points(lines[0].get_start(), lines[0].get_end(), lines[1].get_end(), color=RED)
        b_angle_title = Tex(r'$180^{\circ} - 2$$\alpha$', font_size=FONT_SIZE, tex_template=RUS_TEMPLATE)\
            .set_z_index(2).next_to(b_angle, RIGHT)
        a_angles_titles_cp = VGroup(*[obj.copy() for obj in a_angles_titles])
        self.play(Create(b_angle))
        self.play(Transform(a_angles_titles_cp, b_angle_title))
        self.remove(a_angles_titles_cp)
        self.add(b_angle_title)

        l_line = Line(dots[2].get_center(), invis_dot_1.get_center(),
                      color=YELLOW, stroke_width=DEFAULT_STROKE_WIDTH * 2).set_z_index(1)
        self.play(
            Succession(Create(l_line), FadeOut(l_line))
        )

        c_angle = Angle.from_three_points(d_dot.get_center(), lines[0].get_end(), lines[0].get_start(), color=BLUE)
        c_angle_title = Tex(r'$2$$\alpha$', font_size=FONT_SIZE, tex_template=RUS_TEMPLATE)\
            .set_z_index(2).next_to(c_angle, DL / 50)
        self.play(Uncreate(b_angle), Create(c_angle), Transform(b_angle_title, c_angle_title))
        self.remove(b_angle_title)
        self.add(c_angle_title)

        d_angles_titles = [
            Tex(r'$\alpha$', font_size=FONT_SIZE, tex_template=RUS_TEMPLATE).set_z_index(2).next_to(c_angle, DL / 50),
            Tex(r'$\alpha$', font_size=FONT_SIZE, tex_template=RUS_TEMPLATE).set_z_index(2).next_to(c_angle, UL / 50)
        ]
        eb_line = bisector.copy().set_stroke(YELLOW, DEFAULT_STROKE_WIDTH * 2)
        self.play(
            Succession(Create(eb_line), FadeOut(eb_line))
        )
        self.play(
            c_angle.animate.fade_to(YELLOW, 1),
            Transform(c_angle_title, d_angles_titles[0]),
            Transform(c_angle_title.copy(), d_angles_titles[1]),
        )

        # Final
        self.wait(DEFAULT_WAIT_TIME / 2)
        self.play(
            Create(SurroundingRectangle(d_angles_titles[1])),
            Create(SurroundingRectangle(a_angles_titles[1])),
        )


BISECTOR_TEXTS = [
    [r'\raggedright \textbf{Свойство биссектрисы.} Докажите, что биссектриса делит сторону ', r'треугольника',
     r' в том же отношении, в котором \guillemotleft состоят\guillemotright\ две образующие ее угол стороны.'],
    r'\emph{Доказательство:}',
]
BISECTOR_PROOF = [
    r'Положим $AD \parallel CB$',
    r'$\triangle BPC \sim \triangle APD$',
    [r'$\frac{BP}{PA}=\frac{BC}{AD}$', r', $AD=CA$'],
    r'$\frac{BP}{PA}=\frac{BC}{CA}$'
]


# Bisector property
class Scene6(Common):
    @staticmethod
    def meta_construct(self: Scene):
        bisector_prop = create_tex_group(
            BISECTOR_TEXTS, LEFT, font_size=FONT_SIZE, tex_template=RUS_TEMPLATE
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(UL)
        # self.add(bisector_prop)
        write_tex_group(bisector_prop, self, buf_time=DEFAULT_WAIT_TIME / 2)

        num = 3
        origin = UP.copy() * 0.1
        dots = [
            Dot(origin).set_z_index(2)
            for _ in range(num)
        ]
        dots_titles = [
            Tex(f'${chr(ord("A") + idx)}$', font_size=FONT_SIZE, tex_template=RUS_TEMPLATE).set_z_index(2)
            for idx in range(num)
        ]
        dots_titles[1], dots_titles[2] = dots_titles[2], dots_titles[1]
        lines = [
            Line(prev.get_center(), nxt.get_center(), color=GREEN) for prev, nxt in zip(dots, dots[1:] + dots[:1])
        ]

        for line, prev, nxt in zip(lines, dots, dots[1:] + dots[:1]):
            line.add_updater(get_line_updater(prev, nxt, z_index=1))

        triangle_word = bisector_prop[0][1].copy()
        self.play(
            Transform(triangle_word, dots[0])
        )
        self.remove(triangle_word)
        self.add(*dots)
        self.wait(DEFAULT_WAIT_TIME / 2)

        # Animate construction
        dot_centers = [dot.get_center() for dot in dots]
        locs = [0.7 * DOWN + 1.8 * LEFT, UP, 1.2 * DOWN + 2.5 * RIGHT]
        self.play(
            *[
                dot.animate.move_to(center + pos)
                for dot, center, pos in zip(dots, dot_centers, locs)
            ]
        )
        for title, dot in zip(dots_titles, dots):
            title.add_updater(get_dot_title_updater(dot, origin, fixed=True))
        self.play(
            Succession(
                *[
                    AnimationGroup(Create(line), Write(dot_title))
                    for line, dot_title in zip(lines, dots_titles)
                ]
            )
        )

        p_dot = Dot().set_z_index(2)
        p_title = Tex('$P$', font_size=FONT_SIZE, tex_template=RUS_TEMPLATE).set_z_index(2)

        p_dot.add_updater(bisector_updater(*dots))
        p_dot.updaters[0](p_dot)
        always(p_title.next_to, p_dot, DR / 5)

        pc_line = Line(dots[1].get_center(), p_dot.get_center(), color=RED)
        pa_line = Line(dots[0].get_center(), p_dot.get_center(), color=GREEN)
        bp_line = Line(p_dot.get_center(), dots[2].get_center(), color=GREEN)

        self.play(
            Succession(Create(pc_line), Create(p_dot), Write(p_title)),
            run_time=DEFAULT_WAIT_TIME * 2.5
        )
        self.add(pa_line, bp_line)
        pc_line.add_updater(get_line_updater(dots[1], p_dot, z_index=1))
        pa_line.add_updater(get_line_updater(dots[0], p_dot, z_index=1))
        bp_line.add_updater(get_line_updater(p_dot, dots[2], z_index=1))

        # Shift dots
        self.play(
            *[dot.animate.shift(RIGHT) for dot in dots]
        )

        # Show fractions
        config['tex_template'] = RUS_TEMPLATE

        # BC over CA
        proof_fs = 1.25
        bc_over_ca = DecimalTable(
            [[lines[1].get_length()], [lines[0].get_length()]],
            element_to_mobject_config={'num_decimal_places': 2, 'font_size': FONT_SIZE * proof_fs},
            v_buff=0.2 * proof_fs,
            h_buff=0.2 * proof_fs,
            line_config={'stroke_width': (DEFAULT_STROKE_WIDTH / 3) * proof_fs}
        )
        bc_over_ca_val = DecimalNumber(
            lines[1].get_length() / lines[0].get_length(), num_decimal_places=2, font_size=FONT_SIZE * proof_fs
        )
        bc_over_ca.add_updater(lambda z: update_matrix(z, [lines[1].get_length(), lines[0].get_length()]))
        bc_over_ca_val.add_updater(lambda z: z.set_value(lines[1].get_length() / lines[0].get_length()))

        bc_over_ca_total = VGroup(
            Tex(r'$\frac{BC}{CA}=$', font_size=FONT_SIZE * proof_fs),
            bc_over_ca,
            Tex(r'$=$', font_size=FONT_SIZE * proof_fs),
            bc_over_ca_val
        ).arrange(RIGHT, aligned_edge=ORIGIN, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER / 2).to_edge(LEFT)

        # BP over PA
        bp_over_pa = DecimalTable(
            [[bp_line.get_length()], [pa_line.get_length()]],
            element_to_mobject_config={'num_decimal_places': 2, 'font_size': FONT_SIZE * proof_fs},
            v_buff=0.2 * proof_fs,
            h_buff=0.2 * proof_fs,
            line_config={'stroke_width': (DEFAULT_STROKE_WIDTH / 3) * proof_fs}
        )
        bp_over_pa_val = DecimalNumber(
            bp_line.get_length() / pa_line.get_length(), num_decimal_places=2, font_size=FONT_SIZE * proof_fs
        )
        bp_over_pa.add_updater(lambda z: update_matrix(z, [bp_line.get_length(), pa_line.get_length()]))
        bp_over_pa_val.add_updater(lambda z: z.set_value(bp_line.get_length() / pa_line.get_length()))

        bp_over_pa_total = VGroup(
            Tex(r'$\frac{BP}{PA}=$', font_size=FONT_SIZE * proof_fs),
            bp_over_pa,
            Tex(r'$=$', font_size=FONT_SIZE * proof_fs),
            bp_over_pa_val
        ).arrange(RIGHT, aligned_edge=ORIGIN, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER / 2).to_edge(LEFT)

        all_fractions = VGroup(bc_over_ca_total, bp_over_pa_total).arrange(DOWN, aligned_edge=LEFT).to_edge(LEFT)
        self.play(Write(all_fractions[0]), run_time=DEFAULT_WAIT_TIME * 0.8)
        self.play(Write(all_fractions[1]), run_time=DEFAULT_WAIT_TIME * 0.8)

        # Play with it
        sr_rectangles = [SurroundingRectangle(obj[-1]) for obj in all_fractions]
        self.play(*map(Create, sr_rectangles))

        steps = 4
        buff = 0.7
        min_r = 0.4
        random_walks = np.array(
            [
                get_random_walk(
                    dot, steps, (dot.get_center()[0] - buff, dot.get_center()[1] - buff,
                                 dot.get_center()[0] + buff, dot.get_center()[1] + buff),
                    min_r=min_r
                )
                for dot in dots
            ]
        )
        random_walks = random_walks.transpose((1, 0, 2))
        for random_walk in random_walks:
            self.play(
                *[
                    AnimationGroup(
                        *[dot.animate.move_to(walk) for dot, walk in zip(dots, random_walk)],
                        run_time=DEFAULT_WAIT_TIME * 1.5
                    )
                ]
            )

        self.play(FadeOut(all_fractions), FadeOut(*sr_rectangles), run_time=DEFAULT_WAIT_TIME * 0.8)
        self.wait(DEFAULT_WAIT_TIME / 2)

        # Proof
        proof = create_tex_group(
            BISECTOR_PROOF, LEFT, font_size=FONT_SIZE * proof_fs, tex_template=rus_template(256)
        ).to_edge(LEFT)

        pc_line_intro = pc_line.copy().set_stroke(YELLOW, DEFAULT_STROKE_WIDTH * 2)
        abc_angles = [
            Angle.from_three_points(dots[0].get_center(), dots[1].get_center(), p_dot.get_center(), color=PURPLE),
            Angle.from_three_points(p_dot.get_center(), dots[1].get_center(), dots[2].get_center(), color=PURPLE),
        ]
        self.play(Succession(Create(pc_line_intro), FadeOut(pc_line_intro)))
        self.play(*map(Create, abc_angles))

        def custom_updater(dot: Dot):
            return dot.move_to(
                find_intersection(
                    [dots[0].get_center()],
                    [dots[2].get_center() - dots[1].get_center()],
                    [dots[1].get_center()],
                    [p_dot.get_center() - dots[1].get_center()]
                )[0]
            )
        d_dot = custom_updater(Dot().set_z_index(2))
        d_dot_title = Tex(r'$D$', font_size=FONT_SIZE)
        d_dot.add_updater(custom_updater)
        always(d_dot_title.next_to, d_dot, RIGHT / 4)

        dp_line = Line(p_dot.get_center(), d_dot.get_center(), color=RED).set_z_index(1)
        ad_line = Line(dots[0].get_center(), d_dot.get_center(), color=BLUE).set_z_index(1)
        self.play(Create(dp_line), Create(ad_line))
        self.play(Succession(Create(d_dot), Write(d_dot_title)), Write(proof[0]))
        dp_line.add_updater(get_line_updater(p_dot, d_dot, z_index=1))
        ad_line.add_updater(get_line_updater(dots[0], d_dot, z_index=1))

        adp_angle = Angle.from_three_points(p_dot.get_center(), d_dot.get_center(), dots[0].get_center(), color=PURPLE)
        ac_angles = [
            Angle.from_three_points(d_dot.get_center(), dots[0].get_center(), dots[2].get_center(), color=RED),
            Angle.from_three_points(dots[1].get_center(), dots[2].get_center(), dots[0].get_center(), color=RED),
        ]
        self.play(
            CreateThenFadeOut(ad_line.copy().set_stroke(YELLOW, DEFAULT_STROKE_WIDTH * 2)),
            CreateThenFadeOut(lines[1].copy().set_stroke(YELLOW, DEFAULT_STROKE_WIDTH * 2)),
        )
        self.play(*map(Create, ac_angles + [adp_angle]))

        # Mark angles 1
        self.play(
            adp_angle.animate.set_stroke(width=DEFAULT_STROKE_WIDTH * 4),
            abc_angles[1].animate.set_stroke(width=DEFAULT_STROKE_WIDTH * 4),
            ac_angles[0].animate.set_stroke(width=DEFAULT_STROKE_WIDTH * 4),
            ac_angles[1].animate.set_stroke(width=DEFAULT_STROKE_WIDTH * 4),
            run_time=DEFAULT_WAIT_TIME * 1.5
        )
        self.play(
            adp_angle.animate.set_stroke(width=DEFAULT_STROKE_WIDTH),
            abc_angles[1].animate.set_stroke(width=DEFAULT_STROKE_WIDTH),
            ac_angles[0].animate.set_stroke(width=DEFAULT_STROKE_WIDTH),
            ac_angles[1].animate.set_stroke(width=DEFAULT_STROKE_WIDTH),
            run_time=DEFAULT_WAIT_TIME * 1.5
        )
        self.play(
            CreateThenFadeOut(
                Polygon(
                    dots[0].get_center(), p_dot.get_center(), d_dot.get_center(),
                    color=YELLOW, stroke_width=DEFAULT_STROKE_WIDTH * 2
                ).set_z_index(2)
            ),
            CreateThenFadeOut(
                Polygon(
                    dots[2].get_center(), p_dot.get_center(), dots[1].get_center(),
                    color=YELLOW, stroke_width=DEFAULT_STROKE_WIDTH * 2
                ).set_z_index(2)
            ),
            Transform(proof[0], proof[1]),
            run_time=DEFAULT_WAIT_TIME * 2.5
        )
        self.remove(proof[0])
        self.add(proof[1])
        self.wait(DEFAULT_WAIT_TIME / 2)

        self.play(
            Transform(proof[1], proof[2][0]),
        )
        self.remove(proof[1])
        self.add(proof[2][0])
        self.wait(DEFAULT_WAIT_TIME / 2)

        # Mark angles 2
        self.play(
            adp_angle.animate.set_stroke(width=DEFAULT_STROKE_WIDTH * 4),
            abc_angles[0].animate.set_stroke(width=DEFAULT_STROKE_WIDTH * 4),
            run_time=DEFAULT_WAIT_TIME * 1.5
        )
        self.play(
            adp_angle.animate.set_stroke(width=DEFAULT_STROKE_WIDTH),
            abc_angles[0].animate.set_stroke(width=DEFAULT_STROKE_WIDTH),
            run_time=DEFAULT_WAIT_TIME * 1.5
        )
        self.play(
            CreateThenFadeOut(ad_line.copy().set_stroke(YELLOW, DEFAULT_STROKE_WIDTH * 2)),
            CreateThenFadeOut(lines[0].copy().set_stroke(YELLOW, DEFAULT_STROKE_WIDTH * 2)),
        )
        self.play(Write(proof[2][1]))
        self.wait(DEFAULT_WAIT_TIME / 2)

        proof[3].next_to(proof[2], DOWN)
        self.play(Transform(proof[2].copy(), proof[3]))
        self.play(
            Create(SurroundingRectangle(proof[3])),
            FadeOut(d_dot, d_dot_title, ad_line, dp_line, adp_angle),
            FadeOut(*ac_angles)
        )


ALTITUDE_TEXTS = [
    [r'\raggedright \textbf{Свойство высот.} Докажите, что высоты ', r'треугольника',
     r' пересекаются в одной точке (эта точка называется \textbf{ортоцентром} треугольника)'],
    r'\emph{Доказательство:}',
]
ALTITUDE_PROOF = [
    [r'$\angle BCE$', r' $=180^\circ-$ ', r'$\angle BFE$'],
    [r'$\angle AFE$', r' $=$ ', r'$\angle AHE$'],
    [r'$\angle BCE$', r' $=180^\circ-$ ', r'$(180^\circ-$ ', r'$\angle AFE$', r'$)$'],
    [r'$\angle BCE$', r' $+$ ', r'$\angle EHG$', r' $+$ ', r'$\angle BEC$', r' $+$ ',
     r'$\angle AGC$', r' $=$ ', r'$360^\circ$']
]


class Scene7(Common):
    @staticmethod
    def meta_construct(self: Scene):
        altitude_prop = create_tex_group(
            ALTITUDE_TEXTS, LEFT, font_size=FONT_SIZE, tex_template=RUS_TEMPLATE
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(UL)
        # self.add(altitude_prop)
        write_tex_group(altitude_prop, self, buf_time=DEFAULT_WAIT_TIME / 2)

        num = 3
        origin = DOWN.copy() * 0.7
        dots = [
            Dot(origin).set_z_index(2)
            for _ in range(num)
        ]
        dots_titles = [
            Tex(f'${chr(ord("A") + idx)}$', font_size=FONT_SIZE, tex_template=RUS_TEMPLATE).set_z_index(2)
            for idx in range(num)
        ]
        dots_titles[1], dots_titles[2] = dots_titles[2], dots_titles[1]
        lines = [
            Line(prev.get_center(), nxt.get_center(), color=GREEN) for prev, nxt in zip(dots, dots[1:] + dots[:1])
        ]
        norm_lines = [
            Line(color=RED).add_updater(norm_line_updater(first, second, third, z_index=1))
            for first, second, third in zip(dots, dots[1:] + dots, dots[2:] + dots)
        ]
        norm_dots = [
            Dot().set_z_index(2).add_updater(norm_dot_updater(first, second, third))
            for first, second, third in zip(dots, dots[1:] + dots, dots[2:] + dots)
        ]
        norm_dots_titles = [
            Tex(f'${chr(ord("E") + idx)}$', font_size=FONT_SIZE, tex_template=RUS_TEMPLATE).set_z_index(2)
            for idx in range(num)
        ][::-1]

        orthocenter = Dot().set_z_index(2).add_updater(orthocenter_updater(*dots))
        orthocenter.updaters[0](orthocenter)
        ortho_title = Tex(f'$H$', font_size=FONT_SIZE, tex_template=RUS_TEMPLATE).set_z_index(2).center()

        for line, prev, nxt in zip(lines, dots, dots[1:] + dots[:1]):
            line.add_updater(get_line_updater(prev, nxt, z_index=1))
        for line in norm_lines:
            line.updaters[0](line)
        for dot in norm_dots:
            dot.updaters[0](dot)

        triangle_word = altitude_prop[0][1].copy()
        self.play(
            Transform(triangle_word, dots[0])
        )
        self.remove(triangle_word)
        self.add(*dots)
        self.wait(DEFAULT_WAIT_TIME / 2)

        # Animate construction
        dot_centers = [dot.get_center() for dot in dots]
        locs = [1.35 * DOWN + 2.1 * LEFT, 2.1 * UP, 2.1 * DOWN + 3.75 * RIGHT]
        self.play(
            *[
                dot.animate.move_to(center + pos)
                for dot, center, pos in zip(dots, dot_centers, locs)
            ]
        )
        for title, dot in zip(dots_titles, dots):
            title.add_updater(get_dot_title_updater(dot, origin, fixed=True))
        self.play(
            Succession(
                *[
                    AnimationGroup(Create(line), Write(dot_title))
                    for line, dot_title in zip(lines, dots_titles)
                ]
            )
        )
        # noinspection PyTypeChecker
        self.play(
            *(
                [
                    Succession(Create(line), Create(dot))
                    for line, dot in zip(norm_lines, norm_dots)
                ] +
                [Create(orthocenter)]
            ),
            run_time=DEFAULT_WAIT_TIME * 2
        )

        right_angles = [
            Angle.from_three_points(
                second.get_center(), third.get_center(), first.get_center(), color=BLUE, elbow=True, radius=0.25
            )
            for first, second, third in zip(dots, dots[1:] + dots, norm_dots)
        ]
        for angle, first, second, third in zip(right_angles, dots, dots[1:] + dots, norm_dots):
            angle.add_updater(get_angle_updater(second, third, first))

        for title, dot in zip(norm_dots_titles, norm_dots):
            title.add_updater(get_dot_title_updater(dot, orthocenter, fixed=True))
        optimal_pos = (DOWN + RIGHT / 2) / 3
        ortho_title.move_to(orthocenter)
        ortho_title.shift(optimal_pos)
        always(ortho_title.move_to, orthocenter)
        always(ortho_title.shift, optimal_pos)

        self.play(
            *map(Write, norm_dots_titles + [ortho_title]),
            *map(Create, right_angles),
            run_time=DEFAULT_WAIT_TIME * 1.5
        )

        # Play with it
        steps = 5
        buff = 0.5
        min_r = 0.4
        random_walks = np.array(
            [
                get_random_walk(
                    dot, steps,
                    (
                        dot.get_center()[0] - buff,
                        dot.get_center()[1] - (buff * 1.5 if idx != 1 else buff * 0.6),
                        dot.get_center()[0] + buff,
                        dot.get_center()[1] + (buff * 1.5 if idx == 1 else buff * 0.6)
                    ),
                    min_r=min_r
                )
                for idx, dot in enumerate(dots)
            ]
        )
        random_walks = random_walks.transpose((1, 0, 2))
        for random_walk in random_walks:
            self.play(
                *[
                    AnimationGroup(
                        *[dot.animate.move_to(walk) for dot, walk in zip(dots, random_walk)],
                        run_time=DEFAULT_WAIT_TIME * 1.75
                    )
                ]
            )
        self.wait(DEFAULT_WAIT_TIME / 2)

        self.play(
            *[dot.animate.shift(2 * RIGHT) for dot in dots]
        )

        # Proof
        proof_fs = 1.25
        proof = create_tex_group(
            ALTITUDE_PROOF, LEFT, font_size=FONT_SIZE * proof_fs, tex_template=rus_template(256)
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(LEFT)

        right_angles[0].updaters = []
        right_angles[1].updaters = []
        right_angles[2].updaters = []

        aeb_angle = right_angles[2].copy()
        aeb_angle.updaters = []
        cfb_angle = right_angles[1]
        bec_angle = Angle.from_three_points(
            dots[2].get_center(), norm_dots[2].get_center(), dots[1].get_center(),
            color=BLUE, elbow=True, radius=0.25
        )
        afc_angle = Angle.from_three_points(
            dots[1].get_center(), norm_dots[1].get_center(), dots[0].get_center(),
            color=BLUE, elbow=True, radius=0.25
        )
        self.remove(right_angles[2])
        self.add(aeb_angle)

        self.play(
            FadeOut(right_angles[0]),
            Transform(aeb_angle, bec_angle),
            run_time=DEFAULT_WAIT_TIME * 2
        )
        self.remove(aeb_angle)
        self.add(bec_angle)

        self.play(
            AnimationGroup(
                Succession(
                    AnimationGroup(
                        cfb_angle.animate.set_stroke(width=DEFAULT_STROKE_WIDTH * 4),
                        bec_angle.animate.set_stroke(width=DEFAULT_STROKE_WIDTH * 4)
                    ),
                    AnimationGroup(
                        cfb_angle.animate.set_stroke(width=DEFAULT_STROKE_WIDTH),
                        bec_angle.animate.set_stroke(width=DEFAULT_STROKE_WIDTH)
                    ),
                ),
                mark_line(lines[1])
            ),
            run_time=DEFAULT_WAIT_TIME * 3
        )

        circle_1 = DashedVMobject(
            Circle(radius=lines[1].get_length() / 2, color=PURPLE)
            .center().move_to((dots[1].get_center() + dots[2].get_center()) / 2),
            num_dashes=30,
        )
        self.play(
            Create(circle_1)
        )

        ef_line = Line(norm_dots[1].get_center(), norm_dots[2].get_center(), color=MAROON).set_z_index(1)
        bce_angle = Angle.from_three_points(
            norm_dots[2].get_center(), dots[1].get_center(), dots[2].get_center(),
            color=YELLOW, radius=0.4
        ).set_z_index(2)
        efb_angle = Angle.from_three_points(
            dots[2].get_center(), norm_dots[1].get_center(), norm_dots[2].get_center(),
            color=ORANGE, radius=0.4
        ).set_z_index(2)
        self.play(
            Create(bce_angle), Create(efb_angle), Create(ef_line),
            run_time=DEFAULT_WAIT_TIME * 2
        )

        self.play(
            CreateThenFadeOut(
                Polygon(
                    norm_dots[2].get_center(), dots[1].get_center(), dots[2].get_center(), norm_dots[1].get_center(),
                    color=YELLOW, stroke_width=DEFAULT_STROKE_WIDTH * 2
                ).set_z_index(1)
            ),
            run_time=DEFAULT_WAIT_TIME * 2
        )
        bce_angle_cp = bce_angle.copy()
        efb_angle_cp = efb_angle.copy()
        self.play(
            AnimationGroup(
                Succession(
                    Transform(bce_angle_cp, proof[0][0]),
                    Write(proof[0][1]),
                    Transform(efb_angle_cp, proof[0][2])
                ),
                FadeOut(circle_1)
            ),
            run_time=DEFAULT_WAIT_TIME * 3
        )
        self.remove(bce_angle_cp, efb_angle_cp)
        self.add(proof[0][0], proof[0][2])

        # Second part
        bec_angle_cp = bec_angle.copy()
        cfb_angle_cp = cfb_angle.copy()
        aeb_angle = right_angles[2].copy()
        self.remove(bec_angle, cfb_angle)
        self.add(bec_angle_cp, cfb_angle_cp)
        self.play(Transform(bec_angle_cp, aeb_angle), Transform(cfb_angle_cp, afc_angle))
        self.remove(bec_angle_cp, cfb_angle_cp)
        self.add(aeb_angle, afc_angle)

        ahe_angle = Angle.from_three_points(
            norm_dots[2].get_center(), orthocenter.get_center(), dots[0].get_center(),
            color=WHITE, radius=0.4
        ).set_z_index(0)
        afe_angle = Angle.from_three_points(
            norm_dots[2].get_center(), norm_dots[1].get_center(), dots[0].get_center(),
            color=WHITE, radius=0.4
        ).set_z_index(0)
        ah_line = Line(dots[0].get_center(), orthocenter.get_center()).set_z_index(1)

        self.play(
            AnimationGroup(
                Succession(
                    AnimationGroup(
                        aeb_angle.animate.set_stroke(width=DEFAULT_STROKE_WIDTH * 4),
                        afc_angle.animate.set_stroke(width=DEFAULT_STROKE_WIDTH * 4)
                    ),
                    AnimationGroup(
                        aeb_angle.animate.set_stroke(width=DEFAULT_STROKE_WIDTH),
                        afc_angle.animate.set_stroke(width=DEFAULT_STROKE_WIDTH)
                    ),
                ),
                mark_line(ah_line)
            ),
            run_time=DEFAULT_WAIT_TIME * 3
        )

        circle_2_center = (dots[0].get_center() + orthocenter.get_center()) / 2
        circle_2 = DashedVMobject(
            Circle(radius=ah_line.get_length() / 2, color=PURPLE)
            .center().move_to(circle_2_center),
            num_dashes=20,
        )
        self.play(
            Create(circle_2)
        )
        self.wait(DEFAULT_WAIT_TIME / 2)

        eo_2 = norm_dots[2].get_center() - circle_2_center
        ao_2 = dots[0].get_center() - circle_2_center
        arc_ea = Arc(
            ah_line.get_length() / 2,
            np.arctan2(eo_2[1], eo_2[0]),
            angle_between_vectors(eo_2, ao_2),
            arc_center=circle_2_center,
            color=YELLOW,
            stroke_width=DEFAULT_STROKE_WIDTH * 2
        )
        self.play(
            CreateThenFadeOut(arc_ea),
            run_time=DEFAULT_WAIT_TIME * 1.5
        )
        self.play(
            Create(ahe_angle), Create(afe_angle),
            run_time=DEFAULT_WAIT_TIME * 1.5
        )

        ahe_angle_cp = ahe_angle.copy()
        afe_angle_cp = afe_angle.copy()
        self.play(
            AnimationGroup(
                Succession(
                    Transform(afe_angle_cp, proof[1][0]),
                    Write(proof[1][1]),
                    Transform(ahe_angle_cp, proof[1][2])
                ),
                FadeOut(circle_2)
            ),
            run_time=DEFAULT_WAIT_TIME * 3
        )
        self.remove(ahe_angle_cp, afe_angle_cp)
        self.add(proof[1][0], proof[1][2])

        # Third part
        proof_0_cp = proof[0].copy()
        proof_1_0_cp = proof[1][0].copy()

        self.play(
            AnimationGroup(
                Succession(
                    AnimationGroup(
                        efb_angle.animate.set_stroke(width=DEFAULT_STROKE_WIDTH * 4),
                        afe_angle.animate.set_stroke(width=DEFAULT_STROKE_WIDTH * 4)
                    ),
                    AnimationGroup(
                        FadeOut(efb_angle),
                        FadeOut(afe_angle)
                    ),
                ),
                mark_line(lines[2])
            ),
            run_time=DEFAULT_WAIT_TIME * 1.5
        )

        new_buff = DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 1.05
        self.play(
            proof_0_cp.animate.next_to(
                proof[1], DOWN, aligned_edge=LEFT, buff=new_buff
            )
        )
        self.play(
            LaggedStart(
                Transform(proof_1_0_cp, proof[2][3]),
                Transform(proof_0_cp[2], proof[2][2:]),
                lag_ratio=0.08
            ),
            run_time=DEFAULT_WAIT_TIME * 1.75
        )
        self.remove(proof_0_cp[2], proof_0_cp[1], proof_0_cp[0], proof_1_0_cp)
        self.add(proof[2])

        equality_1 = Tex(
            *[r'$\angle BCE$', r' $=$ ', r'$\angle AFE$'],
            font_size=FONT_SIZE * proof_fs,
            tex_template=RUS_TEMPLATE
        ).next_to(proof[1], DOWN, aligned_edge=LEFT, buff=new_buff)
        equality_2 = Tex(
            *[r'$\angle BCE$', r' $=$ ', r'$\angle AHE$'],
            font_size=FONT_SIZE * proof_fs,
            tex_template=RUS_TEMPLATE
        ).next_to(proof[1], DOWN, aligned_edge=LEFT, buff=new_buff)

        proof_1_2_cp = proof[1][2].copy()

        self.play(
            Transform(proof[2][1:], equality_1[1:]),
            run_time=DEFAULT_WAIT_TIME * 1.5
        )
        self.wait(DEFAULT_WAIT_TIME * 0.4)
        self.remove(proof[2][0], proof[2][1], proof[2][2], proof[2][3], proof[2][4])
        self.add(equality_1)

        self.play(
            Transform(equality_1[2], equality_2[2]), Transform(proof_1_2_cp, equality_2[2]),
            run_time=DEFAULT_WAIT_TIME * 1.5
        )
        self.wait(DEFAULT_WAIT_TIME * 0.4)
        self.remove(equality_1, proof_1_2_cp)
        self.add(equality_2)

        # Fourth part
        equality_3 = Tex(
            *[r'$\angle BCE$', r' $=$ ', r'$180^\circ-$ ', r'$\angle EHG$'],
            font_size=FONT_SIZE * proof_fs,
            tex_template=RUS_TEMPLATE
        ).next_to(proof[1], DOWN, aligned_edge=LEFT, buff=new_buff)
        equality_4 = Tex(
            *[r'$\angle BCE$', r' $+$ ', r'$\angle EHG$', r' $=$ ', r'$180^\circ$'],
            font_size=FONT_SIZE * proof_fs,
            tex_template=RUS_TEMPLATE
        ).next_to(proof[1], DOWN, aligned_edge=LEFT, buff=new_buff)

        ehg_angle = Angle.from_three_points(
            norm_dots[0].get_center(), orthocenter.get_center(), norm_dots[2].get_center(),
            color=MAROON, radius=0.4
        ).set_z_index(0)
        self.play(mark_line(norm_lines[0]), run_time=DEFAULT_WAIT_TIME * 1.75)
        self.play(Create(ehg_angle), Uncreate(ahe_angle), run_time=DEFAULT_WAIT_TIME * 1.75)

        efg_angle_cp = ehg_angle.copy()
        self.play(
            Transform(equality_2[2], equality_3[2:]),
            Transform(efg_angle_cp, equality_3[3]),
            run_time=DEFAULT_WAIT_TIME * 1.75
        )
        self.wait(DEFAULT_WAIT_TIME * 0.4)
        self.remove(equality_2, efg_angle_cp)
        self.add(equality_3)

        self.play(
            Transform(equality_3, equality_4),
            run_time=DEFAULT_WAIT_TIME * 1.5
        )
        self.wait(DEFAULT_WAIT_TIME * 0.4)
        self.remove(equality_3)
        self.add(equality_4)

        aeb_angle_cp = aeb_angle.copy()
        self.remove(aeb_angle)
        self.add(aeb_angle_cp)
        self.play(
            Transform(aeb_angle_cp, bec_angle),
            CreateThenFadeOut(
                Polygon(
                    norm_dots[2].get_center(), dots[1].get_center(),
                    norm_dots[0].get_center(), orthocenter.get_center(),
                    color=YELLOW, stroke_width=DEFAULT_STROKE_WIDTH * 2
                ).set_z_index(1)
            ),
            run_time=DEFAULT_WAIT_TIME * 1.75
        )
        self.remove(aeb_angle_cp)
        self.add(bec_angle)

        proof[3].to_edge(DL)
        self.play(Write(proof[3]), run_time=DEFAULT_WAIT_TIME * 1.5)
        self.play(
            CreateThenFadeOut(
                SurroundingRectangle(proof[3][:5])
            ),
            run_time=DEFAULT_WAIT_TIME * 1.75
        )
        self.play(
            Succession(
                AnimationGroup(
                    bce_angle.animate.set_stroke(width=DEFAULT_STROKE_WIDTH * 4),
                    ehg_angle.animate.set_stroke(width=DEFAULT_STROKE_WIDTH * 4)
                ),
                AnimationGroup(
                    bce_angle.animate.set_stroke(width=DEFAULT_STROKE_WIDTH),
                    ehg_angle.animate.set_stroke(width=DEFAULT_STROKE_WIDTH)
                ),
            ),
            run_time=DEFAULT_WAIT_TIME * 1.75
        )

        equality_4_end = Tex(
            r'$180^\circ$',
            font_size=FONT_SIZE * proof_fs,
            tex_template=RUS_TEMPLATE
        ).next_to(proof[3][:3], ORIGIN)
        equality_5 = Tex(
            r'$90^\circ$',
            font_size=FONT_SIZE * proof_fs,
            tex_template=RUS_TEMPLATE
        ).next_to(proof[3][4], ORIGIN)
        equality_6 = Tex(
            *[r'$\angle AGC$', r' $=$ ', r'$90^\circ$'],
            font_size=FONT_SIZE * proof_fs,
            tex_template=RUS_TEMPLATE
        ).next_to(proof[2], DOWN, aligned_edge=LEFT, buff=new_buff)

        self.play(
            Transform(proof[3][:3], equality_4_end),
            run_time=DEFAULT_WAIT_TIME * 1.5
        )

        self.play(
            bec_angle.animate.set_stroke(width=DEFAULT_STROKE_WIDTH * 4),
            run_time=DEFAULT_WAIT_TIME * 0.9
        )
        self.play(
            bec_angle.animate.set_stroke(width=DEFAULT_STROKE_WIDTH),
            run_time=DEFAULT_WAIT_TIME * 0.9
        )
        self.play(
            Transform(proof[3][4], equality_5),
            run_time=DEFAULT_WAIT_TIME * 1.5
        )
        self.wait(DEFAULT_WAIT_TIME * 0.4)
        self.play(
            Transform(proof[3], equality_6),
            run_time=DEFAULT_WAIT_TIME * 1.5
        )
        self.wait(DEFAULT_WAIT_TIME * 0.4)
        self.play(
            Create(
                SurroundingRectangle(proof[3])
            ),
            Create(right_angles[0]),
            FadeOut(bce_angle, ehg_angle, ef_line),
            run_time=DEFAULT_WAIT_TIME * 1.75
        )
        self.play(
            right_angles[0].animate.set_stroke(width=DEFAULT_STROKE_WIDTH * 4),
            run_time=DEFAULT_WAIT_TIME * 1.25
        )
        self.play(
            right_angles[0].animate.set_stroke(width=DEFAULT_STROKE_WIDTH),
            run_time=DEFAULT_WAIT_TIME * 1.25
        )


THALES_THEOREM_TEXTS = [
    [r'\raggedright \textbf{Теорема Фалеса.} Пусть две стороны ', r'угла',
     r' пересечены параллельными прямыми $AA_1,BB_1,CC_1,DD_1$. Тогда если ', r'$AB=CD$', r', то $A_1B_1=C_1D_1$.'],
    r'\emph{Доказательство:}',
]
THALES_THEOREM_PROOF = [
    [r'$AB_2$', r' $\parallel$ ', r'$A_1D_1$', r' $\parallel$ ', r'$CD_2$'],
    [r'$\angle BAB_2$', r' $=$ ', r'$\angle DCD_2$'],
    [r'$BB_1$', r' $\parallel$ ', r'$DD_1$'],
    [r'$\angle ABB_2$', r' $=$ ', r'$\angle CDD_2$'],
    [r'$AB$', r' $=$ ', r'$CD$'],
    [r'$\triangle ABB_2$', r' $=$ ', r'$\triangle CDD_2$'],
    [r'$AB_2$', r' $=$ ', r'$CD_2$'],
    [r'$A_1B_1$', r' $=$ ', r'$C_1D_1$'],
]


class Scene8(Common):
    @staticmethod
    def meta_construct(self: Scene):
        thales_theorem = create_tex_group(
            THALES_THEOREM_TEXTS, LEFT, font_size=FONT_SIZE, tex_template=RUS_TEMPLATE
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(UL)
        # self.add(thales_theorem)
        write_tex_group(thales_theorem, self, buf_time=DEFAULT_WAIT_TIME / 2)

        num = 4
        ang_scale = 3
        origin = DOWN.copy() * 2.5
        start_from_1 = ang_scale * (LEFT * 1.7)
        start_from_2 = ang_scale * (LEFT * 1.4 + DOWN * 0.3)

        ang_dots = [
            Dot(origin).set_z_index(2),
            Dot(origin + ang_scale * RIGHT, fill_opacity=0).set_z_index(2),
            Dot(origin + ang_scale * (1.4 * UP + RIGHT), fill_opacity=0).set_z_index(2)
        ]
        pl_dots = [
            Dot(ang_dots[2].get_center() + start_from_1 + idx * RIGHT * 1.1, fill_opacity=0)
            for idx in range(num)
        ] + [
            Dot(ang_dots[1].get_center() + start_from_2 + idx * RIGHT * 1.1, fill_opacity=0)
            for idx in range(num)
        ]
        pli_dots = [
            Dot().set_z_index(2).add_updater(intersection_updater(first, second, third, fourth))
            for first, second, third, fourth in zip(pl_dots, pl_dots[num:], [ang_dots[0]] * 4, [ang_dots[2]] * 4)
        ] + [
            Dot().set_z_index(2).add_updater(intersection_updater(first, second, third, fourth))
            for first, second, third, fourth in zip(pl_dots, pl_dots[num:], [ang_dots[0]] * 4, [ang_dots[1]] * 4)
        ]

        ang_lines = [
            Line(ang_dots[0].get_center(), ang_dots[1].get_center(), color=GREEN)
            .add_updater(get_line_updater(ang_dots[0], ang_dots[1], z_index=1)),
            Line(ang_dots[0].get_center(), ang_dots[2].get_center(), color=GREEN)
            .add_updater(get_line_updater(ang_dots[0], ang_dots[2], z_index=1))
        ]
        pl_lines = [
            Line(start.get_center(), end.get_center(), color=RED)
            .add_updater(get_line_updater(start, end, z_index=1))
            for start, end in zip(pl_dots, pl_dots[num:])
        ]

        pl_dots_titles = [
            Tex(f'${chr(ord("A") + idx)}$', font_size=FONT_SIZE, tex_template=RUS_TEMPLATE).center().set_z_index(2)
            for idx in range(num)
        ] + [
            Tex(f'${chr(ord("A") + idx)}_1$', font_size=FONT_SIZE, tex_template=RUS_TEMPLATE).center().set_z_index(2)
            for idx in range(num)
        ]

        for title, dot in zip(pl_dots_titles[:num], pli_dots[:num]):
            always(title.move_to, dot)
            always(title.shift, UP / 10 + LEFT / 3)
        for title, dot in zip(pl_dots_titles[num:], pli_dots[num:]):
            always(title.move_to, dot)
            always(title.shift, DOWN / 5 + LEFT / 5)

        # Construct
        angle_word = thales_theorem[0][1].copy()
        self.play(
            Transform(angle_word, ang_dots[0])
        )
        self.remove(angle_word)
        self.add(*ang_dots)
        self.wait(DEFAULT_WAIT_TIME / 2)

        self.play(ang_dots[0].animate.shift(ang_scale * LEFT))
        self.play(
            *map(Create, ang_lines),
            run_time=DEFAULT_WAIT_TIME * 1.75
        )
        self.play(
            *[
                Succession(Create(line), AnimationGroup(Create(first), Create(second)))
                for line, first, second in zip(pl_lines, pli_dots[:num], pli_dots[num:])
            ],
            run_time=DEFAULT_WAIT_TIME * 1.75
        )
        self.play(
            *map(Write, pl_dots_titles),
            run_time=DEFAULT_WAIT_TIME * 1.75
        )

        # Play with params
        proof_fs = 1.2
        config['tex_template'] = RUS_TEMPLATE

        cd_ab_length = DecimalNumber(
            np.linalg.norm(pli_dots[0].get_center() - pli_dots[1].get_center()),
            num_decimal_places=2,
            font_size=FONT_SIZE * proof_fs
        )
        cd_ab_length.add_updater(
            lambda z: z.set_value(np.linalg.norm(pli_dots[0].get_center() - pli_dots[1].get_center()))
        )
        cd_ab_length_overall = VGroup(
            Tex(r'$AB=CD=$ ', font_size=FONT_SIZE * proof_fs),
            cd_ab_length
        ).arrange(RIGHT, aligned_edge=ORIGIN, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER / 2)

        a1b1_length = DecimalNumber(
            np.linalg.norm(pli_dots[4].get_center() - pli_dots[5].get_center()),
            num_decimal_places=2,
            font_size=FONT_SIZE * proof_fs
        )
        a1b1_length.add_updater(
            lambda z: z.set_value(np.linalg.norm(pli_dots[4].get_center() - pli_dots[5].get_center()))
        )
        c1d1_length = DecimalNumber(
            np.linalg.norm(pli_dots[6].get_center() - pli_dots[7].get_center()),
            num_decimal_places=2,
            font_size=FONT_SIZE * proof_fs
        )
        c1d1_length.add_updater(
            lambda z: z.set_value(np.linalg.norm(pli_dots[6].get_center() - pli_dots[7].get_center()))
        )

        a1b1_length_overall = VGroup(
            Tex(r'$A_1B_1=$ ', font_size=FONT_SIZE * proof_fs),
            a1b1_length
        ).arrange(RIGHT, aligned_edge=ORIGIN, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 0.6)
        c1d1_length_overall = VGroup(
            Tex(r'$C_1D_1=$ ', font_size=FONT_SIZE * proof_fs),
            c1d1_length
        ).arrange(RIGHT, aligned_edge=ORIGIN, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 0.6)

        info_group = VGroup(cd_ab_length_overall, a1b1_length_overall, c1d1_length_overall)\
            .arrange(DOWN, aligned_edge=LEFT).to_edge(LEFT)
        sr_rects = [
            SurroundingRectangle(a1b1_length),
            SurroundingRectangle(c1d1_length),
        ]

        self.play(Write(info_group))
        self.play(*map(Create, sr_rects))

        scale_1 = 0.6
        self.play(
            ang_dots[1].animate.shift(DOWN * scale_1),
            ang_dots[2].animate.shift(UP * scale_1),
            run_time=DEFAULT_WAIT_TIME * 1.75
        )
        self.play(
            ang_dots[1].animate.shift(UP * scale_1 * 2),
            ang_dots[2].animate.shift(DOWN * scale_1 * 2),
            run_time=DEFAULT_WAIT_TIME * 1.75
        )
        self.play(
            ang_dots[1].animate.shift(DOWN * scale_1),
            ang_dots[2].animate.shift(UP * scale_1),
            run_time=DEFAULT_WAIT_TIME * 1.75
        )

        scale_2 = 0.8
        self.play(
            pl_dots[0].animate.shift(LEFT * scale_2),
            pl_dots[3].animate.shift(RIGHT * scale_2),
            pl_dots[4].animate.shift(LEFT * scale_2),
            pl_dots[7].animate.shift(RIGHT * scale_2),
            run_time=DEFAULT_WAIT_TIME * 1.75
        )
        self.play(
            pl_dots[0].animate.shift(RIGHT * scale_2),
            pl_dots[3].animate.shift(LEFT * scale_2),
            pl_dots[4].animate.shift(RIGHT * scale_2),
            pl_dots[7].animate.shift(LEFT * scale_2),
            run_time=DEFAULT_WAIT_TIME * 1.75
        )
        self.wait(DEFAULT_WAIT_TIME / 2)
        self.play(
            FadeOut(info_group),
            FadeOut(*sr_rects)
        )
        self.wait(DEFAULT_WAIT_TIME / 2)

        # Proof
        proof = create_tex_group(
            THALES_THEOREM_PROOF, LEFT, font_size=FONT_SIZE * proof_fs, tex_template=rus_template(256)
        ).to_edge(LEFT)

        add_dots = [
            Dot(
                find_intersection(
                   [pli_dots[idx * 2].get_center()],
                   [ang_dots[1].get_center() - ang_dots[0].get_center()],
                   [pli_dots[idx * 2 + 1].get_center()],
                   [pli_dots[idx * 2 + 5].get_center() - pli_dots[idx * 2 + 1].get_center()]
                )[0]
            ).set_z_index(2)
            for idx in range(num // 2)
        ]
        add_dots_titles = [
            Tex(f'${chr(ord("B") + idx * 2)}_2$', font_size=FONT_SIZE, tex_template=RUS_TEMPLATE)
            .center().set_z_index(2)
            for idx in range(num // 2)
        ]
        add_lines = [
            Line(prev.get_center(), nxt.get_center(), color=BLUE)
            for prev, nxt in zip([pli_dots[0], pli_dots[2]], add_dots)
        ]
        for title, dot in zip(add_dots_titles, add_dots):
            title.next_to(dot, RIGHT / 100)

        add_angles_1 = [
            Angle.from_three_points(
                first.get_center(), second.get_center(), third.get_center(),
                radius=0.4, color=YELLOW
            ).set_z_index(0)
            for first, second, third in zip(add_dots, [pli_dots[0], pli_dots[2]], [pli_dots[1], pli_dots[3]])
        ]
        add_angles_2 = [
            Angle.from_three_points(
                first.get_center(), second.get_center(), third.get_center(),
                radius=0.4, color=PURPLE
            ).set_z_index(0)
            for first, second, third in zip([pli_dots[0], pli_dots[2]], [pli_dots[1], pli_dots[3]], add_dots)
        ]

        self.play(*map(Create, add_lines))
        self.play(*map(Create, add_dots))
        self.play(*map(Write, add_dots_titles))

        # First part
        proof[0].next_to(proof[1], UP, aligned_edge=LEFT)
        proof[1].next_to(proof[1], UP, aligned_edge=LEFT)

        self.play(
            mark_line(ang_lines[0]),
            mark_line(Line(pli_dots[0].get_center(), add_dots[0].get_center()).set_z_index(1)),
            mark_line(Line(pli_dots[2].get_center(), add_dots[1].get_center()).set_z_index(1)),
            Write(proof[0]),
            run_time=DEFAULT_WAIT_TIME * 1.75
        )
        self.play(
            mark_line(ang_lines[1]),
            run_time=DEFAULT_WAIT_TIME * 1.75
        )
        self.play(
            *map(Create, add_angles_1),
            Transform(proof[0], proof[1]),
            run_time=DEFAULT_WAIT_TIME * 1.75
        )
        self.remove(proof[0])
        self.add(proof[1])

        # proof[2].next_to(proof[1], DOWN, aligned_edge=LEFT)
        # proof[3].next_to(proof[1], DOWN, aligned_edge=LEFT)
        self.play(
            mark_line(pl_lines[1]),
            mark_line(pl_lines[3]),
            Write(proof[2]),
            run_time=DEFAULT_WAIT_TIME * 1.75
        )
        self.play(
            mark_line(ang_lines[1]),
            run_time=DEFAULT_WAIT_TIME * 1.75
        )
        self.play(
            *map(Create, add_angles_2),
            Transform(proof[2], proof[3]),
            run_time=DEFAULT_WAIT_TIME * 1.75
        )
        self.remove(proof[2])
        self.add(proof[3])

        proof[4].next_to(proof[3], DOWN, aligned_edge=LEFT)
        ab_cd_word = thales_theorem[0][3].copy()
        self.play(
            mark_line(Line(pli_dots[0].get_center(), pli_dots[1].get_center()).set_z_index(1)),
            mark_line(Line(pli_dots[2].get_center(), pli_dots[3].get_center()).set_z_index(1)),
            Transform(ab_cd_word, proof[4]),
            run_time=DEFAULT_WAIT_TIME * 1.75
        )
        self.remove(ab_cd_word)
        self.add(proof[4])
        self.wait(DEFAULT_WAIT_TIME / 2)

        self.play(
            AnimationGroup(
                Succession(
                    AnimationGroup(
                        add_angles_1[0].animate.set_stroke(width=DEFAULT_STROKE_WIDTH * 4),
                        add_angles_1[1].animate.set_stroke(width=DEFAULT_STROKE_WIDTH * 4),
                        add_angles_2[0].animate.set_stroke(width=DEFAULT_STROKE_WIDTH * 4),
                        add_angles_2[1].animate.set_stroke(width=DEFAULT_STROKE_WIDTH * 4),
                    ),
                    AnimationGroup(
                        add_angles_1[0].animate.set_stroke(width=DEFAULT_STROKE_WIDTH),
                        add_angles_1[1].animate.set_stroke(width=DEFAULT_STROKE_WIDTH),
                        add_angles_2[0].animate.set_stroke(width=DEFAULT_STROKE_WIDTH),
                        add_angles_2[1].animate.set_stroke(width=DEFAULT_STROKE_WIDTH),
                    )
                ),
                CreateThenFadeOut(SurroundingRectangle(VGroup(proof[1], proof[3])))
            ),
            run_time=DEFAULT_WAIT_TIME * 2
        )
        self.wait(DEFAULT_WAIT_TIME * 0.4)

        self.play(
            CreateThenFadeOut(
                SurroundingRectangle(VGroup(proof[1:5]))
            ),
            run_time=DEFAULT_WAIT_TIME * 1.75
        )
        self.play(
            Transform(proof[1:5], proof[5]),
            run_time=DEFAULT_WAIT_TIME * 1.5
        )
        self.remove(proof[1], proof[3], proof[4])
        self.add(proof[5])

        self.play(
            CreateThenFadeOut(
                Polygon(
                    pli_dots[0].get_center(), pli_dots[1].get_center(), add_dots[0].get_center(),
                    color=YELLOW, stroke_width=DEFAULT_STROKE_WIDTH * 2
                ).set_z_index(1)
            ),
            CreateThenFadeOut(
                Polygon(
                    pli_dots[2].get_center(), pli_dots[3 ].get_center(), add_dots[1].get_center(),
                    color=YELLOW, stroke_width=DEFAULT_STROKE_WIDTH * 2
                ).set_z_index(1)
            ),
            Transform(proof[5], proof[6]),
            run_time=DEFAULT_WAIT_TIME * 1.75
        )
        self.remove(proof[5])
        self.add(proof[6])
        self.wait(DEFAULT_WAIT_TIME / 5)

        self.play(
            CreateThenFadeOut(
                Polygon(
                    pli_dots[0].get_center(), add_dots[0].get_center(),
                    pli_dots[5].get_center(), pli_dots[4].get_center(),
                    color=YELLOW, stroke_width=DEFAULT_STROKE_WIDTH * 2
                ).set_z_index(1)
            ),
            CreateThenFadeOut(
                Polygon(
                    pli_dots[2].get_center(), add_dots[1].get_center(),
                    pli_dots[7].get_center(), pli_dots[6].get_center(),
                    color=YELLOW, stroke_width=DEFAULT_STROKE_WIDTH * 2
                ).set_z_index(1)
            ),
            Transform(proof[6], proof[7]),
            run_time=DEFAULT_WAIT_TIME * 1.75
        )
        self.wait(DEFAULT_WAIT_TIME / 5)
        self.remove(proof[6])
        self.add(proof[7])

        sr_rect = SurroundingRectangle(proof[7])
        self.play(
            Create(sr_rect),
            FadeOut(*add_angles_1, *add_angles_2, *add_dots, *add_lines, *add_dots_titles),
            mark_line(Line(pli_dots[4].get_center(), pli_dots[5].get_center()).set_z_index(1)),
            mark_line(Line(pli_dots[6].get_center(), pli_dots[7].get_center()).set_z_index(1)),
            run_time=DEFAULT_WAIT_TIME * 1.75
        )


if __name__ == '__main__':
    with tempconfig({'quality': 'high_quality', 'preview': True, 'media_dir': 'media'}):
        scene = Common(__name__)
        scene.render()
