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
import queue
import logging

# Определяем константу содержащую имя ОС
# для учёта особенностей данной операционной системы
import platform

OS_NAME = platform.system()

# Константы
HOST = "localhost"
PORT = 7771
CLIENT_SOCKET_TIMEOUT = 3
SERVER_SOCKET_TIMEOUT = 30
WEB_SERVER_PATH = "socket/"

REPLY_OK = b"HTTP/1.1 200 OK\n"
REPLY_ERR404 = b"HTTP/1.1 404 Not Found\n\n"
REPLY_HEADERS = b"Host: some.ru\nHost1: some1.ru\n\n"
REPLY_CUSTOM_START = b"<HTML><HEAD><TITLE>Reply from server</TITLE></HEAD><BODY>"
REPLY_CUSTOM_END = b"</BODY></HTML>"

# Единственная глобальная переменная
# доступная всем потокам
run = True

ACCESSIBLE_FILES = ["1.html", "cat.jpg"]


def is_file_accessible(raw_name):
    """
    Проверяет есть ли файл в списке доступных файлов, дотупные файлы копим в списке ACCESSIBLE_FILES
    """
    file_name = raw_name.lstrip("/")
    return file_name in ACCESSIBLE_FILES


def is_file(raw_name):
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


def send_file(file_name, conn):

    if not is_file_accessible(file_name):
        logging.error(f"нет доступа к файлу {file_name}")
        conn.send(REPLY_ERR404)
        return

    try:
        with open(WEB_SERVER_PATH + file_name.lstrip("/"), "rb") as f:
            print(f"send file {file_name}")
            conn.send(REPLY_OK)
            conn.send(REPLY_HEADERS)
            conn.send(f.read())
            logging.info(f"sent file {file_name}")

    except IOError:
        logging.error(f"нет файла {WEB_SERVER_PATH + file_name.lstrip("/")}")
        conn.send(REPLY_ERR404)
        pass


def shutdown_socket(s):
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


def reciver(client, q):
    """Поток обработки запросов, принимает данные и зовет функцию отправки"""
    try:
        # Здесь поток блокируется до тех пор
        # пока не будут считаны все имеющиеся
        # в сокете данные
        data = client.recv(1024)
        if data:  # Если есть данные
            # Отправляем в очередь сообщений кортеж
            # содержащий сокет отправителя
            # и принятые данные
            q.put((client, data))
            logging.info(
                f"{client.getpeername()} отправил: {data.decode().splitlines()[0] if data else ''}"
            )
            sender(client, data)
            q.task_done()  # Сообщаем, что сообщение обработано

    except:
        logging.info(f"Сокет {client.getpeername()} закрыт на ошибке")
        with threading.Lock():
            connections.remove(client)
        client.close()  # И закрываем клиентский сокет


def sender(client, data):
    """Функция отправки данных"""

    message = data.decode()
    ###################################
    # логика обработки запроса
    ###################################
    if message.startswith("GET"):
        # запрос по протоколу HTTP
        lines = message.split("\r")
        path = lines[0].split()[1]
        if path == "/":
            # по умолчанию отдаем главную страницу
            send_file("1.html", client)
        elif path.startswith("/test/"):
            client.send(REPLY_CUSTOM_START)
            client.send(f"<p>тест {path.split('/')[2]} запущен<p>".encode())
            client.send(REPLY_CUSTOM_END)
        elif path.startswith("/message/"):
            _, login, text = path.split("/")
            client.send(REPLY_CUSTOM_START)
            client.send(f"<p>{login} - {text}<p>".encode())
            client.send(REPLY_CUSTOM_END)
        elif is_file(path):
            send_file(path, client)
        else:
            # пришли неизвестные данные по HTTP от клиента
            logging.error(
                f"от {client.getpeername()} пришли неизвестные данные по HTTP - {path}"
            )
            client.send(REPLY_CUSTOM_START)
            client.send(f"пришли неизвестные  данные по HTTP - {path}".encode())
            client.send(REPLY_CUSTOM_END)
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
                client.send(f"{login} зарегистрирован".encode())
            else:
                client.send(
                    f"ошибка регистрации {login} - неверный пароль/логин".encode()
                )
        elif command == "signin":
            if (
                login.isalnum()
                and len(login) >= 6
                and len(password) >= 8
                and any(c.isdigit() for c in password)
            ):
                client.send(f"{login} произведен вход".encode())
            else:
                client.send(f"ошибка входа {login} - неверный пароль/логин".encode())
        else:
            client.send(
                f"пришли неизвестные  данные - {message}".encode()
            )  # Отправляем сообщение обратно

    # q.task_done()  # Сообщаем, что сообщение обработано


def accepter(server, connections, q):
    """Поток принимающий новые соединения"""
    while run:
        try:
            # Здесь поток блокируется до тех пор, пока кто-то не подключится к серверу
            client, addr = server.accept()
        except OSError as e:
            # Если отловлена не ожидаемая ошибка закрытия серверного сокета, а какая-то другая
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
            threading.Thread(target=reciver, args=(client, q)).start()
            logging.info(f"Запущен поток для {client.getpeername()}")
            # send_file("1.html", client)


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s [%(levelno)d]- %(message)s", level=logging.INFO
    )
    logging.info("Запуск...")

    # Очередь сообщений, через которую будут общаться потоки
    q = queue.Queue()
    # Множество соединений
    connections = set()

    # Ловим тут исключения если сервер закрыли принудительно и закрываем все сокеты
    try:
        server = socket.socket()
        server.bind((HOST, PORT))
        server.settimeout(SERVER_SOCKET_TIMEOUT)
        server.listen()

        # print("Сервер запущен на {}\n".format(server.getsockname()))
        logging.info(f"Сервер запущен на {server.getsockname()}")

        # # Поток получающий сообщения из очереди
        # # и отправляющий их всем сокетам в множестве connectionsget
        # threading.Thread(target=sender, args=(q, connections)).start()
        # Поток принимающий новые соединения
        threading.Thread(target=accepter, args=(server, connections, q)).start()

        while True:
            command = input("\nВведите 'exit' для завершения работы сервера\n\n")
            if command == "exit":  # Если в консоли введена команда exit
                run = False  # отменяем выполнение циклов во всех потоках
                logging.info("Завершение работы сервера")
                break  # и выходим из этого цикла

    except Exception as e:
        logging.error(f"Ошибка: {e}")
    finally:
        run = False
        for c in connections:
            shutdown_socket(c)
        shutdown_socket(server)
        logging.info("Сервер остановлен")
