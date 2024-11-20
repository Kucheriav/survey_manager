from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates
from app.database import Base
import re
import os
import hashlib
import binascii


class User(Base):
    id = Column(Integer, primary_key=True)
    login = Column(String, nullable=False)
    _password = Column(String, nullable=False)
    _password_code_salt = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    last_name = Column(String)
    date_of_birth = Column(DateTime, nullable=False)
    gender = Column(String, nullable=False)
    city = Column(String, nullable=False)
    _email = Column(String, nullable=False, unique=True)
    profile_picture = Column(String)
    is_admin = Column(Boolean, default=False)

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

    @validates('phone_number')
    def validate_phone_number(self, phone_number):
        pattern = r'^\+\d{11}$'
        if not re.match(pattern, phone_number):
            raise ValueError(f"Неверный формат номера телефона: {phone_number}. Ожидается формат: +71234567890")
        return phone_number


    def validate_email(self, email):
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if re.match(pattern, email):
            return True
        return False

    def set_email(self, email):
        if self.validate_email(email):
            self._email = email
        else:
            raise ValueError("Некорректный формат электронной почты")


    def __str__(self):
        res = []
        for attr in dir(self):
            if not attr.startswith('_') and attr not in ['metadata',  'registry']:
                x = getattr(self, attr)
                res.append(f'{attr}: {x}')
        return ' '.join(res)




