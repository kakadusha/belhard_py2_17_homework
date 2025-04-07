"""
Обект Sender отвечает за отправку данных клиенту

    - если данные пришли по протоколу http создать возможность след.логики:
        - если путь "/" - вывести главную страницу

        - если путь содержит /test/<int>/ вывести сообщение - тест с номером int запущен

        - если путь содержит message/<login>/<text>/ вывести в консоль/браузер сообщение
            "{дата время} - сообщение от пользователя {login} - {text}"

        - если путь содержит указание на файл вывести в браузер этот файл

        - во всех остальных случаях вывести сообщение:
            "пришли неизвестные  данные по HTTP - путь такой то"


    - если данные пришли НЕ по протоколу http создать возможность след.логики:
        - если пришла строка формата "command:reg; login:<login>; password:<pass>"
            - выполнить проверку:
                login - только латинские символы и цифры, минимум 6 символов
                password - минимум 8 символов, должны быть хоть 1 цифра
            - при успешной проверке:
                1. вывести сообщение на стороне клиента:
                    "{дата время} - пользователь {login} зарегистрирован"
                2. добавить данные пользователя в список/словарь на сервере
            - если проверка не прошла вывести сообщение на стороне клиента:
                "{дата время} - ошибка регистрации {login} - неверный пароль/логин"

        - если пришла строка формата "command:signin; login:<login>; password:<pass>"
            выполнить проверку зарегистрирован ли такой пользователь на сервере:

            при успешной проверке:
                1. вывести сообщение на стороне клиента:
                    "{дата время} - пользователь {login} произведен вход"

            если проверка не прошла вывести сообщение на стороне клиента:
                "{дата время} - ошибка входа {login} - неверный пароль/логин"

        - во всех остальных случаях вывести сообщение на стороне клиента:
            "пришли неизвестные  данные - <присланные данные>"

"""

import datetime

from html_staff import (
    REPLY_CUSTOM_END,
    REPLY_CUSTOM_START,
    REPLY_OK,
    REPLY_ERR404,
    REPLY_HEADERS,
    gen_error_page,
    gen_page,
)


class Sender:
    """Класс для работы с пользователями сервера"""

    def __init__(self, logging, auth, web_server_path, accessible_files):
        self.logging = logging
        self.accessible_files = accessible_files
        self.run = True
        self.web_server_path = web_server_path
        self.auth = auth

    def _is_file_accessible(self, raw_name) -> bool:
        """
        Проверяет есть ли файл в списке доступных файлов, дотупные файлы копим в списке ACCESSIBLE_FILES
        """
        file_name = raw_name.lstrip("/")
        return file_name in self.accessible_files

    def _is_file(self, raw_name) -> bool:
        """
        Проверяет является ли файлом запрашиваемый путь
        """
        name = raw_name.lower().strip("/")
        if name[-4:] in [".jpg", ".png", ".gif", ".ico", ".txt"] or name[-5:] in [
            ".html",
            ".json",
        ]:
            return True
        return False

    def send_file(self, file_name, conn) -> None:
        """Отправляет файл клиенту"""
        if not self._is_file_accessible(file_name):
            self.logging.error(f"нет доступа к файлу {file_name}")
            conn.send(REPLY_ERR404)
            return

        try:
            with open(self.web_server_path + file_name.lstrip("/"), "rb") as f:
                conn.send(REPLY_OK)
                conn.send(REPLY_HEADERS)
                conn.send(f.read())
                self.logging.info(f"sent file {file_name}")

        except IOError:
            self.logging.error(
                f"нет файла {self.web_server_path + file_name.lstrip("/")}"
            )
            conn.send(REPLY_ERR404)
            pass

    def _send_error(self, client, bad_data) -> None:
        """Отправляет ошибку клиенту"""
        client.send(REPLY_OK)
        client.send(REPLY_HEADERS)
        client.send(
            gen_error_page(f"пришли неизвестные  данные по HTTP - {bad_data}").encode()
        )
        self.logging.error(
            f"от {client.getpeername()} пришли неизвестные данные по HTTP - {bad_data}"
        )

    def _is_http(self, message: str) -> bool:
        """начинается с get и содержит HTTP/"""
        return message.startswith("GET") and "HTTP/" in message

    def process(self, client, data):
        """Функция отправки данных
        принимает данные от клиента и отправляет ответ
        client - сокет клиента
        data - данные от клиента

        Если запросили остановку сервера, то бросает исключение
        SystemExit, которое обрабатывается в основном потоке
        """

        message = data.decode()

        ##########################
        # логика обработки запроса
        ##########################
        if self._is_http(message):
            # запрос по протоколу HTTP
            lines = message.split("\r")
            path = lines[0].split()[1]
            if path == "/":
                # по умолчанию отдаем главную страницу
                self.send_file("default.html", client)
            elif path.startswith("/test/"):
                client.send(REPLY_OK)
                client.send(REPLY_HEADERS)
                client.send(
                    gen_page(f"тест с номером {path.split('/')[2]} запущен").encode()
                )
            elif path.startswith("/message/"):
                try:
                    parsed = path.split("/")
                    login, text = parsed[2], parsed[3]
                except IndexError:
                    self._send_error(client, path)
                    return

                date_time_now_str = datetime.datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                client.send(REPLY_OK)
                client.send(REPLY_HEADERS)
                client.send(
                    gen_page(
                        f"{date_time_now_str} - сообщение от пользователя {login} - {text}"
                    ).encode()
                )
            elif path.startswith("/exit/"):
                client.send(REPLY_OK)
                client.send(REPLY_HEADERS)
                client.send(gen_error_page("Stopping server").encode())
                self.logging.info("Завершение работы сервера по команде клиента")
                raise SystemExit
            elif self._is_file(path):
                self.send_file(path, client)
            else:
                # пришли неизвестные данные по HTTP от клиента
                self._send_error(client, path)
                return

        else:
            # запрос не по протоколу HTTP
            command, login, password = message.split(";")
            command = command.split(":")[1]
            login = login.split(":")[1]
            password = password.split(":")[1]
            if command == "reg":
                if (
                    login.isalnum()
                    and len(login) >= 6
                    and len(password) >= 8
                    and any(c.isdigit() for c in password)
                ):
                    if self.auth.add_user(login, password):
                        client.send(f"{login} зарегистрирован".encode())
                    else:
                        client.send(
                            f"ошибка регистрации {login} - пользователь уже существует".encode()
                        )
                else:
                    client.send(
                        f"ошибка регистрации {login} - неверный пароль/логин".encode()
                    )
            elif command == "signin":
                is_login_ok = self.auth.check_user(login)
                is_pass_ok = self.auth.check_pass(login, password)
                if is_login_ok and is_pass_ok:
                    client.send(f"{login} произведен вход".encode())
                else:
                    client.send(
                        f"ошибка входа {login} - неверный пароль({is_login_ok})/логин({is_pass_ok})".encode()
                    )
            else:

                # пришли неизвестные данные по HTTP от клиента
                self._send_error(client, message)
                return
