import socket
import threading
import queue

# Определяем константу содержащую имя ОС
# для учёта особенностей данной операционной системы
import platform

OS_NAME = platform.system()

# Константы
HOST = "localhost"
PORT = 7733

OK = b"HTTP/1.1 200 OK\n"
HEADERS = b"Host: some.ru\nHost1: some1.ru\n\n"
ERR_404 = b"HTTP/1.1 404 Not Found\n\n"

# Единственная глобальная переменная
# доступная всем потокам
run = True

IAMFILE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>

    <h1> HELLO 123</h1>
    <p> Hello first page </p>

    <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTU62Md2yC4lIg8Mt_ZUGEVBaoXR7apfYbWbQ&s" alt="123">

    <br>
    <img src="cat1.jpg" alt="12345">

    <br>
    <!-- эта картинка из папки проекта -->
     <!-- так как сервер умеет отдавать файлы она подгружается автоматически -->
    <img src="cat.jpg" alt="12345" width=200 height="200">
</body>
</html>
"""


def send_file(file_name, conn):
    try:
        # with open(file_name.lstrip("/"), "rb") as f:
        #     print(f"send file {file_name}")
        #     conn.send(OK)
        #     conn.send(HEADERS)
        #     conn.send(f.read())
        print(f"send file file_name")
        conn.send(OK)
        conn.send(HEADERS)
        conn.send(IAMFILE.encode())

    except IOError:
        print("нет файла")
        conn.send(ERR_404)


def shutdown_socket(s):
    # В Linux'ах просто закрыть заблокированный сокет будет мало,
    # он так и не выйдет из состояния блокировки. Нужно передать
    # ему команду на завершение. Но в Windows наоборот, команда
    # на завершение вызовет зависание, если сокет был заблокирован
    # вызовом accept(), а простое закрытие сработает.
    if OS_NAME == "Linux":
        s.shutdown(socket.SHUT_RDWR)
    s.close()


def reciver(client, q):
    while run:
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
                print("{} отправил: {}".format(client.getpeername(), data.decode()))
        except:
            break  # В случае ошибки выходим из цикла
    client.close()  # И закрываем клиентский сокет


def sender(q, connections):
    while run:
        closed_sockets = set()
        try:
            # Получаем из очереди сообщений
            # сокет отправителя и принятые данные
            sender, message = q.get(timeout=1)
        except queue.Empty:
            pass  # Игнорируем отсутствие сообщений в очереди
        else:  # Если же сообщения есть
            for s in set(connections):  # Обходим все сокеты
                if s != sender:  # Кроме сокета отправителя
                    try:
                        s.send(message)  # И отправляем им принятое сообщение
                    except:
                        closed_sockets.add(s)
            if closed_sockets:
                with threading.Lock():
                    connections -= closed_sockets
                print("Подключено (sender):", len(connections))
            q.task_done()  # Сообщаем, что сообщение обработано


def accepter(server, connections, q):
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
            # если в этот сокет не будут ничего писать более 5 минут
            client.settimeout(60 * 5)
            with threading.Lock():
                connections.add(client)
            # Запускаем новый поток, выполняющий функцию receiver
            # для только что полученного сокета
            threading.Thread(target=reciver, args=(client, q)).start()
            print("Подключено (accepter):", len(connections))
            send_file("1.html", client)


if __name__ == "__main__":
    print("Запуск...")

    # Очередь сообщений, через которую будут общаться потоки
    q = queue.Queue()
    # Множество соединений
    connections = set()

    server = socket.socket()
    server.bind((HOST, PORT))
    server.listen()

    print("Сервер запущен на {}\n".format(server.getsockname()))

    # Поток получающий сообщения из очереди
    # и отправляющий их всем сокетам в множестве connections
    threading.Thread(target=sender, args=(q, connections)).start()
    # Поток принимающий новые соединения
    threading.Thread(target=accepter, args=(server, connections, q)).start()

    while True:
        command = input()
        if command == "exit":  # Если в консоли введена команда exit
            run = False  # отменяем выполнение циклов во всех потоках
            break  # и выходим из этого цикла
    for s in connections:
        shutdown_socket(s)
    shutdown_socket(server)
