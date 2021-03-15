from irekua_database.admin.base import IrekuaUserAdmin


class InstitutionAdmin(IrekuaUserAdmin):
    search_fields = [
        "institution_name",
    ]

    list_display = [
        "id",
        "institution_name",
        "institution_code",
        "created_on",
    ]

    list_display_links = ["id", "institution_name", "institution_code"]
