# Generated by Django 3.1.2 on 2020-10-25 01:18

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("irekua_annotations", "0003_annotation_userannotation"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("irekua_models", "0007_create_temporary_model_prediction_model"),
    ]

    operations = [
        migrations.DeleteModel(
            "ModelPrediction",
        ),
        migrations.RenameModel("ModelPredictionTmp", "ModelPrediction"),
    ]
