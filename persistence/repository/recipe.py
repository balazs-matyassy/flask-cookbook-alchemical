from persistence.decorators import (get_by_primary_key, scalar, scalars,
                                    update_ownership, update_authoring, insert_or_update, delete_by_primary_key)
from persistence.repository import AbstractRepository


class RecipeRepository(AbstractRepository):
    @staticmethod
    def get_entity_cls():
        return Recipe

    @staticmethod
    @scalars
    def find_all():
        return (
            Recipe
            .select()
            .join(Category)
            .order_by(Category.name, Recipe.name)
        )

    @classmethod
    @get_by_primary_key
    def find_by_id(cls, recipe_id):
        pass

    @staticmethod
    @scalars
    def find_all_by_category_id(category_id):
        return (
            Recipe
            .select()
            .where(Recipe.category_id == category_id)
            .order_by(Recipe.name)
        )

    @staticmethod
    @scalars
    def find_all_by_name_like(name):
        return (
            Recipe
            .select()
            .join(Category)
            .where(Recipe.name.like(f'%{name}%'))
            .order_by(Category.name, Recipe.name)
        )

    @staticmethod
    @update_ownership
    @update_authoring
    @insert_or_update
    def save(recipe):
        pass

    @classmethod
    @delete_by_primary_key
    def delete_by_id(cls, recipe_id):
        pass


from persistence.model.category import Category
from persistence.model.recipe import Recipe
