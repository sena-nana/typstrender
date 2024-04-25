from tempfile import NamedTemporaryFile
from typing import Unpack

import typst

from .base import _Render, _RequireKwargs


class TypstRender(_Render):
    def __init__(
        self,
        typst: str,
        is_file: bool = False,
        **kwargs: Unpack[_RequireKwargs],
    ) -> None:
        self.typst = typst
        self.is_file = is_file
        super().__init__(**kwargs)

    def render(self) -> bytes:
        if self.is_file:
            return typst.Compiler(self.typst, **self.kwargs).compile(format="png")  # type: ignore
        else:
            fake_file = NamedTemporaryFile()
            fake_file.write(self.typst.encode())
            return typst.Compiler(fake_file.name, **self.kwargs).compile(format="png")  # type: ignore


__all__ = ["TypstRender"]
