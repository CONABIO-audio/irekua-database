from irekua_database.admin.base import IrekuaUserAdmin


class SiteAdmin(IrekuaUserAdmin):
    search_fields = [
        "name",
        "locality__name",
    ]

    list_display = [
        "id",
        "name",
        "geometry_type",
        "locality",
        "created_on",
    ]

    list_display_links = [
        "id",
        "name",
    ]

    list_filter = [
        "created_on",
    ]

    autocomplete_fields = [
        "locality",
    ]

    readonly_fields = [
        *IrekuaUserAdmin.readonly_fields,
        "geom",
    ]

    fieldsets = (
        (
            None,
            {"fields": (("name", "locality"),)},
        ),
        (
            None,
            {
                "fields": ("geom",),
            },
        ),
    )
