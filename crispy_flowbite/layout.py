from crispy_forms.bootstrap import (
    Accordion as BSAccordion,
    AccordionGroup as BSAccordionGroup,
    Alert as BSAlert,
    ContainerHolder,
)
from crispy_forms.layout import BaseInput, Field, LayoutObject
from crispy_forms.utils import render_field
from django.template.loader import render_to_string
from django.utils.safestring import SafeString
from django.utils.text import slugify
from random import randint


class ConditionalLayout(LayoutObject):
    """
    A layout object that renders its contents only if a condition (lambda) evaluates to True.
    Otherwise renders nothing.

    E.g.:

        ConditionalLayout(
            lambda: not self.is_campaign,
            "primary_keywords"
        ),
    """

    def __init__(self, condition, *fields):
        self.condition = condition
        self.fields = list(fields)

    def render(self, form, context, template_pack=None, **kwargs):
        """
        Renders this layout object
        """
        if callable(self.condition) and self.condition():
            html = ""
            for field in self.fields:
                html += render_field(
                    field, form, context, template_pack=template_pack, **kwargs
                )
            return html
        return ""


class Submit(BaseInput):
    """
    Used to create a Submit button descriptor for the {% crispy %} template tag::
        submit = Submit('Search the Site', 'search this site')
    .. note:: The first argument is also slugified and turned into the id for the submit button.

    This is a customised version for Flowbite to add Flowbite CSS style by default
    """

    input_type = "submit"

    def __init__(self, *args, css_class=None, **kwargs):
        if css_class is None:
            self.field_classes = "submit"
        else:
            self.field_classes = css_class
        super().__init__(*args, **kwargs)


class Reset(BaseInput):
    """
    Used to create a Reset button input descriptor for the {% crispy %} template tag::
        reset = Reset('Reset This Form', 'Revert Me!')
    .. note:: The first argument is also slugified and turned into the id for the reset.

    This is a customised version for Flowbite to add Flowbite CSS style by default
    """

    input_type = "reset"

    def __init__(self, *args, css_class=None, **kwargs):
        if css_class is None:
            self.field_classes = (
                "bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded"
            )
        else:
            self.field_classes = css_class
        super().__init__(*args, **kwargs)


class Button(BaseInput):
    """
    Used to create a button descriptor for the {% crispy %} template tag::
        submit = Button('Search the Site', 'search this site')
    .. note:: The first argument is also slugified and turned into the id for the submit button.

    This is a customised version for Flowbite to add Flowbite CSS style by default
    """

    input_type = "button"

    def __init__(self, *args, css_class=None, **kwargs):
        if css_class is None:
            self.field_classes = "button"
        else:
            self.field_classes = css_class
        super().__init__(*args, **kwargs)


class Alert(BSAlert):
    css_class = ""


class Toggle(Field):
    template = "%s/layout/toggle.html"


class Accordion(BSAccordion):
    """
    Flowbite Accordion menu object. It wraps `AccordionGroup` objects in a
    container. It also allows the usage of always-open::

        Accordion(
            AccordionGroup("group name", "form_field_1", "form_field_2"),
            AccordionGroup("another group name", "form_field"),
            always_open=True
        )
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.always_open = kwargs.pop("always_open", False)


class AccordionGroup(BSAccordionGroup):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.help_text = kwargs.pop("help_text", "")
        # highlighted call-to-action text
        self.cta = kwargs.pop("cta", "")
        self.initially_open = kwargs.pop("initially_open", False)


class AccordionSingleInput(BSAccordion):
    """
    Customised Accordion where each item is intended to just wrap a single input to avoid overwhelming users with input boxes. But note, this container can contain multiple such items::

        AccordionSingleInput(
            AccordionSingleInputGroup(
                "Email",
                "email_address",
                help_text="Your email address",
            ),
            AccordionSingleInputGroup(
                "Password",
                "password",
                help_text="Your password",
            ),
        ),

    Note: help_text is hidden when expanded - make sure to also show
    in the input (e.g. under it or as placeholder text)
    """

    template = "%s/accordion-single-input.html"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.always_open = kwargs.pop("always_open", True)


class AccordionSingleInputGroup(BSAccordionGroup):
    """
    Customised Accordion intended to just wrap a single input to avoid overwhelming users with input boxes::

        AccordionSingleInput(
            AccordionSingleInputGroup(
                "Email",
                "email_address",
                help_text="Your email address",
            ),
            AccordionSingleInputGroup(
                "Password",
                "password",
                help_text="Your password",
            ),
        ),
    """

    template = "%s/accordion-single-input-group.html"

    def __init__(self, *args, **kwargs):
        """
        :param kwargs:
          - help_text: Help text to display next to the header when the accordion is closed
          - help_text_open: Help text to display next to the header when the accordion is open
        """
        super().__init__(*args, **kwargs)
        self.help_text = kwargs.pop("help_text", "")
        self.help_text_open = kwargs.pop("help_text_open", "")
        self.initially_open = kwargs.pop("initially_open", False)
        self.required = kwargs.pop("required", False)


class Tabs(ContainerHolder):
    """
    Flowbite Tabs layout object. Wraps ``TabGroup`` objects in a tabbed
    container using Flowbite's ``data-tabs-toggle``::

        Tabs(
            TabGroup("Profile", "first_name", "last_name"),
            TabGroup("Settings", "email", active=True),
        )
    """

    template = "%s/tabs.html"

    def __init__(
        self, *tab_groups, css_id=None, css_class=None, template=None, **kwargs
    ):
        super().__init__(
            *tab_groups, css_id=css_id, css_class=css_class, template=template, **kwargs
        )
        if not self.css_id:
            self.css_id = f"tabs-{randint(1000, 9999)}"

        # Auto-assign css_id to groups that don't have one
        for group in tab_groups:
            if not getattr(group, "css_id", None):
                group.css_id = f"{self.css_id}-{slugify(group.name)}"

        # If no group is explicitly active, activate the first one
        if not any(getattr(g, "active", False) for g in tab_groups):
            if tab_groups:
                tab_groups[0].active = True

        self.groups = list(tab_groups)

    def render(self, form, context, template_pack=None, **kwargs):
        content = SafeString("")
        for group in self.fields:
            content += render_field(
                group, form, context, template_pack=template_pack, **kwargs
            )

        template = self.get_template_name(template_pack)
        context.update({"tabs": self, "content": content})
        return render_to_string(template, context.flatten())


class TabGroup(BSAccordionGroup):
    """
    A single tab pane within a ``Tabs`` container::

        TabGroup("Tab title", "form_field_1", "form_field_2", active=True)
    """

    template = "%s/tab-group.html"

    def __init__(self, *args, **kwargs):
        self.active = kwargs.pop("active", False)
        super().__init__(*args, **kwargs)
