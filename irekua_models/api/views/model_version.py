# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework import viewsets

from irekua_models import models
from irekua_models.api import serializers


class ModelVersionViewSet(
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        mixins.UpdateModelMixin,
        mixins.RetrieveModelMixin,
        mixins.DestroyModelMixin,
        viewsets.GenericViewSet):
    # pylint: disable=no-member
    queryset = models.ModelVersion.objects.all()

    serializer_class = serializers.ModelVersionSerializer
