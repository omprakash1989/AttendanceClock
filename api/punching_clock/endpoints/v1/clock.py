import logging
import json
from datetime import datetime


from flask_restplus import Resource, marshal_with, marshal
from flask_login import login_user, logout_user, current_user, login_required
from flask import redirect

from api.restplus import api
from database import session
from api.punching_clock.business import check_if_any_active_spell, register_clock_in

logger = logging.getLogger("punching_clock")

cns = api.namespace('attendance', description='Operations related to punching_clock details fetch.')


@cns.route('/clock_out', strict_slashes=False)
class ClockOut(Resource):

    @login_required
    def get(self):
        """
        This is API handles the clock out request.

        """

        try:
            success = True
            error = False
            message = ''

            user = current_user
            current_time = datetime.now()
            active_spell = check_if_any_active_spell(current_user.id)
            is_active_spell = True if active_spell else False

            # If active spell then end it.
            if active_spell:
                active_spell.end = datetime.now()
                session.add(active_spell)
                session.commit()
                message = 'You have successfully clocked out.'
            else:
                error = True
                success = False
                message = 'You are not currently clocked in.'
        except Exception as exc:
            logger.exception("Exception while clocking out the user.")

        return redirect('/himama/home')


@cns.route('/clock_in', strict_slashes=False)
class ClockIn(Resource):

    @login_required
    def get(self):
        """
        This is API handles the clock in request.

        """

        try:
            success = True
            error = False
            message = ''

            current_time = datetime.now()
            active_spell = check_if_any_active_spell(current_user.id)

            # If active spell then end it.
            if not active_spell:
                if register_clock_in(current_user.id):
                    message = 'You have successfully clocked in.'
            else:
                error = True
                success = False
                message = 'You are already clocked in.'
        except Exception as exc:
            logger.exception("Exception while clocking In the user.")

        return redirect('/himama/home')
