from typing import List

from alchemical import Model
from sqlalchemy import Integer, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from persistence.mixins import OwnershipMixin, AuthoringMixin
from persistence.utils import try_parse_int


class Recipe(Model, OwnershipMixin, AuthoringMixin):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(180), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False)

    category: Mapped['Category'] = relationship(
        back_populates='recipes',
        foreign_keys=[category_id]
    )
    ingredients: Mapped[List['Ingredient']] = relationship(
        back_populates='recipe',
        order_by='asc(Ingredient.id)',
        cascade='all, delete-orphan'
    )
    images: Mapped[List['Image']] = relationship(
        back_populates='recipe',
        order_by='asc(Image.id)',
        cascade='all, delete-orphan'
    )

    def __init__(self, recipe_id=None, category_id=None, name='', description='', difficulty=1, category=None):
        super().__init__(
            id=recipe_id,
            category_id=category_id,
            name=name,
            description=description,
            difficulty=difficulty
        )

        if category:
            self.category = category

    @property
    def difficulty_description(self):
        if self.difficulty == 1:
            return 'Very easy'
        elif self.difficulty == 2:
            return 'Easy'
        elif self.difficulty == 3:
            return 'Medium'
        elif self.difficulty == 4:
            return 'Difficult'
        elif self.difficulty == 5:
            return 'Very difficult'

        return 'Unknown'

    @property
    def form(self):
        return {
            'id': self.id,
            'category_id': self.category_id,
            'name': self.name,
            'description': self.description,
            'difficulty': self.difficulty,
            **self._ownership_form,
            **self._authoring_form
        }

    @form.setter
    def form(self, data):
        if 'category_id' in data:
            self.category_id = try_parse_int(data['category_id'])

        if 'name' in data:
            self.name = data['name'].strip().capitalize()

        if 'description' in data:
            self.description = data['description'].strip()

        if 'difficulty' in data:
            self.difficulty = try_parse_int(data['difficulty'], 1, 1, 5)

    def validate(self):
        errors = []

        if not self.category_id:
            errors.append('Category missing.')

        if not self.name:
            errors.append('Name missing.')

        return errors

    def __repr__(self):
        return f'<Recipe {self.name}>'


from persistence.model.category import Category
from persistence.model.image import Image
from persistence.model.ingredient import Ingredient
