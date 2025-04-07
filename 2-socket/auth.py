"""
Класс AuthUser реализует авторизацию пользователя

- информация о пользователях хранится на диске в файле users.json и в словаре во время работы программы
- пароли хранятся в виде хешей
- метод класса load_users загружает пользователей из файла в словарь
- метод класса save_users сохраняет пользователей в файл (перезаписывает)
- метод класса add_user добавляет нового пользователя в словарь и в файл
- метод класса check_user проверяет пользователя на существование в словаре
- метод класса check_pass проверяет пароль пользователя
- метод класса delete_user удаляет пользователя из словаря и из файла
- метод класса clear_all_users очищает пользователей из словаря и удаляет файл
- метод класса _hash_password хеширует пароль пользователя

"""

import json
import hashlib
import os


class AuthUser:
    """Класс для авторизации пользователей"""

    def __init__(self, filename: str = "users.json", skip_load: bool = False):
        self.filename = filename
        self.users = {}
        if not skip_load:
            self.load_users()

    def load_users(self):
        """Загрузка пользователей из файла в словарь"""
        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                self.users = json.load(file)
        else:
            self.users = {}

    def save_users(self):
        """Сохранение пользователей из словаря в файл"""
        with open(self.filename, "w") as file:
            json.dump(self.users, file)

    def clear_all_users(self):
        """Очистка пользователей из и словаря"""
        self.users = {}
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def delete_user(self, login: str) -> bool:
        """Удаление пользователя из словаря и из файла"""
        if login in self.users:
            del self.users[login]
            self.save_users()
            return True
        return False

    def add_user(self, login: str, password: str) -> bool:
        """Добавление нового пользователя в словарь и в файл"""
        if login in self.users:
            return False
        else:
            hashed_password = self._hash_password(password)
            self.users[login] = hashed_password
            self.save_users()
            return True

    def check_user(self, login: str) -> bool:
        """Проверка существования пользователя в словаре"""
        return login in self.users

    def _hash_password(self, password: str) -> str:
        """Хеширование пароля. Используем SHA-256 для хэширования пароля"""
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def check_pass(self, login: str, password: str) -> bool:
        """Проверка пароля пользователя"""
        if login in self.users:
            hashed_password = self._hash_password(password)
            return self.users[login] == hashed_password
        return False


if __name__ == "__main__":
    #########
    # тесты

    AUTH_PATH = os.path.dirname(os.path.abspath(__file__)) + "/auth/users.json"
    auth = AuthUser(AUTH_PATH)

    print("Adding user test")
    auth.add_user("test", "1234")
    print("ok_test:", auth.check_user("test"))
    print("ok_test:", auth.check_pass("test", "1234"))
    print("fail_test:", auth.check_user("test1"))
    print("fail_test:", auth.check_pass("test", "12345"))

    print("Adding user test1")
    auth.add_user("test1", "12345")
    print("ok_test1:", auth.check_user("test1"))
    print("ok_test1:", auth.check_pass("test1", "12345"))
    print("fail_test1:", auth.check_pass("test1", "1234"))

    auth.save_users()
    # Загрузка пользователей из файла
    auth.load_users()
    print(auth.users)
