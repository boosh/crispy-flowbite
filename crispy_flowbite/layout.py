from crispy_forms.bootstrap import (
    Accordion as BSAccordion,
    AccordionGroup as BSAccordionGroup,
    Alert as BSAlert,
)
from crispy_forms.layout import BaseInput, Field


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
        super().__init__(*args, **kwargs)
        self.help_text = kwargs.pop("help_text", "")
        self.initially_open = kwargs.pop("initially_open", False)
