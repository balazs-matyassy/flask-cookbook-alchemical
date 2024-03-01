from alchemical import Model
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from persistence.mixins import AuthoringMixin, FileMixin


class Image(Model, FileMixin, AuthoringMixin):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    recipe_id: Mapped[int] = mapped_column(ForeignKey('recipe.id'), nullable=False, index=True)

    recipe: Mapped['Recipe'] = relationship(
        back_populates='images',
        foreign_keys=[recipe_id]
    )

    def __init__(self, image_id=None, recipe_id=None, recipe=None, **kwargs):
        super().__init__(
            id=image_id,
            recipe_id=recipe_id,
            **kwargs
        )

        if recipe:
            self.recipe = recipe

    @property
    def form(self):
        return {
            'id': self.id,
            'recipe_id': self.recipe_id,
            **self._file_form,
            **self._authoring_form
        }

    @form.setter
    def form(self, data):
        self._file_form = data

    def validate(self):
        return self._validate_file_data({'png', 'jpg', 'jpeg', 'gif'})

    def __repr__(self):
        return f'<Image {self.recipe.name} - {self.filename}>'


from persistence.model.recipe import Recipe
