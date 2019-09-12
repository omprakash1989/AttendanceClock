import pytest
import logging
import os
import sys

from alembic.command import upgrade, downgrade
from alembic.config import Config
from flask import Flask

from factory import initialize_app
from database import db as _db
from settings import APP_ENV
from settings.settings_celery import CELERY_BROKER_URL

# Setting alembic configurations.
ALEMBIC_CONFIG = '../app/migrations/alembic.ini'
config = Config(ALEMBIC_CONFIG)
config.set_main_option("script_location", "migrations")


logger = logging.getLogger("punching_clock")


@pytest.fixture(scope='function')
def check_environment():
    app_env = os.environ.get("APP_ENV", 'production')
    if app_env == 'production' or APP_ENV == 'production':
        logger.error("\nIs this a production server? Skipping unit tests.")
        logger.error("\nIf you wants to run unittests, make sure APP_ENV is set in system variable and setting.")
        sys.exit()


@pytest.fixture(scope='session')
def app(request):
    # Check environment to make sure it's not production.
    check_environment()
    # New app context is required which is doing to be used through out the tests.
    app = Flask('TESTING', instance_relative_config=True)
    app = initialize_app(flask_app=app, config='settings')
    context = app.app_context()
    context.push()

    def teardown():
        # Remove the context once over.
        context.pop()

    # Register teardown.
    request.addfinalizer(teardown)
    return app


@pytest.fixture(scope='session')
def db(app, request):
    """
        This will be activated once we have test url.
        :param app:
        :param request:
        :return:
        """

    _db.app = app

    # Apply migrations.
    # apply_migrations()

    def teardownrdown():
        # As a tear down downgrade the revision to base.
        # Safer option, got to check with different constraints though.
        downgrade(config, revision='base')

        # Just a make sure.
        _db.drop_all()

    # request.addfinalizer(teardown)
    return _db


def apply_migrations():
    """Applies all alembic migrations."""
    upgrade(config, 'head')


@pytest.fixture(scope='function')
def session(db, request):
    """Creates a new database session for a test."""
    conn = db.engine.connect()
    transaction = conn.begin()

    options = dict(bind=conn, binds={})
    session = db.create_scoped_session(options=options)

    # Attach the session.
    db.session = session

    def teardown():
        transaction.rollback()
        conn.close()
        session.remove()

    request.addfinalizer(teardown)
    return session
