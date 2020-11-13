from django.conf.urls import url, include


urlpatterns = [
    url("", include("irekua_database.autocomplete")),
]
