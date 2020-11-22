from django.db.models import Q
from dal import autocomplete

from irekua_devices.models import DeviceType
from irekua_devices.models import DeviceBrand
from irekua_devices.models import Device
from irekua_database.autocomplete import register_autocomplete


urlpatterns = []


@register_autocomplete(DeviceType, urlpatterns)
class DeviceTypesAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = DeviceType.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


@register_autocomplete(DeviceBrand, urlpatterns, create_field="name")
class DeviceBrandAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = DeviceBrand.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs

    def has_add_permission(self, request):
        return request.user.is_authenticated


@register_autocomplete(Device, urlpatterns)
class DeviceAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Device.objects.all()

        if self.q:
            qs = qs.filter(
                Q(model__istartswith=self.q) | Q(brand__name__istartswith=self.q)
            )

        if "device_type" in self.request.GET:
            qs = qs.filter(device_type=self.request.GET["device_type"])

        return qs
