from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class IrekuaAdmin(admin.ModelAdmin):
    """
    Base ModelAdmin class for Irekua Models.

    All models in Irekua, except the User model, should
    inherit from irekua_database.models.IrekuaModelBase.

    When this occurs the model has two fields default
    fields concerning its date of creation and modification.
    This admin model automatically includes a section displaying
    these fields.
    """

    date_hierarchy = 'created_on'

    list_per_page = 50

    actions_on_top = True

    readonly_fields = [
        'created_on',
        'modified_on'
    ]

    def get_fieldsets(self, request, obj=None):
        fieldsets = list(super().get_fieldsets(request, obj=obj))
        fieldsets.append(
            (_('Creation'), {
                'fields': (
                    ('created_on', 'modified_on',),
                ),
            })
        )
        return tuple(fieldsets)


class IrekuaUserAdmin(IrekuaAdmin):
    """
    Base ModelAdmin class for Irekua User Models.

    Whenever it is important to store information of the
    user that created or modified a database object, the model
    should inherit from irekua_database.models.IrekuaModelBaseUser.

    Apart from the two default fields of date of creation and
    modification, models that inherit from IrekuaModelBaseUser
    have two fields acknowledging the user that created or
    modified the object.

    This admin model includes this information automatically
    in the Creation section of the admin detail.

    Additionally, this admin model will register information on the author
    of the changes on the object.
    """

    readonly_fields = [
        'created_on',
        'modified_on',
        'created_by',
        'modified_by',
    ]

def get_fieldsets(self, request, obj=None):
    fieldsets = list(super().get_fieldsets(request, obj=obj))
    fieldsets.append(
        (_('Creation'), {
            'fields': (
                ('created_on', 'created_by',),
                ('modified_on', 'modified_by',),
            ),
        })
    )
    return tuple(fieldsets)

    def save_model(self, request, obj, form, change):
        obj.modified_by = request.user

        if not change:
            obj.created_by = request.user

        return super().save_model(request, obj, form, change)
