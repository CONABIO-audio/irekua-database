from django.db.models import Q
from dal import autocomplete

from irekua_items.models import MimeType
from irekua_items.models import MediaInfoType
from irekua_items.models import ItemType
from irekua_items.models import LicenceType
from irekua_items.models import Tag
from irekua_items.models import Item
from irekua_items.models import Licence
from irekua_database.autocomplete import register_autocomplete


urlpatterns = []


@register_autocomplete(MimeType, urlpatterns)
class MimeTypesAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = MimeType.objects.all()

        if self.q:
            qs = qs.filter(mime_type__istartswith=self.q)

        return qs


@register_autocomplete(MediaInfoType, urlpatterns)
class MediaInfoTypesAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = MediaInfoType.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


@register_autocomplete(ItemType, urlpatterns)
class ItemTypesAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = ItemType.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


@register_autocomplete(LicenceType, urlpatterns)
class LicenceTypesAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = LicenceType.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


@register_autocomplete(Tag, urlpatterns, create_field="name")
class TagsAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Tag.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs

    # pylint: disable=no-self-use
    def has_add_permission(self, request):
        return request.user.is_authenticated


@register_autocomplete(Item, urlpatterns)
class ItemAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Item.objects.all()

        if self.q:
            qs = qs.filter(
                Q(id__istartswith=self.q) | Q(item_type__name__istartswith=self.q)
            )

        return qs


@register_autocomplete(Licence, urlpatterns)
class LicenceAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Licence.objects.all()

        if self.q:
            qs = qs.filter(
                Q(created_by__username__istartswith=self.q)
                | Q(licence_type__name__istartswith=self.q)
            )

        return qs
