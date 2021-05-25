from django import forms

from irekua_upload.models import Operation
from irekua_upload.widgets import AceCodeWidget


class OperationCodeField(forms.CharField):
    def __init__(self, *args, **kwargs):
        kwargs["widget"] = AceCodeWidget
        super().__init__(*args, **kwargs)

    def clean(self, value):
        value = super().clean(value)

        compiled_code = Operation.validate_syntax(value)
        Operation.validate_content(compiled_code)

        return value
