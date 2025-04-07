"""

написать приложение-клиент используя модуль socket работающее в домашней
локальной сети.
Приложение должно соединятся с сервером по известному адрес:порт и отправлять
туда текстовые данные.

известно что сервер принимает данные следующего формата:
    "command:reg; login:<login>; password:<pass>" - для регистрации пользователя
    "command:signin; login:<login>; password:<pass>" - для входа пользователя


"""

import socket


def get_user_command():
    """Функция для получения команды от пользователя"""
    command = input("\nВведите команду (1 - регистрация, 2 - вход, 0 - выход):> ")
    return command


def server_transaction(text):
    """Функция для обработки транзакции с сервером"""
    server_address = ("localhost", 7771)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(server_address)
    client.sendall(text.encode())
    response = client.recv(1024)
    client.close()
    return response.decode()


if __name__ == "__main__":
    # Создание сокета
    # client_socket = socket.socket()

    print(
        "Внимание! Пароли пересылаются в открытом виде, необходим защищенный канал связи!"
    )

    try:
        while True:
            menu = get_user_command()

            if menu == "1":
                login = input(
                    "Введите логин (только латинские символы и цифры, минимум 6 символов): "
                )
                password = input("Введите пароль (не менее 8 символов, с цифрой): ")
                command = f"command:reg; login:{login}; password:{password}"
                print("Ответ от сервера:", server_transaction(command))

            elif menu == "2":
                login = input("Введите логин: ")
                password = input("Введите пароль: ")
                command = f"command:signin; login:{login}; password:{password}"
                print("Ответ от сервера:", server_transaction(command))

            elif menu == "0":
                print("Выход из программы.")
                break

            else:
                print("Неверная команда. Попробуйте снова.")

    except KeyboardInterrupt:
        print("Выход из программы.")
