from django import forms


class AceCodeWidget(forms.Textarea):
    template_name = "irekua_upload/ace_code_widget.html"

    class Media:
        js = ("vendor/src-min-noconflict/ace.js",)
        css = {"all": ("vendor/src-min-noconflict/ace.css",)}
