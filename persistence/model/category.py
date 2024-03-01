from typing import List

from alchemical import Model
from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from persistence.mixins import AuthoringMixin


class Category(Model, AuthoringMixin):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(180), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    recipes: Mapped[List['Recipe']] = relationship(
        back_populates='category',
        order_by='asc(Recipe.name)'
    )

    def __init__(self, category_id=None, name='', description=''):
        super().__init__(
            id=category_id,
            name=name,
            description=description
        )

    @property
    def form(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            **self._authoring_form
        }

    @form.setter
    def form(self, data):
        if 'name' in data:
            self.name = data['name'].strip().capitalize()

        if 'description' in data:
            self.description = data['description'].strip()

    def validate(self):
        errors = []

        if self.name == '':
            errors.append('Name missing.')

        return errors

    def __repr__(self):
        return f'<Category {self.name}>'


from persistence.model.recipe import Recipe
