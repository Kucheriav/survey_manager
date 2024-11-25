from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_mail import Mail, Message
import re
from app.log_writer import setup_logger
from app.models.user import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['MAIL_SERVER'] = 'smtp.yourmailserver.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@example.com'
app.config['MAIL_PASSWORD'] = 'your_email_password'

login_manager = LoginManager()
login_manager.init_app(app)

mail = Mail(app)
logger = setup_logger(__name__)
users = {}

@login_manager.user_loader
def load_user(user_id):
    # Загрузите пользователя по user_id
    return User.get(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Логика входа
    pass

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Логика входа
    pass


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
# Стартовая страница для регистрации
@app.route('/')
def index():
    return render_template('index.html')

# Обработка данных из формы регистрации
@app.route('/register', methods=['POST'])
def process_registration():
    username = request.form['username']
    email = request.form['email']

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return "Некорректный адрес электронной почты. Пожалуйста, вернитесь и попробуйте снова."

    # Отправка письма с подтверждением
    msg = Message('Подтверждение регистрации', sender='your_email@example.com', recipients=[email])
    msg.body = f'Здравствуйте, {username}! Для завершения регистрации перейдите по ссылке: http://127.0.0.1:5000/confirm/{email}'
    mail.send(msg)

    users[email] = username

    return "Письмо с подтверждением отправлено. Пожалуйста, проверьте свою почту."

# Страница подтверждения регистрации
@app.route('/confirm/<email>')
def confirm_registration(email):
    if email in users:
        return redirect(url_for('questionnaire'))
    else:
        return "Ошибка при подтверждении регистрации."

# Страница с вопросами
@app.route('/questionnaire')
def questionnaire():
    return render_template('questionnaire.html')

if __name__ == '__main__':
    app.run(debug=True)
