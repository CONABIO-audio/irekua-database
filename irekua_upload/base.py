import sys
import contextlib
import traceback
from abc import ABC
from abc import abstractmethod
from io import StringIO

from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.exceptions import PermissionDenied


@contextlib.contextmanager
def capture():
    oldout, olderr = sys.stdout, sys.stderr

    try:
        out = [StringIO(), StringIO()]
        sys.stdout, sys.stderr = out
        yield out

    finally:
        sys.stdout, sys.stderr = oldout, olderr
        out[0] = out[0].getvalue()
        out[1] = out[1].getvalue()


class BaseForm(forms.Form):
    pass


class IrekuaOperation(ABC):
    form_class = BaseForm

    initial = {}

    prefix = None

    required_parameters = []

    @abstractmethod
    def run(self, request=None, form=None, **kwargs):
        pass

    @property
    @abstractmethod
    def name(self):
        pass

    # pylint: disable=no-self-use
    def has_run_permission(self, request):
        user = request.user
        return user.is_superuser

    def dispatch(self, request):
        # Check that the operation can be run by the requestor
        self.validate_permissions(request)

        # Check that all required query parameters were provided in the request
        self.validate_request_query(request)

        form = self.get_form(request=request)

        # Check that request body data is valid
        self.validate_form_data(form)

        # Consolidate all positional and keyword arguments for operation run
        kwargs = self.get_operation_kwargs(request, form)

        return self._run(request=request, form=form, **kwargs)

    def __str__(self):
        return self.name

    def get_initial(self):
        return self.initial.copy()

    def get_prefix(self):
        return self.prefix

    def get_form_class(self):
        return self.form_class

    def get_form(self, request, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()

        return form_class(**self.get_form_kwargs(request))

    def get_form_kwargs(self, request):
        kwargs = {
            'initial': self.get_initial(),
            'prefix': self.get_prefix(),
        }

        if request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': request.POST,
                'files': request.FILES,
            })

        return kwargs

    @staticmethod
    def get_operation_kwargs(request, form):
        return {
            **request.GET,
            **form.cleaned_data,
        }

    def validate_request_query(self, request):
        errors = {}

        for parameter in self.required_parameters:
            if not parameter in request.GET:
                msg = _('The parameter %(parameter)s is required')
                params = dict(parameter=parameter)
                errors[parameter] = msg % params

        if errors:
            raise ValidationError(errors)

    @staticmethod
    def validate_form_data(form):
        if not form.is_valid():
            raise ValidationError(form.errors.as_data())

    def validate_permissions(self, request):
        if not self.has_run_permission(request):
            msg = _(
                'You do not have permission to execute the operation'
                ' %(operation)s')
            params = dict(operation=self)
            raise PermissionDenied(msg % params)

    def _run(self, request=None, form=None, **kwargs):
        with capture() as (stdout, stderr):
            try:
                results = self.run(request=request, form=form, **kwargs)

            except Exception as error:
                traceback.print_exc()
                results = f'ERROR: {repr(error)}'

        return {
            'result': results,
            'stdout': stdout.getvalue(),
            'stderr': stderr.getvalue(),
        }
