"""Adding initial user.

Revision ID: 29b9e3d13be0
Revises: a8e6b2c4be0a
Create Date: 2018-10-19 12:52:15.902642

"""
import datetime

from alembic import op
import sqlalchemy as sa

from sqlalchemy.orm.exc import NoResultFound

from database import db
from database.models import ApplicationUser


# revision identifiers, used by Alembic.
revision = '29b9e3d13be0'
down_revision = 'a90dbc8696dc'
branch_labels = None
depends_on = None

user_name = 'admin'


def upgrade():
    password = ApplicationUser.set_password('admin')
    email = 'test@test_email.com'
    name = 'Admin User'

    conn = op.get_bind()
    application_user = conn.execute("SELECT id FROM application_users WHERE user_name='{}'".format(user_name))
    user = application_user.fetchone()

    if not user:
        conn.execute("INSERT INTO application_users (user_name, password, email, name, created_dttm, created_by, is_admin,"
                     " is_active) VALUES ('{}', '{}', '{}', '{}', NOW(), '{}', TRUE, TRUE )".format(user_name, password, email, name, 'Migration User'))


def downgrade():
    conn = op.get_bind()
    application_user = conn.execute("SELECT id FROM application_users WHERE user_name='{}'".format(user_name))
    user = application_user.fetchone()

    if user:
        conn.execute("DELETE FROM application_users WHERE user_name='{}'".format(user_name))
