import logging
import csv
from datetime import datetime, timedelta
from operator import itemgetter
from io import StringIO

from flask import render_template, make_response, url_for, redirect, request, Response
from flask_login import login_user, logout_user, current_user, login_required
from flask_restplus import Resource, marshal_with, marshal

from api.punching_clock.business import get_admin_user
from api.restplus import api
from database import session

logger = logging.getLogger("punching_clock")

ans = api.namespace('/', description='Operations related to user sessions.')


@ans.route('/login', strict_slashes=False)
class Login(Resource):

    def get(self):
        """
        Login get handler.
        """
        if not current_user.is_authenticated:
            return make_response(render_template('/admin/login.html'))
        else:
            return redirect('/himama/home')

    def post(self):
        """
        Login method for Admin Panel.
        """

        authenticated = False
        error = ''
        username = ''
        try:
            if not current_user.is_authenticated:
                username = request.form.get('username')
                password = request.form.get('password')

                user = get_admin_user(username)
                if user:
                    if user.check_password(password):
                        authenticated = True
                        login_user(user)
                    else:
                        error = "Invalid credentials."
                else:
                    error = "No such user exists."
            else:
                authenticated = True

        except Exception as exc:
            logger.exception("Exception while logging In the user.")

        if authenticated:
            return redirect('/himama/home')
        else:
            return make_response(render_template('/admin/login.html', **{"error": error, "username": username}))


@ans.route('/logout', strict_slashes=False)
class Logout(Resource):

    def get(self):
        """
        Logout handler.
        """

        try:
            if current_user.is_authenticated:
                logout_user()
        except Exception as exc:
            logger.exception("Exception while logging out the user.")

        return redirect('/himama/login')
