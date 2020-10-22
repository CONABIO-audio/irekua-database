# -*- coding: utf-8 -*-
from rest_framework import serializers

from irekua_models import models


class ModelSerializer(serializers.ModelSerializer):
        class Meta:
            model = models.Model
            fields = [
                'id',
                'name',
                'description',
                'repository',
                'annotation_type',
                'item_types',
                'event_types',
                'terms',
            ]
