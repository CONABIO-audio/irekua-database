# Generated by Django 3.1.2 on 2020-10-25 01:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def move_predictions_to_new_model(apps, schema_editor):
    ModelPredictionTmp = apps.get_model("irekua_models", "ModelPredictionTmp")
    ModelPrediction = apps.get_model("irekua_models", "ModelPrediction")
    Annotation = apps.get_model("irekua_annotations", "Annotation")

    pre_migration_annotations = Annotation.objects.count()
    predictions = ModelPrediction.objects.count()

    for prediction in ModelPrediction.objects.all():
        annotation_type = prediction.model_version.model.annotation_type
        new_prediction = ModelPredictionTmp(
            item=prediction.item,
            event_type=prediction.event_type,
            annotation_type=annotation_type,
            annotation=prediction.annotation,
            model_version=prediction.model_version,
            created_by=prediction.created_by,
            modified_by=prediction.modified_by,
            certainty=prediction.certainty,
        )

        new_prediction.save()

        for label in prediction.labels.all():
            new_prediction.labels.add(label)

        new_prediction.save()

    assert (
        ModelPrediction.objects.count() == ModelPredictionTmp.objects.count()
    )
    assert (
        Annotation.objects.count() == pre_migration_annotations + predictions
    )


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("irekua_annotations", "0003_annotation_userannotation"),
        ("irekua_items", "0010_relocate_annotation_models"),
        ("irekua_terms", "0006_auto_20201021_2015"),
        ("irekua_models", "0006_update_annotation_type_reference"),
    ]

    operations = [
        migrations.CreateModel(
            name="ModelPredictionTmp",
            fields=[
                (
                    "annotation_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="irekua_annotations.annotation",
                    ),
                ),
                (
                    "certainty",
                    models.FloatField(
                        db_column="certainty",
                        help_text="Model certainty of prediction. A number from 0 to 1.",
                        verbose_name="certainty",
                    ),
                ),
                (
                    "model_version",
                    models.ForeignKey(
                        db_column="model_version_id",
                        help_text="Model and version used for this prediction",
                        on_delete=django.db.models.deletion.PROTECT,
                        to="irekua_models.modelversion",
                        verbose_name="model version",
                    ),
                ),
            ],
            options={
                "verbose_name": "Model Prediction",
                "verbose_name_plural": "Model Predictions",
                "ordering": ["-modified_on"],
            },
            bases=("irekua_annotations.annotation",),
        ),
        migrations.RunPython(
            move_predictions_to_new_model,
        ),
    ]
