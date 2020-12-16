from django import forms
from django.utils.http import urlencode
from dal import autocomplete as dal


class CustomURLMixin:
    def __init__(self, query=None, *args, **kwargs):
        self.query = query
        super().__init__(*args, **kwargs)

    @property
    def media(self):
        m = super().media
        return forms.Media(
            js=(
                "admin/js/vendor/jquery/jquery.min.js",
                *m._js,
            ),
            css={
                "screen": [
                    *m._css["screen"],
                    "irekua_database/css/vendor/select2-bootstrap.min.css",
                ],
            },
        )

    def _get_url(self):
        url = super()._get_url()

        if not self.query:
            return url

        return f"{url}?{urlencode(self.query)}"

    def _set_url(self, url):
        self._url = url

    url = property(_get_url, _set_url)


class SelectMultiple(CustomURLMixin, dal.ModelSelect2Multiple):
    pass


class Select(CustomURLMixin, dal.ModelSelect2):
    pass
