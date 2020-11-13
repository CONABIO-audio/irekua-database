import re
from django.db.models import Q
from django.urls import path

from dal import autocomplete

from irekua_database.models import User
from irekua_database.models import Institution
from .widgets import SelectMultiple
from .widgets import Select


model_store = {}


def get_name_from_model(model):
    return re.sub(r"(?<!^)(?=[A-Z])", "_", model.__name__).lower() + "s"


def get_viewname_from_model(model):
    return f"{get_name_from_model(model)}_autocomplete"


def register_autocomplete(model, urlpatterns, view_name=None, create_field=None):
    """
    Register an autocomplete view in the urlpatterns.

    This decorator helps avoid the boilerplate code of adding a view to the
    urlpatterns list. It will bind the model autocomplete view to the url
    %(modelname)s/ with the view name %(modelname)s_autocomplete.
    """
    if view_name is None:
        view_name = get_viewname_from_model(model)

    model_store[model] = view_name

    def wrapper(ViewClass):
        urlpatterns.append(
            path(
                f"{get_name_from_model(model)}/",
                ViewClass.as_view(create_field=create_field),
                name=view_name,
            )
        )

        return ViewClass

    return wrapper


def get_autocomplete_widget(
    model=None, view_name=None, multiple=False, attrs=None, query=None
):
    """
    Get a custom widget to render a select2 autocomplete form.

    This form will allow the user to dynamically search and select an
    option from a model table or a custom autocomplete view.
    """
    if view_name is None:
        view_name = model_store.get(model, get_viewname_from_model(model))

    if attrs is None:
        attrs = {
            "data-theme": "bootstrap",
        }

    if multiple:
        return SelectMultiple(url=view_name, query=query, attrs=attrs)

    return Select(url=view_name, query=query, attrs=attrs)


urlpatterns = []


@register_autocomplete(User, urlpatterns)
class UsersAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = User.objects.all()

        if self.q:
            qs = qs.filter(
                Q(username__istartswith=self.q)
                | Q(first_name__istartswith=self.q)
                | Q(last_name__istartswith=self.q)
            )

        return qs


@register_autocomplete(Institution, urlpatterns)
class InstitutionAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Institution.objects.all()

        if self.q:
            qs = qs.filter(
                Q(institution_name__istartswith=self.q)
                | Q(institution_code__istartswith=self.q)
            )

        return qs
