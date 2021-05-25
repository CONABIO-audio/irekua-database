# Generated by Django 3.1.2 on 2020-10-25 00:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import irekua_database.utils


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("irekua_visualizers", "0004_auto_20201024_1826"),
        ("irekua_annotators", "0004_update_annotation_type_reference"),
        ("irekua_items", "0010_relocate_annotation_models"),
        ("irekua_terms", "0006_auto_20201021_2015"),
        ("irekua_annotations", "0001_initial"),
    ]

    operations = [
        migrations.RenameModel(
            "Annotation",
            "AnnotationTmp",
        ),
        migrations.AlterField(
            model_name="annotationvote",
            name="annotation",
            field=models.ForeignKey(
                db_column="annotation_id",
                help_text="Reference to annotation being voted",
                on_delete=django.db.models.deletion.CASCADE,
                to="irekua_annotations.annotationtmp",
                verbose_name="annotation",
            ),
        ),
        migrations.AlterField(
            model_name="annotationtmp",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                db_column="creator_id",
                help_text="Creator of object",
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="annotationtmp_created_by",
                to=settings.AUTH_USER_MODEL,
                verbose_name="creator",
            ),
        ),
        migrations.AlterField(
            model_name="annotationtmp",
            name="modified_by",
            field=models.ForeignKey(
                blank=True,
                db_column="modified_by",
                editable=False,
                help_text="User who made modifications last",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="annotationtmp_modified_by",
                to=settings.AUTH_USER_MODEL,
                verbose_name="modified by",
            ),
        ),
    ]
