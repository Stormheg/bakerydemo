from wagtail import hooks
from wagtail.admin.userbar import AccessibilityItem
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup

from bakerydemo.base.models import FooterText, Person

"""
N.B. To see what icons are available for use in Wagtail menus and StreamField block types,
enable the styleguide in settings:

INSTALLED_APPS = (
   ...
   'wagtail.contrib.styleguide',
   ...
)

or see https://thegrouchy.dev/general/2015/12/06/wagtail-streamfield-icons.html

This demo project also includes the wagtail-font-awesome-svg package, allowing further icons to be
installed as detailed here: https://github.com/allcaps/wagtail-font-awesome-svg#usage
"""


@hooks.register("register_icons")
def register_icons(icons):
    return icons + [
        "wagtailfontawesomesvg/solid/suitcase.svg",
        "wagtailfontawesomesvg/solid/utensils.svg",
    ]


class CustomAccessibilityItem(AccessibilityItem):
    axe_run_only = None


@hooks.register("construct_wagtail_userbar")
def replace_userbar_accessibility_item(request, items):
    items[:] = [
        CustomAccessibilityItem() if isinstance(item, AccessibilityItem) else item
        for item in items
    ]


class PersonViewSet(SnippetViewSet):
    # Instead of decorating the Person model class definition in models.py with
    # @register_snippet - which has Wagtail automatically generate an admin interface for this model - we can also provide our own
    # SnippetViewSet class which allows us to customize the admin interface for this snippet.
    # See the documentation for SnippetViewSet for more details
    # https://docs.wagtail.org/en/stable/reference/viewsets.html#snippetviewset
    model = Person
    menu_label = "People"  # ditch this to use verbose_name_plural from model
    icon = "group"  # change as required
    list_display = ("first_name", "last_name", "job_title", "thumb_image")
    list_filter = {
        "job_title": ["icontains"],
    }


class FooterTextViewSet(SnippetViewSet):
    model = FooterText
    search_fields = ("body",)


class BakerySnippetViewSetGroup(SnippetViewSetGroup):
    menu_label = "Bakery Misc"
    menu_icon = "utensils"  # change as required
    menu_order = 300  # will put in 4th place (000 being 1st, 100 2nd)
    items = (PersonViewSet, FooterTextViewSet)


# When using a SnippetViewSetGroup class to group several SnippetViewSet classes together,
# you only need to register the SnippetViewSetGroup class with Wagtail:
register_snippet(BakerySnippetViewSetGroup)

from wagtail import hooks
from wagtail_ab_testing.events import BaseEvent


class CustomEvent(BaseEvent):
    name = "Custom event"
    requires_page = False  # Set to False to create a "Global" event type that could be reached on any page

    # def get_page_types(self):
    #     return [
    #         # Return a list of page models that can be used as destination pages for this event type
    #         # For example, if this 'event type' is for a 'call to action' button that only appears on
    #         # the homepage, put your `HomePage` model here.
    #     ]


@hooks.register('register_ab_testing_event_types')
def register_ab_test_event_types():
    return {
        'custom-event-type': CustomEvent,
    }
