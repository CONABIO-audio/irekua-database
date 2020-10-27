from irekua_upload.base import IrekuaOperation
from irekua_devices.models import PhysicalDevice


class Operation(IrekuaOperation):
    def run(self, *args, **kwargs):
        num_items = Item.objects.count()
        print(f'Hay {num_items}')
