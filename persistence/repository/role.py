from persistence.decorators import get_by_primary_key, scalar, scalars
from persistence.repository import AbstractRepository


class RoleRepository(AbstractRepository):
    @staticmethod
    def get_entity_cls():
        return Role

    @staticmethod
    @scalars
    def find_all():
        return (
            Role
            .select()
            .order_by(Role.name)
        )

    @classmethod
    @get_by_primary_key
    def find_by_id(cls, role_id):
        pass

    @staticmethod
    @scalar
    def find_by_name(name):
        return (
            Role
            .select()
            .where(Role.name == name)
        )

    @staticmethod
    def save(role):
        raise NotImplementedError()

    @classmethod
    def delete_by_id(cls, role_id):
        raise NotImplementedError()


from persistence.model.role import Role
