"""
написать приложение-сервер используя модуль socket работающее в домашней
локальной сети.
Приложение должно принимать данные с любого устройства в сети отправленные
или через программу клиент или через браузер
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

import socket
import threading
import os
import logging
import platform
from time import sleep

from sender import Sender
from auth import AuthUser

# Определяем константу содержащую имя ОС
# для учёта особенностей данной операционной системы
OS_NAME = platform.system()

# Константы
HOST = "localhost"
PORT = 7771
CLIENT_SOCKET_TIMEOUT = 3  # секунды
SERVER_SOCKET_TIMEOUT = 5  # секунды
# путь к папке с файлами
WEB_SERVER_PATH = os.path.dirname(os.path.abspath(__file__)) + "/web/"
# WEB_SERVER_PATH = os.path.dirname(__name__) + "/"
# путь к файлу с пользователями
AUTH_PATHFILE = os.path.dirname(os.path.abspath(__file__)) + "/auth/users.json"
# файлы к которым разрешен доступ
ACCESSIBLE_FILES = [
    "default.html",
    "index.html",
    "1.html",
    "cat.jpg",
    "doc.txt",
    "favicon.ico",
]


# глобальный обьект для работы с пользователями
auth = AuthUser(AUTH_PATHFILE)
# глобальная переменная для управления потоками
run = True


def shutdown_socket(s):
    """Закрывает сокет"""
    # В Linux'ах просто закрыть заблокированный сокет будет мало,
    # он так и не выйдет из состояния блокировки. Нужно передать
    # ему команду на завершение. Но в Windows наоборот, команда
    # на завершение вызовет зависание, если сокет был заблокирован
    # вызовом accept(), а простое закрытие сработает.
    if OS_NAME == "Linux":
        # если сокет еще открыт
        try:
            if s.fileno() != -1:
                logging.info("Дополнительно для Linux, закрываем сокет")
                s.shutdown(socket.SHUT_RDWR)
            s.close()
        except:
            logging.info("Сокет уже закрыт")


def reciver(client, connections):
    """Поток обработки запросов, принимает данные и зовет функцию отправки"""

    sender = Sender(
        logging, auth, WEB_SERVER_PATH, ACCESSIBLE_FILES
    )  # создаем экземпляр класса Sender

    try:
        # Здесь поток блокируется до тех пор
        # пока не будут считаны все имеющиеся
        # в сокете данные
        data = client.recv(1024)
        if data:  # Если есть данные
            logging.info(
                f"{client.getpeername()} отправил: {data.decode().splitlines()[0] if data else ''}"
            )
            sender.process(client, data)
    except socket.timeout:
        logging.info(f"Сокет {client.getpeername()} закрыт")
    except SystemExit:
        run = False
        logging.info(f"{client.getpeername()} запросил остановку сервера")

    with threading.Lock():
        connections.remove(client)
    logging.info(f"Закончен поток для {client.getpeername()}")
    client.close()


def server_accepter():
    """Поток принимающий новые соединения на сокет сервера"""

    #
    def open_server_socket(server):
        """Открывает серверный сокет"""
        # если серверный сокет не закрыт
        if server.fileno() != -1:
            server.listen()
            server.settimeout(SERVER_SOCKET_TIMEOUT)
            logging.info(f"Сервер запущен на {server.getsockname()}")
        else:
            logging.info("Закрытие серверного сокета")

    #
    # глобальный переменная для управления потоками
    global run

    # Множество соединений
    connections = set()

    # server = socket.socket()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((HOST, PORT))
    except OSError as e:
        run = False
        logging.error(f"Ошибка привязки сокета: {e}")
        server.close()
        raise

    open_server_socket(server)
    while run:
        try:
            # Здесь поток блокируется до тех пор, пока кто-то не подключится к серверу
            client, _ = server.accept()
        except socket.timeout:
            # Если сокет закрыт по таймауту, то просто пересоздаём его
            # server.close()
            # open_server_socket(server)
            if not run:
                break
            # logging.info(f"Сервер всё еще ждет подключения...")
        except OSError as e:
            if (OS_NAME == "Windows" and e.errno != 10038) or (
                OS_NAME == "Linux" and e.errno != 22
            ):
                raise  # то возбуждаем её повторно
        else:  # Если кто-то подключился и создан новый клиентский сокет
            # Устанавливаем ему таймаут, чтобы считать его сбойным,
            # если в этот сокет не будут ничего писать
            client.settimeout(CLIENT_SOCKET_TIMEOUT)
            with threading.Lock():
                connections.add(client)
            # Запускаем новый поток, выполняющий обработку его запросов
            logging.info(f"Запущен поток для {client.getpeername()}")
            threading.Thread(target=reciver, args=(client, connections)).start()

    run = False
    for c in connections:
        shutdown_socket(c)
    shutdown_socket(server)
    logging.info("Сервер остановлен")


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s [%(levelno)d]- %(message)s", level=logging.INFO
    )
    logging.info("Запуск...")

    # Ловим тут исключения если сервер закрыли принудительно и закрываем все сокеты
    run = True
    try:
        # # Поток получающий сообщения из очереди
        # # и отправляющий их всем сокетам в множестве connectionsget
        # threading.Thread(target=sender, args=(q, connections)).start()
        # Поток принимающий новые соединения
        threading.Thread(target=server_accepter, args=()).start()
        sleep(1)  # даем время на запуск сервера

        while run:
            command = input("\nВведите 'exit' для завершения работы сервера\n\n")
            if command == "exit":  # Если в консоли введена команда exit
                run = False  # отменяем выполнение циклов во всех потоках
                logging.info("Завершение работы сервера")
                break  # и выходим из этого цикла

    except Exception as e:
        run = False
        logging.error(f"Ошибка: {e}")
        raise
