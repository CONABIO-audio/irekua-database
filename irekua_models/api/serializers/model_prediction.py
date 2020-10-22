# -*- coding: utf-8 -*-
from rest_framework import serializers

from irekua_models import models


class ModelPredictionSerializer(serializers.ModelSerializer):
        class Meta:
            model = models.ModelPrediction
            fields = [
                'id',
                'item',
                'event_type',
                'annotation_type',
            ]
