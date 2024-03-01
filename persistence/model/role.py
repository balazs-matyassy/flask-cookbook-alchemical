from typing import List

from alchemical import Model
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Role(Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(180), nullable=False, unique=True)

    def __init__(self, role_id=None, name=''):
        super().__init__(
            id=role_id,
            name=name
        )

    users: Mapped[List['User']] = relationship(
        back_populates='role',
        order_by='asc(User.username)'
    )

    @property
    def form(self):
        return {
            'id': self.id,
            'name': self.name
        }

    @form.setter
    def form(self, data):
        if 'name' in data:
            self.name = data['name'].strip().upper()

    def validate(self):
        errors = []

        if self.name == '':
            errors.append('Name missing.')

        return errors

    def __repr__(self):
        return f'<Role {self.name}>'


from persistence.model.user import User
