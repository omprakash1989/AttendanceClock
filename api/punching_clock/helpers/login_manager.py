from flask_login import LoginManager

from wsgi import application
from api.punching_clock.business import get_admin_user

login = LoginManager(application)


@login.user_loader
def load_user(user_email):
    return get_admin_user(user_email)
