def can_view(item, user):
    if not user.is_authenticated:
        return False

    if user.is_special:
        return True

    # pylint: disable=no-member
    if not item.licence.is_active:
        return True

    # pylint: disable=no-member
    if item.licence.licence_type.can_view:
        return True

    if item.created_by == user:
        return True

    if item.collection.collection_type.is_admin(user):
        return True

    if item.collection.is_admin(user):
        return True

    role = item.collection.get_user_role(user)

    if role is None:
        return False

    return role.has_permission("view_collectionitem")


def can_change(item, user):
    if not user.is_authenticated:
        return False

    if user.is_superuser or user.is_curator:
        return True

    if item.created_by == user:
        return True

    if item.collection.collection_type.is_admin(user):
        return True

    if item.collection.is_admin(user):
        return True

    role = item.collection.get_user_role(user)

    if role is None:
        return False

    return role.has_permission("change_collectionitem")


def can_delete(item, user):
    if not user.is_authenticated:
        return False

    if user.is_superuser:
        return True

    if item.created_by == user:
        return True

    if item.collection.collection_type.is_admin(user):
        return True

    if item.collection.is_admin(user):
        return True

    role = item.collection.get_user_role(user)

    if role is None:
        return False

    return role.has_permission("delete_collectionitem")
