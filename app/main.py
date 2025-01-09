from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
import os
from app.log_writer import setup_logger
from app.models.user import User
from app.registration import *
from app.forms import registration_form, login_form, profile_form


app = Flask(__name__)
app.config.update(config.dict())


login_manager = LoginManager()
login_manager.init_app(app)


logger = setup_logger(__name__)


@login_manager.user_loader
def load_user(user_id):
    # Загрузите пользователя по user_id
    return User.get(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Логика входа
    pass

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

# Страница с вопросами
@app.route('/questionnaire')
def questionnaire():
    # нет ее пока
    return render_template('questionnaire.html')



# Стартовая страница для регистрации
@app.route('/')
def index():
    return render_template('index.html')

# Обработка данных из формы регистрации
@app.route('/register', methods=['GET', 'POST'])
def register():
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

    form = registration_form.RegistrationForm()
    if form.validate_on_submit():
        # начинаем разбор данных с формы
        user = User(email=form.email.data,
                    surname=form.surname.data,
                    first_name=form.first_name.data,
                    date_of_birth=form.date_of_birth.data,
                    city=form.city.data,
                    school=form.school.data)
        if form.last_name.data:
            user.last_name = form.last_name.data
        user.set_password(form.password.data)
        file = form.profile_picture.data
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)  # Безопасное имя файла
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))  # Сохранение файла
            user.profile_picture_filename = filename

        # вот тут затыка с базулькой
        db.session.add(user)
        db.session.commit()
        # Отправляем письмо с подтверждением
        send_confirmation_email(user.email)

        flash('Пожалуйста, проверьте вашу электронную почту и подтвердите регистрацию.', 'info')
        return redirect(url_for('login'))
    return render_template('register.html', title='Регистрация', form=form)

# Страница подтверждения регистрации
@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    user = User.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        flash('Account already confirmed. Please login.', 'success')
    else:
        user.confirmed = True
        db.session.update(user)
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
