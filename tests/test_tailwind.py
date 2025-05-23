from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_forms.utils import render_crispy_form
from crispy_tailwind.tailwind import CSSContainer
from django.template import Context, Template

from .forms import CustomTextWidgetForm, SampleForm

individual_inputs = {"text": "text", "radioselect": "radio"}

base_standalone = {"base": "base"}

combined = {"base": "base", "text": "text", "radioselect": "radio"}


def test_individual_input():
    container = CSSContainer(individual_inputs)
    assert container.text == "text"
    assert container.radioselect == "radio"
    assert container.checkbox == ""


def test_base_input():
    container = CSSContainer(base_standalone)
    for item in container.__dict__.values():
        assert item == "base"


def test_base_and_individual():
    container = CSSContainer(combined)
    assert "base" in container.text
    assert "text" in container.text
    assert "base" in container.radioselect
    assert "radio" in container.radioselect


def test_add_remove_extra_class():
    container = CSSContainer(base_standalone)
    container += individual_inputs
    assert "text" in container.text
    container -= individual_inputs
    assert "text" not in container.text


def test_form():
    form_helper = FormHelper()
    form_helper.css_container = CSSContainer(base_standalone)
    form_helper.layout = Layout("first_name")

    template = Template(
        """
        {% load crispy_forms_tags %}
        {% crispy form form_helper %}
        """
    )

    context = Context({"form": SampleForm(), "form_helper": form_helper})
    html = template.render(context)
    assert "base" in html


def test_custom_widget():
    form = CustomTextWidgetForm()
    form.helper = FormHelper()
    html = render_crispy_form(form)
    assert (
        '<input type="text" name="first_name" class="customtextwidget " required id="id_first_name">'
        in html
    )
    assert (
        '<input type="text" name="last_name" class="custom-css customtextwidget " required id="id_last_name">'
        in html
    )
