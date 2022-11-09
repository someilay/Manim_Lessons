from __future__ import annotations
import inspect
import sys

from manim import Scene
from typing import Optional, Iterable


def _extract_scene_num(class_name: str) -> int:
    try:
        return int(class_name[5:])
    except ValueError:
        return -1


def _get_scene_classes(module: str) -> Iterable[tuple[str, type[Common]]]:
    classes = inspect.getmembers(sys.modules[module], inspect.isclass)
    classes = filter(lambda c: c[1].__base__ == Common, classes)
    classes = filter(lambda c: c[1].__dict__.get('__module__', None) == module, classes)
    classes = sorted(classes, key=lambda x: _extract_scene_num(x[0]))
    return classes


class Common(Scene):
    def __init__(self, module: Optional[str] = None):
        super().__init__()
        self.__classes: Optional[list[tuple[str, type[Common]]]] = None
        if self.__class__ == Common:
            self.__classes = _get_scene_classes(module)

    @staticmethod
    def meta_construct(self: Scene):
        raise NotImplementedError()

    def construct(self):
        if self.__classes is None:
            self.meta_construct(self)
        else:
            for _, class_ins in self.__classes:
                self.clear()
                class_ins.meta_construct(self)
                self.wait()
