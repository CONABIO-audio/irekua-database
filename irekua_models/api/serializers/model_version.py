# -*- coding: utf-8 -*-
from rest_framework import serializers

from irekua_models import models


class ModelVersionSerializer(serializers.ModelSerializer):
        class Meta:
            model = models.ModelVersion
            fields = [
                'id',
                'model',
                'version',
            ]
