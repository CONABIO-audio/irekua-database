from django.contrib import admin

from irekua_terms import models
from .entailment_type import EntailmentTypeAdmin
from .entailment import EntailmentAdmin
from .term_type import TermTypeAdmin
from .term import TermAdmin


admin.site.register(models.TermType, TermTypeAdmin)
admin.site.register(models.EntailmentType, EntailmentTypeAdmin)
admin.site.register(models.Term, TermAdmin)
admin.site.register(models.Entailment, EntailmentAdmin)
