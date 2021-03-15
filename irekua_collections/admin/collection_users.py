from django.utils.translation import gettext_lazy as _

from irekua_database.admin.base import IrekuaUserAdmin


class CollectionUserAdmin(IrekuaUserAdmin):
    search_fields = [
        "user__username",
        "user__first_name",
        "user__last_name",
        "user__userinstitution__institution_name",
        "collection__name",
        "collection__collection_type__name",
    ]

    list_display = [
        "id",
        "__str__",
        "user",
        "collection",
        "role",
        "created_by",
        "created_on",
    ]

    list_display_links = [
        "id",
        "__str__",
    ]

    autocomplete_fields = [
        "user",
        "collection",
        "role",
    ]

    fieldsets = (
        (None, {"fields": (("collection", "user"), "role")}),
        (_("Additional metadata"), {"fields": ("collection_metadata",)}),
    )
