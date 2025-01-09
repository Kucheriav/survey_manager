import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from itsdangerous import URLSafeTimedSerializer
from app.config import config

def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(config.SECRET_KEY)
    return serializer.dumps(email, salt=config.SECURITY_PASSWORD_SALT)

def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(config.SECRET_KEY)
    try:
        email = serializer.loads(
            token,
            salt=config.SECURITY_PASSWORD_SALT,
            max_age=expiration
        )
    except:
        return False
    return email

def send_email(user_email, subject, message):
    msg = MIMEMultipart()
    msg['From'] = config.MAIL_USERNAME  # Адрес отправителя
    msg['To'] = user_email
    msg['Subject'] = subject

    body = message
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP(config.MAIL_SERVER, config.MAIL_PORT)
    server.starttls()  # Включаем шифрование TLS
    server.login(config.MAIL_USERNAME, config.MAIL_PASSWORD)  # Логин и пароль от вашего почтового аккаунта
    text = msg.as_string()
    server.sendmail(msg['From'], msg['To'], text)
    server.quit()

from flask_mail import Message

def send_confirmation_email(user_email):
    token = generate_confirmation_token(user_email)
    confirm_url = url_for('confirm_email', token=token, _external=True)
    html = render_template('email_confirm.html', confirm_url=confirm_url)
    subject = "Подтвердите ваш аккаунт"
    send_email(user_email, subject, html)