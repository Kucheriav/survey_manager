from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message
from config import Config
import re

app = Flask(__name__)
app.config.from_object(Config)

mail = Mail(app)

users = {}

# Стартовая страница для регистрации
@app.route('/')
def register():
    return render_template('register.html')

# Обработка данных из формы регистрации
@app.route('/register', methods=['POST'])
def process_registration():
    username = request.form['username']
    email = request.form['email']

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return "Некорректный адрес электронной почты. Пожалуйста, вернитесь и попробуйте снова."

    # Отправка письма с подтверждением
    msg = Message('Подтверждение регистрации', sender=app.config['MAIL_USERNAME'], recipients=[email])
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
