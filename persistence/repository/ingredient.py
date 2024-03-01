from persistence.decorators import (get_by_primary_key, scalar, scalars,
                                    update_authoring, insert_or_update, delete_by_primary_key)
from persistence.repository import AbstractRepository


class IngredientRepository(AbstractRepository):
    @staticmethod
    def get_entity_cls():
        return Ingredient

    @classmethod
    @get_by_primary_key
    def find_by_id(cls, ingredient_id):
        pass

    @staticmethod
    @scalars
    def find_all(recipe_id):
        return (
            Ingredient
            .select()
            .order_by(Ingredient.id)
        )

    @staticmethod
    @scalar
    def find_by_id_and_recipe_id(ingredient_id, recipe_id):
        return (
            Ingredient
            .select()
            .where(Ingredient.id == ingredient_id, Ingredient.recipe_id == recipe_id)
        )

    @staticmethod
    @scalars
    def find_all_by_recipe_id(recipe_id):
        return (
            Ingredient
            .select()
            .where(Ingredient.recipe_id == recipe_id)
            .order_by(Ingredient.id)
        )

    @staticmethod
    @update_authoring
    @insert_or_update
    def save(ingredient):
        pass

    @classmethod
    @delete_by_primary_key
    def delete_by_id(cls, ingredient_id):
        pass


from persistence.model.ingredient import Ingredient
