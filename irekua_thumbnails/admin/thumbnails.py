from irekua_database.admin.base import IrekuaAdmin


class ItemThumbnailAdmin(IrekuaAdmin):
    search_fields = [
        "item__id",
    ]

    list_display = [
        "item",
        "created_on",
    ]

    list_display_links = [
        "item",
    ]

    fieldsets = ((None, {"fields": (("item", "thumbnail"),)}),)
