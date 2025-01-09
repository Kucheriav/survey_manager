from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean
from app.database import Base
import os
import hashlib
import binascii


class User(Base):
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    _password = Column(String, nullable=False)
    _password_salt = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String)
    date_of_birth = Column(DateTime, nullable=False)
    city = Column(String, nullable=False)
    school = Column(String, nullable=False)
    profile_picture_filename = Column(String)
    is_admin = Column(Boolean, default=False)
    is_email_confirmed = Column(Boolean, default=False)


    @property
    def password(self):
        raise AttributeError("Нельзя напрямую получить значение пароля")

    def set_password(self, password):
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
        self._password = binascii.hexlify(pwdhash).decode('utf-8')
        self._password_salt = salt.decode('utf-8')

    def verify_password(self, password):
        stored_password = self._password
        stored_password_salt = self._password_salt.encode('ascii')
        pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), stored_password_salt, 100000)
        return stored_password == binascii.hexlify(pwdhash).decode('utf-8')

    def __str__(self):
        res = []
        for attr in dir(self):
            if not attr.startswith('__') and attr not in ['metadata',  'registry']:
                x = getattr(self, attr)
                res.append(f'{attr}: {x}')
        return ' '.join(res)




