from alchemical import Model
from sqlalchemy import Integer, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from persistence.mixins import AuthoringMixin
from persistence.utils import try_parse_int


class Ingredient(Model, AuthoringMixin):
    __table_args__ = (
        UniqueConstraint('recipe_id', 'name'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    recipe_id: Mapped[int] = mapped_column(ForeignKey('recipe.id'), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(180), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit: Mapped[str] = mapped_column(String(180), nullable=False)

    recipe: Mapped['Recipe'] = relationship(
        back_populates='ingredients',
        foreign_keys=[recipe_id]
    )

    def __init__(self, ingredient_id=None, recipe_id=None, name='', quantity=0, unit='', recipe=None):
        super().__init__(
            id=ingredient_id,
            recipe_id=recipe_id,
            name=name,
            quantity=quantity,
            unit=unit
        )

        if recipe:
            self.recipe = recipe

    @property
    def form(self):
        return {
            'id': self.id,
            'recipe_id': self.recipe_id,
            'name': self.name,
            'quantity': self.quantity,
            'unit': self.unit,
            **self._authoring_form
        }

    @form.setter
    def form(self, data):
        if 'name' in data:
            self.name = data['name'].strip().lower()

        if 'quantity' in data:
            self.quantity = try_parse_int(data['quantity'], 0)

        if 'unit' in data:
            self.unit = data['unit'].strip().lower()

    def validate(self):
        errors = []

        if not self.name:
            errors.append('Name missing.')

        if self.quantity < 0:
            errors.append('Invalid quantity.')

        return errors

    def __repr__(self):
        return f'<Ingredient {self.recipe.name} - {self.name}>'


from persistence.model.recipe import Recipe
