"""The application's model objects"""
from .meta import Session, Base

import uuid
import random
import hashlib
from datetime import datetime

import sqlalchemy as sa
import sqlalchemy.dialects.postgresql


def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    Session.configure(bind=engine)

class UUID(sa.types.TypeDecorator):
    """Platform-independent GUID type.

    Uses Postgresql's UUID type, otherwise uses
    CHAR(32), storing as stringified hex values.

    """
    impl = sa.types.CHAR

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(sqlalchemy.dialects.postgresql.UUID())
        else:
            return dialect.type_descriptor(sa.types.CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return "%.32x" % uuid.UUID(value)
            else:
                # hexstring
                return "%.32x" % value

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            return uuid.UUID(value)


class Password(object):
    """This is returned for user.password. It simply has an == check builtin,
which tests the SHA512 of the password and salt."""

    def __init__(self, user):
        self.user = user

    def __eq__(self, password):
        return hashlib.sha512(password.encode('utf-8')+self.user.salt).digest() \
            == self.user.password_sha512

    def __str__(self):
        return "<sha512 hashed password+salt \"%r\">" % (
            self.user.password_sha512)
        
class PasswordProperty(object):
    """This is the password attribute of User.

When set, it writes to user.password_sha512 and user.salt.

When get, it returns a Password object.
"""

    def __get__(self, instance, owner):
        if instance:
            return Password(instance)
        else:
            return self

    def __set__(self, instance, value):
        instance.salt = ''.join((chr(random.getrandbits(8)) for i in range(64)))
        instance.password_sha512 = hashlib.sha512(value.encode('utf-8')+instance.salt).digest()

class User(Base):
    """A user.

id: PKey
username: Unique username.
salt: random salt. Regenerated each time the password changes.
password_sha512: SHA512 hash of the password+salt
email: The email, if any. Not unique. (TODO: Allow multiple emails for an account.)
admin: Whether they are admin.
password: Not stored. This property you to set and check the password.
"""

    __tablename__ = 'users'

    id              = sa.Column(UUID, primary_key=True, default=uuid.uuid4)
    username        = sa.Column(sa.types.Unicode, unique=True, nullable=False)
    salt            = sa.Column(sa.types.LargeBinary(64), nullable=False)
    password_sha512 = sa.Column(sa.types.LargeBinary(64), nullable=False)
    email           = sa.Column(sa.types.Unicode, nullable=True)
    admin           = sa.Column(sa.types.Boolean, nullable=False, default=False)

    password        = PasswordProperty()
