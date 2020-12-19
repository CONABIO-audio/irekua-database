from django import forms
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save

from irekua_items.models import Item
from irekua_thumbnails.models import ThumbnailCreator
from irekua_thumbnails.models import ItemThumbnail


class ThumbnailForm(forms.ModelForm):
    class Meta:
        model = ItemThumbnail
        fields = (
            "item",
            "thumbnail",
        )


@receiver(post_save)
def create_thumbnail(sender, instance, **kwargs):
    if not issubclass(sender, Item):
        # Exit early if not an item
        return

    if kwargs.get("raw", False):
        # Do not execute when raw
        return

    try:
        getattr(instance, "itemthumbnail")
        #  If item thumbnail already exists do nothing
        return

    except ObjectDoesNotExist:
        pass

    item_type = instance.item_type

    try:
        creator = ThumbnailCreator.get_thumbnail_creator(item_type)

    except ObjectDoesNotExist:
        # Do not create thumbnail if no creator has been
        # registered
        return

    creator_function = creator.get_creator()
    thumbnail_file = creator_function(instance.item_file.file)

    form = ThumbnailForm(
        data={
            "item": instance,
        },
        files={
            "thumbnail": thumbnail_file,
        },
    )

    if form.is_valid():
        form.save()
