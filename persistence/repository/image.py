from persistence.decorators import (get_by_primary_key, scalar, scalars,
                                    update_authoring, insert_or_update, delete_by_primary_key)
from persistence.repository import AbstractRepository


class ImageRepository(AbstractRepository):
    @staticmethod
    def get_entity_cls():
        return Image

    @classmethod
    @get_by_primary_key
    def find_by_id(cls, image_id):
        pass

    @staticmethod
    @scalars
    def find_all(recipe_id):
        return (
            Image
            .select()
            .order_by(Image.id)
        )

    @staticmethod
    @scalar
    def find_by_id_and_recipe_id(image_id, recipe_id):
        return (
            Image
            .select()
            .where(Image.id == image_id, Image.recipe_id == recipe_id)
        )

    @staticmethod
    @scalars
    def find_all_by_recipe_id(recipe_id):
        return (
            Image
            .select()
            .where(Image.recipe_id == recipe_id)
            .order_by(Image.id)
        )

    @staticmethod
    @update_authoring
    @insert_or_update
    def save(ingredient):
        pass

    @classmethod
    @delete_by_primary_key
    def delete_by_id(cls, image_id):
        pass


from persistence.model.image import Image
