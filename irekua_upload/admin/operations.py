from django import forms
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.translation import gettext_lazy as _

from irekua_database.admin.base import IrekuaAdmin
from irekua_upload.models import Operation
from irekua_upload.fields import OperationCodeField


class OperationForm(forms.ModelForm):
    code = OperationCodeField()

    class Meta:
        model = Operation
        fields = [
            "name",
            "python_file",
            "description",
        ]

    def get_initial_for_field(self, field, field_name):
        initial = super().get_initial_for_field(field, field_name)

        if field_name != "code":
            return initial

        try:
            return self.instance.python_file.read().decode("utf-8")

        except Exception:
            return None

    def clean(self):
        super().clean()

        if "code" not in self.cleaned_data:
            return

        try:
            self.instance.python_file.delete()

        except ValueError:
            pass

        content_file = ContentFile(self.cleaned_data["code"].encode("utf-8"))
        name = self.cleaned_data["name"] + ".py"
        uploaded_file = InMemoryUploadedFile(
            file=content_file,
            name=name,
            size=content_file.size,
            charset="utf-8",
            content_type="text/x-python-script",
            field_name="python_file",
        )
        self.cleaned_data["python_file"] = uploaded_file


class OperationAdmin(IrekuaAdmin):
    search_fields = ["name"]

    list_display = [
        "id",
        "__str__",
        "created_on",
    ]

    list_display_links = [
        "id",
        "__str__",
    ]

    form = OperationForm

    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("name", "python_file"),
                    "description",
                )
            },
        ),
        (_("Code"), {"fields": ("code",)}),
    )
