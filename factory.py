"""
Factory of the application which contains initialization of the application.

The whole purpose is:
    1: Testing. You can have instances of the application with different settings to test every case.

    2: Multiple instances. Imagine you want to run different versions of the same application. Of course you could have
     multiple instances with different configs set up in your webserver, but if you use factories,
    you can have multiple instances of the same application running in the same application process which can be handy.

    Ref: http://flask.pocoo.org/docs/0.12/patterns/appfactories/
"""

import logging.config

from flask import Blueprint, g
from flask_migrate import Migrate
from celery import Celery
from flask_admin import Admin
from flask_login import LoginManager, current_user

from api.punching_clock.endpoints.v1.clock import cns as clock_namespace
from api.punching_clock.endpoints.v1.admin import ans as admin_panel_namespace
from api.restplus import api
from database import db
from database.models import AdminUserView, ApplicationUser, Spell, SpellView
from logger import setup_logging
from settings.settings_celery import CELERY_BROKER_URL


# Initialize celery.
celery = Celery(__name__, broker=CELERY_BROKER_URL)
celery.config_from_object('settings.settings_celery')

# Register tasks.

# Setup logging.
setup_logging()
logger = logging.getLogger("punching_clock")


def configure_app(flask_app, config):
    # Load config to app.
    flask_app.config.from_object(config)


def initialize_app(flask_app, config='settings', override={}):
    logger.info("Initializing the application.")
    configure_app(flask_app, config=config)

    # Check if any external override in config to be applied.
    if override:
        flask_app.config.update(override)

    admin = Admin(flask_app, name='Employee Attendance', template_mode='bootstrap3')
    admin.add_view(AdminUserView(ApplicationUser, db.session, 'Teachers'))
    admin.add_view(SpellView(Spell, db.session, 'Clock Timings'))

    # Register admin panel.
    admin_blueprint = Blueprint('admin_api', __name__, url_prefix='/himama')
    api.init_app(admin_blueprint)
    api.add_namespace(admin_panel_namespace)
    flask_app.register_blueprint(admin_blueprint)

    clock_blueprint = Blueprint('clock_api', __name__, url_prefix='/himama')
    api.init_app(clock_blueprint)
    api.add_namespace(clock_namespace)
    # # Register the API blueprint.blueprint
    flask_app.register_blueprint(clock_blueprint)

    # Initialize db and app.
    db.init_app(flask_app)

    # Registering login manager.
    login = LoginManager()
    login.init_app(flask_app)



    # Remember the current user
    @flask_app.before_request
    def before_request():
        g.user = current_user

    @login.user_loader
    def load_user(user_id):
        return ApplicationUser.query.get(user_id)
    # Path set according to the current repo.
    migration_path = 'migrations'

    # Flask Migration.
    Migrate(flask_app, db, directory=migration_path)

    return flask_app
