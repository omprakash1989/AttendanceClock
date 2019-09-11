import logging
from datetime import datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import cast, Date

from database.models import ApplicationUser, Spell
from database import session

logger = logging.getLogger("punching_clock")


def get_admin_user(username):
    """
    Fetch ApplicationUser by username.


    Parameters:
    -----------
    `username`: <String>
        User name

    Returns
    -------
    <database.models.ApplicationUser>
        User object if match found
    <None>
        In case no match found.
    """

    user = None
    try:
        user = ApplicationUser.query.filter_by(user_name=username).one()
    except NoResultFound:
        pass

    return user


def check_if_any_active_spell(user_id):

    """
    Check If any active spell of teacher going on.
    :param user_id: <int>
        User id of current user.
    :return: <database.models.Spell>
        Spell object if active else None
    """

    active_spell = session.query(Spell).filter(cast(Spell.start, Date) == datetime.today().date(),
                                       Spell.user_id == user_id, Spell.end.is_(None), Spell.start.isnot(None)).first()

    return active_spell


def register_clock_in(user_id):
    """
    Register clock in for a teacher.
    :param user_id:
    :return: True or False
    """
    success = True
    try:
        spell = Spell(start=datetime.now())
        spell.user_id = user_id
        session.add(spell)
        session.commit()
    except Exception as exc:
        success = False
        logger.exception(exc)

    return success
