from irekua_annotations.models import UserAnnotation
from .annotations import Filter as AnnotationFilter
from .annotations import search_fields
from .annotations import ordering_fields


__all__ = [
    "search_fields",
    "ordering_fields",
    "Filter",
]


class Filter(AnnotationFilter):
    class Meta:
        model = UserAnnotation

        fields = {
            **AnnotationFilter.Meta.fields,
            "certainty": ["exact"],
            "quality": ["exact"],
        }
