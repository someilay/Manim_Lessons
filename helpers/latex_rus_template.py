from typing import Optional
from manim import TexTemplate, TexTemplateLibrary


_RUS_PREAMBLE = r"""
\usepackage[T2A, T1]{fontenc}
\usepackage[english, russian]{babel}
\usepackage[utf8]{inputenc}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{dsfont}
\usepackage{setspace}
\usepackage{tipa}
\usepackage{relsize}
\usepackage{textcomp}
\usepackage{mathrsfs}
\usepackage{calligra}
\usepackage{wasysym}
\usepackage{ragged2e}
\usepackage{xcolor}
\usepackage{microtype}
\usepackage{graphicx}
\DisableLigatures{encoding = *, family = * }
\linespread{1}

\newcommand*{\divby}{\mathrel{\rotatebox{90}{$\hskip-1pt.{}.{}.$}}}%
"""

RUS_TEMPLATE = TexTemplate(preamble=_RUS_PREAMBLE)


def rus_template(width: Optional[int] = None):
    if width is None:
        return RUS_TEMPLATE
    return TexTemplate(
        documentclass=fr'\documentclass[preview, varwidth={width}px]{{standalone}}',
        preamble=_RUS_PREAMBLE
    )


if __name__ == '__main__':
    pass
