from django.urls import path
from irekua_thumbnails.views import generate_thumbnail


urlpatterns = [
    path("thumbnails/", generate_thumbnail, name="thumbnails"),
]
