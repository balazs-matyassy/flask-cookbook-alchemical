from datetime import datetime

from sqlalchemy import ForeignKey, String, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column


class AuthoringMixin:
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow)
    created_by: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=True, index=True)
    modified_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow)
    modified_by: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=True, index=True)

    @property
    def _authoring_form(self):
        return {
            'created_at': self.created_at,
            'created_by': self.created_by,
            'modified_at': self.modified_at,
            'modified_by': self.modified_by
        }


class OwnershipMixin:
    owned_by: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False, index=True)

    @property
    def _ownership_form(self):
        return {
            'owned_by': self.owned_by
        }


class FileMixin:
    filename: Mapped[str] = mapped_column(String(180), nullable=False)
    mimetype: Mapped[str] = mapped_column(String(180), nullable=False)
    content: Mapped[bytes] = mapped_column(
        LargeBinary(length=(2**24-1)),
        nullable=False,
        deferred=True
    )

    @property
    def basename(self):
        return self.filename.rsplit('.', 1)[0] if '.' in self.filename else self.filename

    @property
    def extension(self):
        return '' if '.' not in self.filename else self.filename.rsplit('.', 1)[1]

    @property
    def _file_form(self):
        return {
            'filename': self.filename,
            'mimetype': self.mimetype,
            'content': self.content
        }

    @_file_form.setter
    def _file_form(self, data):
        if 'filename' in data:
            self.filename = data['filename']

        if 'mimetype' in data:
            self.mimetype = data['mimetype']

        if 'content' in data:
            self.content = data['content']

    def _validate_file_data(self, allowed_extensions=None):
        errors = []

        if not self.filename:
            errors.append('Filename missing.')
        elif allowed_extensions and self.extension not in allowed_extensions:
            errors.append('Invalid file extension.')

        if not self.mimetype:
            errors.append('Mime type missing.')

        if not self.content:
            errors.append('Content missing.')

        return errors
