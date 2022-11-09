from helpers import RUS_TEMPLATE, Common
from helpers.text_utils import create_tex_group, write_tex_group, straight_forward_proof, fade_out_objects
from manim import *

FONT_SIZE = DEFAULT_FONT_SIZE / 1.5
QED = Tex(r'$\blacksquare$', font_size=FONT_SIZE,
          tex_template=RUS_TEMPLATE, tex_to_color_map={r'$\blacksquare$': GREEN})
DIOPHANTINE_EQ_DEF_TEXTS = [
    r'\textbf{Диофантовы уравнения \textendash\ это уравнения в целых числах}:',
    r'\begin{itemize} \item пифагоровы тройки \textendash\ целочисленные решения уравнения $a^2+b^2=c^2$ \textendash\ '
    r'интересовали математиков уже в древнем Вавилоне ок. 4 тыс. лет назад; \end{itemize}',
    r'\begin{itemize} \item великая теорема Ферма, ставящая вопрос об отсутствии ненулевых целочисленных решений '
    r'уравнения $a^n+b^n=c^n$ для целых $n>2$ и сформулированная в сер. XVII века, волновала величайшие умы вплоть '
    r'до кон. XX века, когда была наконец доказана; \end{itemize}',
    r'\begin{itemize} \item 10-я проблема Гильберта, вошедшая в 1900 г. в его список из 23 важнейших проблем '
    r'математики и ставящая вопрос о существовании общего алгоритма решения диофантовых уравнений, была решена лишь '
    r'70 лет спустя с неутешительным вердиктом: нет, общего алгоритма существовать не может. \end{itemize}'
]


# Diophantine equations definition
class Scene1(Common):
    @staticmethod
    def meta_construct(self: Scene):
        diophantine_def = create_tex_group(
            DIOPHANTINE_EQ_DEF_TEXTS, LEFT, font_size=FONT_SIZE, tex_template=RUS_TEMPLATE
        ).arrange(DOWN, center=True, aligned_edge=LEFT).to_edge(LEFT)
        write_tex_group(diophantine_def, self)


LIN_DIOPHANTINE_EQ_DEF_TEXTS = [
    r'\raggedright \textbf{Линейное диофантово уравнение с двумя неизвестными} \textendash\ это уравнение вида '
    r'$a$$x$$+$$b$$y$$=$$c$ для целочисленных неизвестных $x,y$ и (тоже целых) чисел $a$, $b$, $c$.',
    r'\raggedright Давайте условимся, что $a$$^2+$$b$$^2\ne0$, иначе получим равенство вида $a$$x$$=$$c$ '
    r'либо $0=$$c$ \textendash\ оба случая тривиальны, и мы предоставим читателю самостоятельно разобрать их. '
    r'Итак, далее считаем $a$$\ne0$ и $b$$\ne0$'
]


# Linear diophantine equations definition
class Scene2(Common):
    @staticmethod
    def meta_construct(self: Scene):
        lin_diophantine_def = create_tex_group(
            LIN_DIOPHANTINE_EQ_DEF_TEXTS, LEFT,
            font_size=FONT_SIZE,
            tex_template=RUS_TEMPLATE,
            c_maps={'$a$': BLUE, '$b$': TEAL, '$c$': GREEN}
        ).arrange(DOWN, center=True, aligned_edge=LEFT).to_edge(LEFT)
        write_tex_group(lin_diophantine_def, self)


THEOREM_1_TEXTS = [
    r'\raggedright \textbf{Теорема 1}. Уравнение $a$$x$$+$$b$$y$$=$$c$ с целыми $a$, $b$, $c$ имеет целочисленное '
    r'решение $($$x$,$y$$)$ тогда и только тогда, когда $c$ кратно $n$$=$НОД$($$a$,$b$$)$.',
    r'\textsl{Доказательство:}', r'$\Rightarrow$: ', r'$\Leftarrow$: ',
]
PROOF_RIGHT_1_TEXTS = [
    r'Существуют $x$,$y$ $\in \mathbb{Z}$, которые удовлетворяют $a$$x$$+$$b$$y$$=$$c$',
    r'$\Rightarrow$ ', r'$a$$x$ $\divby$ $n$ и $b$$y$ $\divby$ $n$', r'$\Rightarrow$ ',
    r'$a$$x$$+$$b$$y$ $\divby$ $n$', r'$\Rightarrow$ ', r'$c$ $\divby$ $n$', r'$\Rightarrow$ ',
    r'$c$ $\divby$ НОД$($$a$,$b$$)$'
]
PROOF_LEFT_1_TEXTS = [
    r'Будем считать, что числа $a$, $b$ взаимно простые, иначе поделим обе части равенства на НОД$($$a$,$b$$)$',
    r'$\Rightarrow$ ', r'Тогда, $a$$x_0$$+$$b$$y_0$ $=1$ будет иметь корни согласно лемме Безу',
    r'$\Rightarrow$ ', r'Следовательно, $($$c$$x_0$, $c$$y_0$$)$ является решением исходного уравнения'
]
TEX_TO_COLOR_MAP = {
    '$a$': BLUE, '$b$': TEAL, '$c$': GREEN, '$n$': RED, r'$\divby$': WHITE, '$x$': WHITE, '$y$': WHITE, '$t$': ORANGE
}


# Theorem 1 and proof
class Scene3(Common):
    @staticmethod
    def meta_construct(self: Scene):
        theorem_1 = create_tex_group(
            THEOREM_1_TEXTS, LEFT,
            font_size=FONT_SIZE,
            tex_template=RUS_TEMPLATE,
            c_maps=TEX_TO_COLOR_MAP
        ).arrange(DOWN, center=True, aligned_edge=LEFT).to_edge(LEFT).shift(UP / 2)
        theorem_1[-1].next_to(theorem_1[-1], DOWN)
        write_tex_group(theorem_1, self)

        # From right to left
        to_right_proof = create_tex_group(
            PROOF_RIGHT_1_TEXTS, LEFT, font_size=FONT_SIZE, tex_template=RUS_TEMPLATE,
            c_maps=TEX_TO_COLOR_MAP
        ).arrange(RIGHT)
        straight_forward_proof(self, to_right_proof, lambda z: z.next_to(theorem_1[-2]))

        box = SurroundingRectangle(to_right_proof[-1], buff=.1)
        self.play(Create(box))
        fade_out_objects(scene, to_right_proof[2:-1], 2)
        box_text = VGroup(to_right_proof[-1], box)
        self.play(box_text.animate.next_to(theorem_1[-2]))
        self.play(Transform(box_text, QED.copy().next_to(theorem_1[-2])))

        # From left to right
        to_left_proof = create_tex_group(
            PROOF_LEFT_1_TEXTS, LEFT, font_size=FONT_SIZE, tex_template=RUS_TEMPLATE,
            c_maps=TEX_TO_COLOR_MAP
        ).arrange(RIGHT)
        straight_forward_proof(self, to_left_proof, lambda z: z.next_to(theorem_1[-1]))

        box = SurroundingRectangle(to_left_proof[-1], buff=.1)
        self.play(Create(box))
        box_text = VGroup(to_left_proof[-1], box)
        qed = QED.copy().next_to(theorem_1[-1])
        self.play(Transform(box_text, qed))
        self.remove(box_text)
        self.add(qed)
        always(qed.next_to, theorem_1[-1])
        self.play(theorem_1[-1].animate.next_to(theorem_1[-2], DOWN))


THEOREM_2_TEXTS = [
    r'\raggedright \textbf{Теорема 2}. Если $(x_0,y_0)$ \textendash\ корень уравнения $a$$x$$+$$b$$y$$=$$c$, '
    r'то для любого целого $t$ пара $(x_0$$+$$b$$t$, $y_0-$$a$$t$$)$ \textendash\ тоже корень уравнения. '
    r'Более того, любой корень этого уравнения может быть представлен в виде $(x_0+$$b$$t$, $y_0-$$a$$t$$)$ '
    r'для некоторого целого $t$.',
    r'\textsl{Доказательство:}', r'$\Rightarrow$: ', r'$\Leftarrow$: ',
]
PROOF_RIGHT_2_TEXTS = [
    r'$a$$(x_0+$$b$$t$$)+$$b$$(y_0-$$a$$t$$)$',
    r' $=$ ', r'$a$$x_0+$$b$$y_0+$$a$$b$$t$$-$$a$$b$$t$', r' $=$ ',
    r'$a$$x_0+$$b$$y_0$', r' $=$ ', '$c$'
]
PROOF_LEFT_2_TEXTS = [
    r'Пусть пары $(x_0,y_0)$, $(x,y)$ \textendash\ корни исходного уравнения.',
    r'$\Rightarrow$', r'$a$$x+$$b$$y=$ $a$$x_0+$$b$$y_0=$ $c$', r'$\Rightarrow$',
    '$a$$(x-x_0)=$ $b$$(y_0-y)$', r'; ', r'Будем считать, что НОД$($$a$, $b$$)=1$',
    r'$\Rightarrow$', r'$x-x_0$ $\divby$ $b$ и $y_0-y$ $\divby$ $a$', r'$\Rightarrow$',
    '$x-x_0=$ $t$$b$, $y_0-y=$ $t$$a$', r'$\Rightarrow$', '$x=x_0+$$b$$t$, $y=y_0-$$a$$t$'
]


# Theorem 2 and proof
class Scene4(Common):
    @staticmethod
    def meta_construct(self: Scene):
        theorem_2 = create_tex_group(
            THEOREM_2_TEXTS, LEFT,
            font_size=FONT_SIZE,
            tex_template=RUS_TEMPLATE,
            c_maps=TEX_TO_COLOR_MAP
        ).arrange(DOWN, center=True, aligned_edge=LEFT).to_edge(LEFT).shift(UP / 2)
        theorem_2[-1].next_to(theorem_2[-1], DOWN)
        write_tex_group(theorem_2, self)

        # From right to left
        to_right_proof = create_tex_group(
            PROOF_RIGHT_2_TEXTS, LEFT, font_size=FONT_SIZE, tex_template=RUS_TEMPLATE,
            c_maps=TEX_TO_COLOR_MAP
        ).arrange(RIGHT)
        straight_forward_proof(self, to_right_proof, lambda z: z.next_to(theorem_2[-2]))

        box = SurroundingRectangle(to_right_proof[-1], buff=.1)
        self.play(Create(box))
        fade_out_objects(scene, to_right_proof[:-1], 2)
        box_text = VGroup(to_right_proof[-1], box)
        self.play(box_text.animate.next_to(theorem_2[-2]))
        self.play(Transform(box_text, QED.copy().next_to(theorem_2[-2])))

        # From left to right
        to_left_proof = create_tex_group(
            PROOF_LEFT_2_TEXTS, LEFT, font_size=FONT_SIZE, tex_template=RUS_TEMPLATE,
            c_maps=TEX_TO_COLOR_MAP
        ).arrange(RIGHT)
        straight_forward_proof(self, to_left_proof, lambda z: z.next_to(theorem_2[-1]))

        box = SurroundingRectangle(to_left_proof[-1], buff=.1)
        self.play(Create(box))
        fade_out_objects(scene, to_left_proof[:-1], 2)
        box_text = VGroup(to_left_proof[-1], box)
        self.play(box_text.animate.next_to(theorem_2[-1]))
        qed = QED.copy().next_to(theorem_2[-1])
        self.play(Transform(box_text, qed))
        self.remove(box_text)
        self.add(qed)
        always(qed.next_to, theorem_2[-1])
        self.play(theorem_2[-1].animate.next_to(theorem_2[-2], DOWN))


EXAMPLE_1_TEXTS = [
    r'\textbf{Пример 1.} Решить в целых числах уравнение $2$$x$ $-$ $7$$y$ $=4$',
    r'\emph{Решение:}'
]
SOLUTION_1_TEXTS = [
    r'Заметим, что $4$ кратно НОД$(2,-7)=1$', r'$\Rightarrow$', r'Корни есть', r';',
    r'Можно угадать один из них \textendash\ $(9,2)$', r'$\Rightarrow$',
    r'$(9-7$$t$,$2-2$$t$$)$ \textendash\ по \textbf{Теореме 2}'
]


# Example 1
class Scene5(Common):
    @staticmethod
    def meta_construct(self: Scene):
        c_map = {'$x$': GREEN_D, '$y$': BLUE_D, '$t$': ORANGE}
        example_1 = create_tex_group(
            EXAMPLE_1_TEXTS, LEFT,
            font_size=FONT_SIZE,
            tex_template=RUS_TEMPLATE,
            c_maps=c_map
        ).arrange(DOWN, center=True, aligned_edge=LEFT).to_edge(LEFT)
        write_tex_group(example_1, self)

        solution_1 = create_tex_group(
            SOLUTION_1_TEXTS, LEFT, font_size=FONT_SIZE, tex_template=RUS_TEMPLATE,
            c_maps=c_map
        ).arrange(RIGHT)
        straight_forward_proof(self, solution_1, lambda z: z.next_to(example_1[-1]))
        answer = Tex(r'$x$ $=9-7$$t$, $y$ $=2-2$$t$; $t$ $\in \mathbb{Z}$', font_size=FONT_SIZE,
                     tex_template=RUS_TEMPLATE, tex_to_color_map=c_map)

        box = SurroundingRectangle(solution_1[-1], buff=.1)
        self.play(Create(box))
        fade_out_objects(scene, solution_1[:-1], 2)
        box_text = VGroup(solution_1[-1], box)
        self.play(box_text.animate.next_to(example_1[-1]))
        self.wait(0.5)
        self.play(Transform(box_text, answer.next_to(example_1[-1])))


EXAMPLE_2_TEXTS = [
    r'\raggedright \textbf{Пример 2.} Остаток от деления некоторого натурального числа $n$ на $6$ равен $4$, '
    r'остаток от деления $n$ на $15$ равен $7$. Чему равен остаток от деления $n$ на $30$?',
    r'\emph{Решение:}'
]
SOLUTION_2_TEXTS = [
    r'$n$ $\equiv$ $4 \mod 6$ и $n$ $\equiv$ $7 \mod 15$', r'$\Rightarrow$',
    r'$n$ $=6$$x$$+4$ и $n$ $=15$$y$$+7$, для $x$,$y$$\ge0$', r'$\Rightarrow$',
    r'$6$$x$$+4$ $=15$$y$$+7$', r'$\Rightarrow$', '$2$$x$$-5$$y$ $=1$',
    r'Частное решение:', r'(-2,-1)', r'$\Rightarrow$',
    r'$(-2+5$$k$,$-1+2$$k$$)$ \textendash\ решение, для $k$ $\in \mathbb{Z}$', r';',
    r'$x$,$y$$\ge0$, значит, $k$$>0$', r'$\Rightarrow$', r'$n$ $=6$$x$$+4$', r'$=$',
    r'$6(-2+5$$k$$)+4$', r'$=$', r'$30$$k$$-8$', r'$=$', r'$30($$k$$-1)+22$', r'$\Rightarrow$',
    r'$n$ $\equiv$ $22 \mod 30$'
]


# Example 2
class Scene6(Common):
    @staticmethod
    def meta_construct(self: Scene):
        c_map = {'$x$': GREEN_D, '$y$': BLUE_D, '$n$': YELLOW, '$k$': RED_D}
        example_2 = create_tex_group(
            EXAMPLE_2_TEXTS, LEFT,
            font_size=FONT_SIZE,
            tex_template=RUS_TEMPLATE,
            c_maps=c_map
        ).arrange(DOWN, center=True, aligned_edge=LEFT).to_edge(LEFT)
        write_tex_group(example_2, self)

        solution_1 = create_tex_group(
            SOLUTION_2_TEXTS, LEFT, font_size=FONT_SIZE, tex_template=RUS_TEMPLATE,
            c_maps=c_map
        ).arrange(RIGHT)
        straight_forward_proof(self, solution_1, lambda z: z.next_to(example_2[-1]))
        answer = Tex(r'Остаток от деления $n$ на $30$ равен $22$', font_size=FONT_SIZE,
                     tex_template=RUS_TEMPLATE, tex_to_color_map=c_map)

        box = SurroundingRectangle(solution_1[-1], buff=.1)
        self.play(Create(box))
        fade_out_objects(scene, solution_1[:-1], 2)
        box_text = VGroup(solution_1[-1], box)
        self.play(box_text.animate.next_to(example_2[-1]))
        self.wait(0.5)
        self.play(Transform(box_text, answer.next_to(example_2[-1])))


if __name__ == '__main__':
    with tempconfig({'quality': 'high_quality', 'preview': True, 'media_dir': '../media'}):
        scene = Common(__name__)
        scene.render()
