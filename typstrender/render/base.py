import abc
from io import BytesIO
from pathlib import Path
from typing import NotRequired, TypedDict, Unpack


class _RequireKwargs(TypedDict):
    input: NotRequired[Path]
    root: NotRequired[Path | None]
    font_paths: NotRequired[list[Path]]
    sys_inputs: NotRequired[dict[str, str]]


class _Render(abc.ABC):
    def __init__(self, **kwargs: Unpack[_RequireKwargs]) -> None:
        self.kwargs = kwargs

    def render(self) -> bytes: ...
    def render_bytesIO(self) -> BytesIO:
        fake_file = BytesIO()
        fake_file.write(self.render())
        return fake_file


__all__ = ["_RequireKwargs", "_Render"]
