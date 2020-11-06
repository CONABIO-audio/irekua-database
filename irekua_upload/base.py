from abc import ABC
from abc import abstractmethod


class IrekuaOperation(ABC):
    @abstractmethod
    def run(self, *args, **kwargs):
        pass

    def has_run_permission(self, request):
        user = request.user
        return user.is_superuser
