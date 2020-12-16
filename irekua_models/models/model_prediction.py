from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from irekua_annotations.models import Annotation


class ModelPrediction(Annotation):
    model_version = models.ForeignKey(
        "ModelVersion",
        on_delete=models.PROTECT,
        db_column="model_version_id",
        verbose_name=_("model version"),
        help_text=_("Model and version used for this prediction"),
        blank=False,
        null=False,
    )

    certainty = models.FloatField(
        db_column="certainty",
        verbose_name=_("certainty"),
        help_text=_("Model certainty of prediction. A number from 0 to 1."),
        blank=False,
        null=False,
    )

    model_run = models.ForeignKey(
        "ModelRun",
        on_delete=models.PROTECT,
        db_column="model_run_id",
        verbose_name=_("model run"),
        help_text=_("Model run in which this prediction was made"),
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _("Model Prediction")

        verbose_name_plural = _("Model Predictions")

        ordering = ["-modified_on"]

    def __str__(self):
        msg = _("Prediction of item %(item_id)s by model %(model)s")
        params = dict(item_id=self.item, model=self.model_version)
        return msg % params

    def clean(self):
        super().clean()

        # pylint: disable=no-member
        model = self.model_version.model

        # Check model can process items of this type
        self.clean_compatible_model_and_item_types(model)

        # Check model detects and classifies events of this type
        self.clean_compatible_model_and_event_types(model)

        # Check model outputs annotations of this type
        self.clean_compatible_model_and_annotation_types(model)

        # Check model run item is the same as with annotated item.
        self.clean_model_run()

    def clean_compatible_model_and_item_types(self, model):
        try:
            # pylint: disable=no-member
            model.validate_item_type(self.item.item_type)

        except ValidationError as error:
            raise ValidationError({"item": error}) from error

    # pylint: disable=no-self-use
    def clean_compatible_model_and_event_types(self, model):
        try:
            model.validate_event_type(self.event_type)

        except ValidationError as error:
            raise ValidationError({"event_type": error}) from error

    def clean_compatible_model_and_annotation_types(self, model):
        annotation_type = model.annotation_type

        if annotation_type != self.annotation_type:
            msg = _(
                "Annotation type of annotation and model do "
                "not coincide (%(self)s != %(annotation_type)s)"
            )
            params = dict(
                self=self.annotation_type,
                model=annotation_type,
            )
            raise ValidationError({"annotation_type": msg % params})

    def clean_model_run(self):
        if self.model_run is None:
            return

        if self.item == self.model_run.item:
            return

        msg = _(
            "The declared model run was made on an item different to "
            "the annotated item"
        )
        raise ValidationError({"model_run": msg})
