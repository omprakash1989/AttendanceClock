from datetime import datetime, timedelta
import enum

from flask_admin.contrib.sqla import ModelView, filters
from flask_login import current_user, UserMixin
from sqlalchemy import event, cast, Date
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.fields import TextField
from flask_admin.form.fields import Select2Field
from flask_admin.model.form import converts
from flask_admin.contrib.sqla.form import AdminModelConverter
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from . import db


# Define signals.
def post_update(mapper, connect, target):
    """ Post update signal.

    Parameter
    ---------
    mapper : <sqlalchemy.orm.mapper>
        SqlAlchemy mapper object

    connect : <sqlalchemy.engine.Connection>
        the Connection being used to emit

    target : <sqlalchemy.orm.mapper>
        target object associated with the instance.

    Returns
    -------
    None
    """

    target.post_update(connect)


def post_save(mapper, connect, target):
    """ Post save signal.

    Parameter
    ---------
    mapper : <sqlalchemy.orm.mapper>
        SqlAlchemy mapper object

    connect : <sqlalchemy.engine.Connection>
        the Connection being used to emit

    target : <sqlalchemy.orm.mapper>
        target object associated with the instance.

    Returns
    -------
    None
    """
    target.post_save(connect)


class ApplicationUser(db.Model, UserMixin):
    __tablename__ = 'application_users'

    id = db.Column('id', db.Integer, primary_key=True)
    user_name = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=True)
    name = db.Column(db.String, nullable=True)
    created_dttm = db.Column(db.DateTime, default=datetime.now)
    updated_dttm = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    created_by = db.Column(db.String, nullable=True)
    updated_by = db.Column(db.String, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    can_update = db.Column(db.Boolean, default=False)
    can_create = db.Column(db.Boolean, default=False)
    can_delete = db.Column(db.Boolean, default=False)


    @staticmethod
    def set_password(password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def active_spell(self):
        return db.session.query(Spell).filter(cast(Spell.start, Date) == datetime.today().date(), Spell.user_id == current_user.id, Spell.end.is_(None)).count() > 0

    def __repr__(self):
        return self.user_name


class Spell(db.Model):
    __tablename__ = "spells"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("application_users.id"))
    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime)

    teacher_name = db.relationship('ApplicationUser', backref=db.backref('Spell'))

    def duration(self):
        # Deal with ongoing spells
        return self.end - self.start

    def __init__(self, start):
        self.start = start

    def __repr__(self):
        return "<Spell from {0} to {1}>". \
            format(self.start, self.end)

    @staticmethod
    def date_filter(datetime_input):
        return db.session.query(Spell).filter(cast(Spell.start, Date) == datetime_input.date(),
                                       Spell.user_id == current_user.id).all()


class EnumField(Select2Field):
    def __init__(self, column, **kwargs):
        assert isinstance(column.type, enum.Enum)

        def coercer(value):
            # coerce incoming value into an enum value
            if isinstance(value, column.type.enum_class):
                return value
            elif isinstance(value, basestring):
                return column.type.enum_class[value]
            else:
                assert False

        super(EnumField, self).__init__(
            choices=[(v, v) for v in column.type.enums],
            **kwargs)

    def pre_validate(self, form):
        # we need to override the default SelectField validation because it
        # apparently tries to directly compare the field value with the choice
        # key; it is not clear how that could ever work in cases where the
        # values and choice keys must be different types

        for (v, _) in self.choices:
            if self.data == self.coerce(v):
                break
        else:
            raise ValueError(self.gettext('Not a valid choice'))


class CustomAdminConverter(AdminModelConverter):
    @converts("enum.Enum")
    def conv_enum(self, field_args, **extra):
        return EnumField(column=extra["column"], **field_args)


class DateFilterConverter(filters.FilterConverter):
    datetime_filters = (
        filters.DateTimeBetweenFilter
    )


class TotalTimeField(TextField):
    def process_data(self, value):
        self.data = ''
        self.orig_hash = value

    def process_fromdata(self, valuelist):
        value = ''
        if valuelist:
            value = valuelist[0]
        if value:
            self.data = generate_password_hash(value)
        else:
            self.data = self.orig_hash



class SpellView(ModelView):

    def is_accessible(self):
        return current_user.is_authenticated

    column_display_pk = False
    can_delete = False
    can_create = False

    @property
    def can_edit(self):
        return current_user.is_admin or current_user.can_update

    @property
    def can_create(self):
        return False

    @property
    def can_delete(self):
        return current_user.is_admin or current_user.can_delete


    page_size = 20
    edit_modal = True
    column_hide_backrefs = False
    column_list = ('teacher_name', 'start', 'end')
    column_filters = ("start", 'end', 'teacher_name')

    column_exclude_list = ('created_by', 'updated_by', 'updated_dttm')

    def get_query(self):
        if current_user.is_admin:
            return self.session.query(self.model).filter()
        else:
            return self.session.query(self.model).filter(self.model.user_id == current_user.id)


class PasswordField(TextField):
    def process_data(self, value):
        self.data = ''
        self.orig_hash = value

    def process_fromdata(self, valuelist):
        value = ''
        if valuelist:
            value = valuelist[0]
        if value:
            self.data = generate_password_hash(value)
        else:
            self.data = self.orig_hash


class AdminUserView(ModelView):

    column_list = ('user_name', 'email', 'name', 'is_active', 'can_edit', 'can_delete')

    @property
    def can_edit(self):
        if current_user.is_admin:
            return True

    @property
    def can_create(self):
        if current_user.is_admin:
            return True

    @property
    def can_delete(self):
        if current_user.is_admin:
            return True

    form_overrides = dict(
        password=PasswordField,
    )

    form_widget_args = dict(
        password=dict(
            placeholder='Enter new password here to change password',
        )
    )

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_name == 'admin'

    def on_model_change(self, form, model, is_created):
        model.password = ApplicationUser.set_password(model.password)
        model.updated_by = current_user.name
        model.updated_dttm = datetime.now()

    column_display_pk = False
    page_size = 20
    edit_modal = True


# Registering signals.
