import click
from alchemical.flask import Alchemical
from flask import g

from persistence.model.role import Role
from persistence.model.user import User

db = Alchemical()


def init_app(app):
    app.cli.add_command(__install_command)
    app.before_request(__create_session)
    app.teardown_appcontext(__close_session)

    db.init_app(app)


def install():
    db.drop_all()
    db.create_all()

    with db.Session() as session:
        role_admin = Role(name='ADMIN')
        session.add(role_admin)

        role_moderator = Role(name='MODERATOR')
        session.add(role_moderator)

        role_editor = Role(name='EDITOR')
        session.add(role_editor)

        role_user = Role(name='USER')
        session.add(role_user)

        user = User()
        user.username = 'admin'
        user.password = 'Admin123.'
        user.role = role_admin
        session.add(user)

        session.commit()


@click.command('install')
def __install_command():
    install()

    click.echo('Application installation successful.')


def __create_session():
    if 'session' not in g:
        g.session = db.Session()


def __close_session(e):
    if 'session' in g:
        g.pop('session').close()
