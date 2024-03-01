from persistence.decorators import (get_by_primary_key, scalar, scalars,
                                    update_authoring, insert_or_update, delete_by_primary_key)
from persistence.repository import AbstractRepository


class UserRepository(AbstractRepository):
    @staticmethod
    def get_entity_cls():
        return User

    @staticmethod
    @scalars
    def find_all():
        return (
            User
            .select()
            .join(Role)
            .order_by(Role.name, User.username)
        )

    @classmethod
    @get_by_primary_key
    def find_by_id(cls, user_id):
        pass

    @staticmethod
    @scalars
    def find_all_by_role_id(role_id):
        return (
            User
            .select()
            .where(User.role_id == role_id)
            .order_by(User.username, User)
        )

    @staticmethod
    @scalar
    def find_by_username(username):
        return (
            User
            .select()
            .where(User.username == username)
        )

    @staticmethod
    @scalars
    def find_all_by_username_like(username):
        return (
            User
            .select()
            .join(Role)
            .where(User.username.like(f'%{username}%'))
            .order_by(Role.name, User.username)
        )

    @staticmethod
    @update_authoring
    @insert_or_update
    def save(user):
        pass

    @classmethod
    @delete_by_primary_key
    def delete_by_id(cls, user_id):
        pass


from persistence.model.role import Role
from persistence.model.user import User
