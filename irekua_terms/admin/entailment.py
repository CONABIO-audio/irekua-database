from irekua_database.admin.base import IrekuaAdmin
from django.contrib import admin


class EntailmentAdmin(IrekuaAdmin):
    list_display = (
        "id",
        "source",
        "target",
        "created_on",
    )

    list_filter = [
        "source__term_type",
        "target__term_type",
    ]

    search_fields = [
        "source__value",
        "target__value",
    ]

    autocomplete_fields = [
        "source",
        "target",
    ]
