import json
from random import choice, randint
import string

# Предположим, что у вас уже есть определение модели User

# Генерация случайной строки для имени и фамилии
def random_string(length):
    letters = string.ascii_letters
    return ''.join(choice(letters) for _ in range(length))

def generate_users(n):
    # Создание n разных пользователей
    users = []
    for _ in range(1, n + 1):
        user = {
            'login': f'user{_}',
            'name': random_string(8),
            'surname': random_string(10),
            'password': ''.join(choice(string.ascii_letters + string.digits) for _ in range(10)),
            'email': f'user{_}@example.com',
            'reg_date': '2022-01-01 00:00:00',  # Предположим, что это формат даты и времени
            'last_visit': '2022-01-02 00:00:00',
            'is_teacher': choice([True, False]),
            'is_admin': choice([True, False])
        }
        users.append(user)

    # Сохранение информации в JSON-файл
    with open('test_users.json', 'w') as file:
        json.dump(users, file, indent=4)



