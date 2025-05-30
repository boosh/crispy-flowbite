import os
from crispy_forms.utils import render_crispy_form
from django.test.html import Element, parse_html
from pathlib import Path

TEST_DIR = os.path.dirname(os.path.abspath(__file__))


def contains_partial(haystack, needle):
    """Search for a html element with at least the corresponding elements
    (other elements may be present in the matched element from the haystack)
    """
    if not isinstance(haystack, Element):
        haystack = parse_html(haystack)
    if not isinstance(needle, Element):
        needle = parse_html(needle)

    if needle.name == haystack.name and set(needle.attributes).issubset(
        haystack.attributes
    ):
        return True
    return any(
        contains_partial(child, needle)
        for child in haystack.children
        if isinstance(child, Element)
    )


def parse_expected(expected_file):
    test_file = Path(TEST_DIR) / "results" / expected_file
    with open(test_file) as f:
        return parse_html(f.read())


def parse_form(form):
    html = render_crispy_form(form)
    return parse_html(html)
