import pytest

from irekua_database.models import User


@pytest.fixture
@pytest.mark.django_db
def user_factory():
    def create_user(
        username,
        email=None,
        password=None,
        first_name="",
        last_name="",
        institutions=None,
        is_superuser=False,
        is_curator=False,
        is_developer=False,
    ):
        if email is None:
            email = f"{username}@conabio.gob.mx"

        if password is None:
            password = username

        if institutions is None:
            institutions = []

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_superuser=is_superuser,
            is_developer=is_developer,
            is_curator=is_curator,
        )

        for institution in institutions:
            user.institutions.add(institution)

        return user

    return create_user


@pytest.fixture
@pytest.mark.django_db
def superuser(user_factory):
    return user_factory("superuser", is_superuser=True)


@pytest.fixture
@pytest.mark.django_db
def curator(user_factory):
    return user_factory("curator", is_curator=True)


@pytest.fixture
@pytest.mark.django_db
def developer(user_factory):
    return user_factory("developer", is_developer=True)


@pytest.fixture
@pytest.mark.django_db
def manager_A(user_factory):
    return user_factory("manager_A")


@pytest.fixture
@pytest.mark.django_db
def manager_B(user_factory):
    return user_factory("manager_B")


@pytest.fixture
@pytest.mark.django_db
def administrator_A(user_factory):
    return user_factory("administrator_A")


@pytest.fixture
@pytest.mark.django_db
def administrator_B(user_factory):
    return user_factory("administrator_B")


@pytest.fixture
@pytest.mark.django_db
def collection_user_A(user_factory):
    return user_factory("collection_user_A")


@pytest.fixture
@pytest.mark.django_db
def restricted_user_A(user_factory):
    return user_factory("restricted_user_A")


@pytest.fixture
@pytest.mark.django_db
def external_user_A(user_factory):
    return user_factory("foreign_user_A")


@pytest.fixture
@pytest.mark.django_db
def collection_user_B(user_factory):
    return user_factory("collection_user_B")


@pytest.fixture
@pytest.mark.django_db
def restricted_user_B(user_factory):
    return user_factory("restricted_user_B")


@pytest.fixture
@pytest.mark.django_db
def external_user_B(user_factory):
    return user_factory("foreign_user_B")
