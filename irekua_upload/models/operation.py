import os
import importlib.util

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


from irekua_database.base import IrekuaModelBase
from irekua_upload.base import IrekuaOperation



class Operation(IrekuaModelBase):
    name = models.CharField(
        max_length=64,
        unique=True,
        db_column='name',
        verbose_name=_('name'),
        help_text=_('Name of operation'))

    description = models.TextField(
        db_column='description',
        verbose_name=_('description'),
        help_text=_('Description of operation'),
        blank=False)

    python_file = models.FileField(
        upload_to='operations/',
        db_column='python_file',
        verbose_name=_('python file'),
        help_text=_('Python file containing the operation'),
        blank=True,
        null=True)

    class Meta:
        verbose_name = _('Operation')

        verbose_name_plural = _('Operations')

        ordering = ['-created_on']

    def get_operation_class(self):
        name = self.python_file.name
        basename = os.path.basename(name)
        module_name = os.path.splitext(basename)[0]

        spec = importlib.util.spec_from_file_location(
            module_name,
            self.python_file.path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        return module.Operation

    def get_operation_instance_kwargs(self):
        return {}

    def get_operation(self):
        operation_class = self.get_operation_class()
        kwargs = self.get_operation_instance_kwargs()
        return operation_class(**kwargs)

    def run(self, *args, **kwargs):
        operation = self.get_operation()
        return operation.run(*args, **kwargs)
