from tempfile import NamedTemporaryFile
from typing import Unpack, cast

import mistune
import typst
from mistune.renderers._list import (
    _render_list_item,
    _render_unordered_list,
    strip_end,
)
from mistune.renderers.markdown import MarkdownRenderer

from .base import _Render, _RequireKwargs


class _MarkdownToTypst(MarkdownRenderer):
    def heading(self, token, state) -> str:
        level = token["attrs"]["level"]
        marker = "=" * level
        text = self.render_children(token, state)
        return marker + " " + text + "\n\n"

    def strong(self, token, state) -> str:
        return "*" + self.render_children(token, state) + "*"

    def emphasis(self, token, state) -> str:
        return "_" + self.render_children(token, state) + "_"

    def link(self, token, state) -> str:
        label = token.get("label")
        text = self.render_children(token, state)
        out = "(" + text + ")"
        if label:
            return out + "(" + label + ")"

        attrs = token["attrs"]
        url = attrs["url"]
        title = attrs.get("title")

        out += "["
        if "(" in url or ")" in url:
            out += "<" + url + ">"
        else:
            out += url
        if title:
            out += ' "' + title + '"'
        return "#link" + out + "]"

    def list(self, token, state) -> str:
        attrs = token["attrs"]
        if attrs["ordered"]:
            children = _render_ordered_list(self, token, state)
        else:
            children = _render_unordered_list(self, token, state)

        text = "".join(children)
        parent = token.get("parent")
        if parent:
            if parent["tight"]:
                return text
            return text + "\n"
        return strip_end(text) + "\n"

    def text(self, token, state) -> str:
        text: str = token["raw"]
        if text.startswith("// "):
            text = "`" + text + "`"
        return text


def _render_ordered_list(renderer, token, state):
    for item in token["children"]:
        parent = {
            "leading": "+ ",
            "tight": token["tight"],
        }
        yield _render_list_item(renderer, parent, item, state)


_markdown_typst_render = mistune.Markdown(renderer=_MarkdownToTypst())


class MarkdownRender(_Render):
    def __init__(
        self,
        markdown: str,
        **kwargs: Unpack[_RequireKwargs],
    ) -> None:
        self.markdown = cast(str, _markdown_typst_render(markdown))
        super().__init__(**kwargs)

    def render(self) -> bytes:
        fake_file = NamedTemporaryFile()
        fake_file.write(self.markdown.encode())
        return typst.Compiler(fake_file.name, **self.kwargs).compile(format="png")  # type: ignore


__all__ = ["MarkdownRender"]
