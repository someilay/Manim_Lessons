from manim import *
from typing import Optional, Callable, Union


def create_tex_group(texts: list[str], align: np.ndarray, font_size: float,
                     c_maps: Optional[Union[list[dict], dict]] = None, base_class: type = Tex, **kwargs) -> VGroup:
    if c_maps is None:
        c_maps = [dict()] * len(texts)
    if isinstance(c_maps, dict):
        c_maps = [c_maps] * len(texts)

    return VGroup(
        *[base_class(text, font_size=font_size, tex_to_color_map=c_map, **kwargs).align_to(align)
          for text, c_map in zip(texts, c_maps)]
    )


def write_tex_group(tex_group: VGroup, scene: Scene,
                    write_speed: float = 50, buf_time: float = DEFAULT_WAIT_TIME):
    for tex in tex_group:
        scene.play(Write(tex), run_time=min(len(tex.tex_string) / write_speed, DEFAULT_WAIT_TIME * 2))
        scene.wait(buf_time)


def fade_out_objects(scene: Scene, group: VGroup, tr_run_time: float):
    for obj in group:
        if obj in scene.mobjects:
            scene.play(FadeOut(obj), run_time=tr_run_time / len(group))


def straight_forward_proof(scene: Scene, proof: VGroup, move_to: Callable[[VGroup], None],
                           start_with: int = 0, tr_run_time: float = 2,
                           min_x: float = -7, max_x: float = 7, min_y: float = -4, max_y: float = 4):
    if not (min_x < max_x) or not (min_y < max_y):
        raise ValueError('min_x < max_x and min_y < max_y!')

    move_to(proof)
    if start_with > 0:
        scene.play(FadeIn(*proof[:start_with]))
    scene.play(FadeIn(proof[start_with]))

    first = start_with
    indexes1 = range(start_with, len(proof), 2)
    indexes2 = range(start_with + 1, len(proof), 2)
    indexes3 = range(start_with + 2, len(proof), 2)
    for prev, cur, nxt in zip(indexes1, indexes2, indexes3):
        if proof[nxt].get_right()[0] >= max_x:
            if prev == first:
                move_to(
                    VGroup(
                        *(list(proof[nxt:]))
                    ).arrange(RIGHT)
                )
                scene.play(Transform(proof[prev], proof[nxt]), run_time=tr_run_time)
                scene.remove(proof[prev])
                scene.add(proof[nxt])
                scene.wait(tr_run_time / 2)
                first = nxt
                continue

            fade_out_objects(scene, proof[first: prev], tr_run_time)
            scene.play(proof[prev].animate.move_to(proof[first], aligned_edge=LEFT), run_time=tr_run_time)
            move_to(
                VGroup(
                    *(list(proof[:start_with]) + list(proof[prev:]))
                ).arrange(RIGHT)
            )
            first = prev

        scene.play(FadeIn(proof[cur]))
        scene.play(
            TransformMatchingTex(
                proof[prev].copy(), proof[nxt],
                path_arc=PI / 2,
                transform_mismatches=True,
            ),
            run_time=tr_run_time
        )
