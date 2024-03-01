from persistence.decorators import (get_by_primary_key, scalar, scalars,
                                    update_authoring, insert_or_update, delete_by_primary_key)
from persistence.repository import AbstractRepository


class CategoryRepository(AbstractRepository):
    @staticmethod
    def get_entity_cls():
        return Category

    @staticmethod
    @scalars
    def find_all():
        return (
            Category
            .select()
            .order_by(Category.name)
        )

    @classmethod
    @get_by_primary_key
    def find_by_id(cls, category_id):
        pass

    @staticmethod
    @scalars
    def find_all_by_name_like(name):
        return (
            Category
            .select()
            .where(Category.name.like(f'%{name}%'))
            .order_by(Category.name)
        )

    @staticmethod
    @update_authoring
    @insert_or_update
    def save(category):
        pass

    @classmethod
    @delete_by_primary_key
    def delete_by_id(cls, category_id):
        pass


from persistence.model.category import Category
