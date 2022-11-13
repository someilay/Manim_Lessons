from random import random
from typing import Optional, Union as TUnion
from math import sqrt, ceil

import numpy as np
from manim import *


def make_interval_pos(start: float, end: float) -> tuple[float, float]:
    if start < 0:
        offset = ceil(-start / (2 * np.pi)) * 2 * np.pi
        return start + offset, end + offset
    return start, end


def get_angle_interval(center: np.ndarray, r: float,
                       x: Optional[float] = None, y: Optional[float] = None) -> tuple[float, float]:
    x_c, y_c = center

    if (x is None and y is None) or (x is not None and y is not None):
        raise ValueError('x either y should be initialized!')

    x1 = x2 = x
    y1 = y2 = y

    try:
        reverse_order = False
        if y is not None:
            reverse_order = True
            x1 = sqrt(r ** 2 - (y - y_c) ** 2) + x_c
            x2 = -sqrt(r ** 2 - (y - y_c) ** 2) + x_c
        if x is not None:
            reverse_order = x > x_c
            y1 = sqrt(r ** 2 - (x - x_c) ** 2) + y_c
            y2 = -sqrt(r ** 2 - (x - x_c) ** 2) + y_c

        theta_1 = np.arctan2(y1 - y_c, x1 - x_c)
        theta_2 = np.arctan2(y2 - y_c, x2 - x_c)

        if theta_1 == theta_2 and not reverse_order:
            theta_1 -= 2 * np.pi

        if theta_1 > theta_2:
            theta_1, theta_2 = theta_2, theta_1

        if reverse_order:
            theta_1, theta_2 = theta_2 - 2 * np.pi, theta_1

        return make_interval_pos(theta_1, theta_2)
    except ValueError:
        return 0, 2 * np.pi


def _split_interval(interval: tuple[float, float]) -> list[tuple[float, float]]:
    start, end = interval
    if end > 2 * np.pi:
        return [(start, 2 * np.pi), (0, end - 2 * np.pi)]
    return [interval]


def _unite_two_intervals(a: tuple[float, float], b: tuple[float, float]) -> Optional[tuple[float, float]]:
    start_a, end_a = a
    start_b, end_b = b

    if start_a == start_b and end_a == end_b:
        return start_a, end_a

    if start_a == start_b:
        return start_a, min(end_a, end_b)

    if end_a == end_b:
        return max(start_a, start_b), end_a

    if start_a < start_b:
        return (start_b, min(end_a, end_b)) if end_a >= start_b else None

    if start_a > start_b:
        return (start_a, min(end_a, end_b)) if end_b >= start_a else None


def sew_intervals(intervals: list[tuple[float, float]]) -> list[tuple[float, float]]:
    intervals = intervals.copy()
    intervals.sort(key=lambda z: z[0])
    idx = 1
    while idx < len(intervals):
        if intervals[idx][0] == intervals[idx - 1][1]:
            intervals[idx - 1] = (intervals[idx - 1][0], intervals[idx][1])
            intervals.pop(idx)
        else:
            idx += 1
    return intervals


def _unite_intervals(a: list[tuple[float, float]], b: list[tuple[float, float]]) -> list[tuple[float, float]]:
    res = []
    for sub_a in a:
        for sub_b in b:
            sub_unite = _unite_two_intervals(sub_a, sub_b)
            if sub_unite:
                res.append(sub_unite)
    return sew_intervals(res)


def unite_intervals(*intervals: tuple[float, float]) -> list[tuple[float, float]]:
    new_intervals = []
    for interval in intervals:
        new_intervals.append(_split_interval(interval))
    res = new_intervals[0] if new_intervals else []
    for sub_i in new_intervals[1:]:
        res = _unite_intervals(res, sub_i)
    return sew_intervals(res)


def random_interval_val(intervals: list[tuple[float, float]]) -> float:
    lengths = [end - start for start, end in intervals]
    common_l = sum(lengths)
    random_l = common_l * random()

    cumulative_l = 0
    for length, interval in zip(lengths, intervals):
        if random_l - cumulative_l <= length:
            return interval[0] + random_l - cumulative_l
        cumulative_l += length
    return intervals[-1][1]


def get_intersection(p: np.ndarray, angle: float, a: float, b: float, c: float) -> np.ndarray:
    direction = np.array([np.cos(angle), np.sin(angle)])
    r = np.array([np.sin(angle), -np.cos(angle)])
    m = np.array([r, [a, b]])
    d = np.array([p.dot(r), c])

    try:
        res = np.linalg.inv(m).dot(d) - p
        if direction.dot(res) > 0:
            return res
        return np.array([np.inf, np.inf])
    except np.linalg.LinAlgError:
        return np.array([np.inf, np.inf])


def get_random_move(p: np.ndarray, min_r: float, max_r: float,
                    constraints: tuple[float, float, float, float]) -> np.ndarray:
    if not min_r < max_r:
        raise ValueError('min_r should be less than max_r!')

    min_x, min_y, max_x, max_y = constraints
    if not min_x < max_x or not min_y < max_y:
        raise ValueError('Box(min_x, min_y, max_x, max_y) should be defined properly!')

    _p = p[:2]
    angles = unite_intervals(
        get_angle_interval(_p, min_r, x=min_x),
        get_angle_interval(_p, min_r, x=max_x),
        get_angle_interval(_p, min_r, y=min_y),
        get_angle_interval(_p, min_r, y=max_y),
    )

    if not angles:
        raise ValueError(f'Box for random walk is too small! '
                         f'p = {p}, constraints = {constraints}')

    r_angle = random_interval_val(angles)
    intersections = [
        get_intersection(_p, r_angle, 1, 0, min_x),
        get_intersection(_p, r_angle, 1, 0, max_x),
        get_intersection(_p, r_angle, 0, 1, min_y),
        get_intersection(_p, r_angle, 0, 1, max_y)
    ]
    closest = min(intersections, key=lambda x: x.dot(x))
    closest_l = np.linalg.norm(closest)
    scaler = min((random() * (max_r - min_r) / closest_l + min_r / closest_l), 0.99)
    res = closest * scaler
    return p + np.array([res[0], res[1], 0])


def get_random_walk(dot: Dot, steps: int, constraints: tuple[float, float, float, float],
                    min_r: float = 1.0, max_r: float = 2.0) -> list[np.ndarray]:
    initial = dot.get_center().copy()
    cur = dot.get_center().copy()
    animations = []
    for _ in range(steps):
        cur = get_random_move(cur, min_r, max_r, constraints)
        animations.append(cur)
    animations.append(initial)
    return animations


def get_dot_title_updater(dot: Dot, origin: TUnion[np.ndarray, Dot], scale: float = 0.33,
                          fixed: bool = False) -> Callable[[Mobject], None]:
    if not fixed and isinstance(origin, np.ndarray):
        return lambda z: z.move_to(dot.get_center() + normalize(dot.get_center() - origin) * scale)
    if not fixed and isinstance(origin, Dot):
        return lambda z: z.move_to(dot.get_center() + normalize(dot.get_center() - origin.get_center()) * scale)

    if isinstance(origin, Dot):
        origin = origin.get_center()
    shift = normalize(dot.get_center() - origin).copy()
    return lambda z: z.move_to(dot.get_center() + shift * scale)


def get_dot_updater(follow: Dot, shift: np.ndarray) -> Callable[[Mobject], None]:
    return lambda z: z.move_to(follow.get_center() + shift)


def get_optimal_title_loc(origin: Dot, dots: list[Dot]) -> np.ndarray:
    dot_1, dot_2 = max(
        zip(dots, dots[1:] + dots[:1]),
        key=lambda z: angle_between_vectors(
            z[0].get_center() - origin.get_center(), z[1].get_center() - origin.get_center()
        )
    )
    return normalize(
        normalize(dot_1.get_center() - origin.get_center()) + normalize(dot_2.get_center() - origin.get_center())
    )


if __name__ == '__main__':
    pass
