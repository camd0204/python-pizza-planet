

import pytest
from flask.cli import FlaskGroup
from flask_migrate import Migrate

from app import flask_app
from app.plugins import db
# flake8: noqa
from app.repositories.models import Ingredient, Order, OrderDetail, Size
from app.scripts import populate_db


manager = FlaskGroup(flask_app)

migrate = Migrate()
migrate.init_app(flask_app, db)
CLIENT_NUMBER = 30
ORDER_NUMBER = 100


@manager.command('test', with_appcontext=False)
def test():
    return pytest.main(['-v', './app/test'])

@manager.command('populate_db')
def populate_db_command():
    populate_db(CLIENT_NUMBER, ORDER_NUMBER)




if __name__ == '__main__':
    manager()
