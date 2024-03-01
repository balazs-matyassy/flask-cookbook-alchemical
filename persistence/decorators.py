from datetime import datetime
import functools

from flask import g


def get_by_primary_key(view):
    @functools.wraps(view)
    def wrapped_view(cls, entity_key):
        return g.session.get(cls.get_entity_cls(), entity_key)

    return wrapped_view


def scalar(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        return g.session.scalar(view(*args, **kwargs))

    return wrapped_view


def scalars(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        return g.session.scalars(view(*args, **kwargs))

    return wrapped_view


def update_authoring(view):
    @functools.wraps(view)
    def wrapped_view(entity):
        now = datetime.utcnow()

        if not entity.id:
            if hasattr(entity, 'created_at'):
                entity.created_at = now

            if hasattr(entity, 'created_by'):
                entity.created_by = g.user.id

        if hasattr(entity, 'modified_at'):
            entity.modified_at = now

        if hasattr(entity, 'modified_by'):
            entity.modified_by = g.user.id

        return view(entity)

    return wrapped_view


def update_ownership(view):
    @functools.wraps(view)
    def wrapped_view(entity):
        if not entity.id and hasattr(entity, 'owned_by'):
            entity.owned_by = g.user.id

        return view(entity)

    return wrapped_view


def insert_or_update(view):
    @functools.wraps(view)
    def wrapped_view(entity):
        if not entity.id:
            g.session.add(entity)

        g.session.commit()

        return entity

    return wrapped_view


def delete_by_primary_key(view):
    @functools.wraps(view)
    def wrapped_view(cls, entity_key):
        g.session.delete(g.session.get(cls.get_entity_cls(), entity_key))
        g.session.commit()

    return wrapped_view
