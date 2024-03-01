from alchemical import Model
from sqlalchemy import Integer, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import generate_password_hash, check_password_hash

from persistence.mixins import AuthoringMixin
from persistence.utils import try_parse_int


class User(Model, AuthoringMixin):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(180), nullable=False, unique=True)
    digest: Mapped[str] = mapped_column('password', String(180), nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey('role.id'), nullable=False, index=True)

    role: Mapped['Role'] = relationship(
        back_populates='users',
        foreign_keys=[role_id]
    )

    def __init__(self, user_id=None, username='', digest=None, role_id=None, role=None):
        super().__init__(
            id=user_id,
            username=username,
            digest=digest,
            role_id=role_id
        )

        if role:
            self.role = role

    @property
    def password(self):
        return None

    @password.setter
    def password(self, value):
        if value:
            self.digest = generate_password_hash(value)

    @property
    def form(self):
        return {
            'id': self.id,
            'username': self.username,
            'digest': self.digest,
            'role_id': self.role_id,
            **self._authoring_form
        }

    @form.setter
    def form(self, data):
        if 'username' in data:
            self.username = data['username'].strip().lower()

        if 'password' in data:
            self.password = data['password']

        if 'role_id' in data:
            self.role_id = try_parse_int(data['role_id'])

    def check_password(self, password):
        return check_password_hash(self.digest, password)

    def validate(self):
        errors = []

        if not self.username:
            errors.append('Username missing.')

        if not self.digest:
            errors.append('Password missing.')

        if not self.role_id:
            errors.append('Role missing.')

        return errors

    def __repr__(self):
        return f'<User {self.username}>'


from persistence.model.role import Role
