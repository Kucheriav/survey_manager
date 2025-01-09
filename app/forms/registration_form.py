from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
import re
from app.models.user import User

class RegistrationForm(FlaskForm):
    email = StringField('Почта', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    surname = StringField('Фамилия', validators=[DataRequired()])
    first_name = StringField('Имя', validators=[DataRequired()])
    last_name = StringField('Отчество')
    date_of_birth = DateField('Дата рождения', validators=[DataRequired()])
    city = StringField('Город', validators=[DataRequired()])
    school = StringField('Школа', validators=[DataRequired()])
    profile_picture = FileField('Загрузить фотографию профиля')
    rules = BooleanField('Я ознакомился с правилами', validators=[DataRequired()])
    submit = SubmitField('Подтвердить')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Пользователь с таким адресом электронной почты уже существует.')
        if not re.match(r"[^@]+@[^@]+.[^@]+", email):
            raise ValidationError('Неверный формат почты.')

    def validate_rules(self, rules):
        if not rules.data:
            raise ValidationError('Ознакомьтесь с правилами')

    def validate_password(self, password):
        if len(password.data) < 8:
            raise ValidationError("Пароль должен быть не короче 8 символов!")


