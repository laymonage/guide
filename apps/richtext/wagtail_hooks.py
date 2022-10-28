from html import escape

from django.utils.text import slugify
from draftjs_exporter.dom import DOM
from draftjs_exporter.engines.string import DOMString, Elt
from wagtail import hooks
from wagtail.admin.rich_text.converters.html_to_contentstate import BlockElementHandler


class DOMText(DOMString):
    """Like DOMString, but the element is rendered without any tags (text-only)."""

    @staticmethod
    def render_children(children):
        return "".join(
            DOMText.render(c) if isinstance(c, Elt) else escape(c) for c in children
        )

    @staticmethod
    def render(elt):
        return DOMText.render_children(elt.children) if elt.children else ""


class AnchorBlockConverter:
    """
    AnchorBlockConverter, Draft.js ContentState to database HTML.
    Adds `id="SLUG"` attr.
    """

    def __init__(self, tag):
        self.tag = tag

    def __call__(self, props):
        id = text = props["children"]
        if isinstance(text, Elt):
            id = DOMText.render(text)
        return DOM.create_element(self.tag, {"id": slugify(id)}, text)


@hooks.register("register_rich_text_features")
def register_rich_heading_anchor_feature(features):
    for elm, handler in [
        ("h1", "header-one"),
        ("h2", "header-two"),
        ("h3", "header-three"),
        ("h4", "header-four"),
        ("h5", "header-five"),
        ("h6", "header-six"),
    ]:
        features.register_converter_rule(
            "contentstate",
            elm,
            {
                "from_database_format": {elm: BlockElementHandler(handler)},
                "to_database_format": {
                    "block_map": {handler: AnchorBlockConverter(elm)}
                },
            },
        )
