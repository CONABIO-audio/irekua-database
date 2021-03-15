# Generated by Django 3.1.2 on 2020-10-25 01:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("irekua_terms", "0006_auto_20201021_2015"),
        ("irekua_items", "0010_relocate_annotation_models"),
        ("irekua_annotations", "0002_move_annotation_to_temporal_model"),
    ]

    operations = [
        migrations.CreateModel(
            name="Annotation",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_on",
                    models.DateTimeField(
                        auto_now_add=True,
                        db_column="created_on",
                        help_text="Date of creation",
                        verbose_name="created on",
                    ),
                ),
                (
                    "modified_on",
                    models.DateTimeField(
                        auto_now=True,
                        db_column="modified_on",
                        help_text="Date of last modification",
                        verbose_name="modified on",
                    ),
                ),
                (
                    "annotation",
                    models.JSONField(
                        blank=True,
                        db_column="annotation",
                        help_text="Information of annotation location within item",
                        verbose_name="annotation",
                    ),
                ),
                (
                    "annotation_metadata",
                    models.JSONField(
                        blank=True,
                        db_column="annotation_metadata",
                        help_text="Additional annotation metadata",
                        null=True,
                        verbose_name="annotation metadata",
                    ),
                ),
                (
                    "event_metadata",
                    models.JSONField(
                        blank=True,
                        db_column="event_metadata",
                        help_text="Additional metadata on event occurence",
                        null=True,
                        verbose_name="event metadata",
                    ),
                ),
                (
                    "annotation_type",
                    models.ForeignKey(
                        db_column="annotation_type_id",
                        help_text="Type of annotation",
                        on_delete=django.db.models.deletion.PROTECT,
                        to="irekua_annotations.annotationtype",
                        verbose_name="annotation type",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        db_column="creator_id",
                        help_text="Creator of object",
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="annotation_created_by",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="creator",
                    ),
                ),
                (
                    "event_type",
                    models.ForeignKey(
                        db_column="event_type_id",
                        help_text="Type of event being annotated",
                        on_delete=django.db.models.deletion.PROTECT,
                        to="irekua_annotations.eventtype",
                        verbose_name="event type",
                    ),
                ),
                (
                    "item",
                    models.ForeignKey(
                        db_column="item_id",
                        help_text="Annotated item",
                        on_delete=django.db.models.deletion.PROTECT,
                        to="irekua_items.item",
                        verbose_name="item",
                    ),
                ),
                (
                    "labels",
                    models.ManyToManyField(
                        blank=True,
                        db_column="labels",
                        help_text="Labels associated with annotation",
                        to="irekua_terms.Term",
                        verbose_name="labels",
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        blank=True,
                        db_column="modified_by",
                        editable=False,
                        help_text="User who made modifications last",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="annotation_modified_by",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="modified by",
                    ),
                ),
            ],
            options={
                "verbose_name": "Annotation",
                "verbose_name_plural": "Annotations",
                "ordering": ["-modified_on"],
                "permissions": (("vote", "Can vote annotation"),),
            },
        ),
        migrations.CreateModel(
            name="UserAnnotation",
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
                    models.CharField(
                        blank=True,
                        choices=[
                            ("L", "uncertain"),
                            ("M", "somewhat certain"),
                            ("H", "certain"),
                        ],
                        db_column="certainty",
                        help_text="Level of certainty of location or labelling of annotation",
                        max_length=16,
                        null=True,
                        verbose_name="certainty",
                    ),
                ),
                (
                    "quality",
                    models.CharField(
                        blank=True,
                        choices=[("L", "low"), ("M", "medium"), ("H", "high")],
                        db_column="quality",
                        help_text="Quality of item content inside annotation",
                        max_length=16,
                        verbose_name="quality",
                    ),
                ),
                (
                    "commentaries",
                    models.TextField(
                        blank=True,
                        db_column="commentaries",
                        help_text="Commentaries of annotator",
                        verbose_name="commentaries",
                    ),
                ),
            ],
            options={
                "verbose_name": "User Annotation",
                "verbose_name_plural": "User Annotations",
                "ordering": ["-created_on"],
            },
            bases=("irekua_annotations.annotation",),
        ),
    ]
