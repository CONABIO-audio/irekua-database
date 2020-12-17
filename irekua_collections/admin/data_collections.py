from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from irekua_database.admin.base import IrekuaUserAdmin
from irekua_collections.models import Collection


class UsersInline(admin.TabularInline):
    extra = 0

    model = Collection.users.through

    verbose_name = _("User")

    verbose_name_plural = _("Users")

    autocomplete_fields = ["user"]

    readonly_fields = [
        "created_by",
        "created_on",
    ]


class InstitutionsInline(admin.TabularInline):
    extra = 0

    model = Collection.institutions.through

    verbose_name = _("Institution")

    verbose_name_plural = _("Institutions")

    autocomplete_fields = ["institution"]


class AdministratorsInline(admin.TabularInline):
    extra = 0

    model = Collection.administrators.through

    verbose_name = _("Administrator")

    verbose_name_plural = _("Administrators")

    autocomplete_fields = ["user"]


class CollectionAdmin(IrekuaUserAdmin):
    search_fields = [
        "name",
        "collection_type__name",
        "institutions__institution_name",
    ]

    list_display = [
        "id",
        "__str__",
        "collection_type",
        "is_open",
        "created_by",
        "created_on",
    ]

    list_display_links = [
        "id",
        "__str__",
    ]

    list_filter = [
        "is_open",
        "institutions",
        "collection_type",
    ]

    autocomplete_fields = [
        "collection_type",
    ]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("name", "collection_type"),
                    "description",
                    ("logo", "is_open"),
                )
            },
        ),
        (
            _("Additional Metadata"),
            {
                "fields": ("metadata",),
            },
        ),
    )

    inlines = [
        AdministratorsInline,
        UsersInline,
        InstitutionsInline,
    ]

    def save_related(self, request, form, formsets, change):
        user = request.user
        user_formset = formsets[1]
        for user_form in user_formset:
            if user_form.instance.pk is None:
                user_form.instance.created_by = user

            if user_form.has_changed():
                user_form.instance.modified_by = user

        return super().save_related(request, form, formsets, change)
