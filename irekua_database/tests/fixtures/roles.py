import pytest

from irekua_database.models import Role


@pytest.fixture
@pytest.mark.django_db
def role_factory():
    def create_role(
        name,
        description=None,
        icon=None,
        permissions=None,
    ):
        if description is None:
            description = f"Role {name}"

        if permissions is None:
            permissions = []

        role = Role.objects.create(
            name=name,
            description=description,
            icon=icon,
        )

        for permission in permissions:
            role.permissions.add(permission)

        return role

    return create_role


@pytest.fixture
@pytest.mark.django_db
def restrictive_role(role_factory):
    return role_factory("restrictive role")


@pytest.fixture
@pytest.mark.django_db
def role_A(role_factory):
    return role_factory("role_A")


@pytest.fixture
@pytest.mark.django_db
def role_B(role_factory):
    return role_factory("role_B")
