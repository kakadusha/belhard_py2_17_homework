"""
Модуль для html переменных и декораторов
"""

import functools

# заголовки
REPLY_OK = b"HTTP/1.1 200 OK\n"
REPLY_ERR404 = b"HTTP/1.1 404 Not Found\n\n"
REPLY_HEADERS = b"Host: some.ru\nHost1: some1.ru\n\n"
REPLY_CUSTOM_START = b"<HTML><HEAD><TITLE>Reply from server</TITLE></HEAD><BODY>"
REPLY_CUSTOM_END = b"</BODY></HTML>"

# html страничка
HTML_DOC_START = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{}</title>
</head>
<body>
"""
HTML_DOC_END = """
</body>
</html>
"""


def html_doc(doc_name: str):
    """
    Декоратор который оборачивает строковую функцию и делает html страничку именем doc_name
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            # получаем результат функции
            result = func(*args, **kwargs)
            # создаем html страницу
            html = HTML_DOC_START.format(doc_name) + result + HTML_DOC_END
            return html

        return wrapper

    return decorator


def html_p(func):
    """
    Декоратор который оборачивает строковую функцию в теги <p>
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # получаем результат функции
        result = func(*args, **kwargs)
        # создаем html страницу
        html = f"<p>{result}</p>"
        return html

    return wrapper


def html_h1(func):
    """
    Декоратор который оборачивает строковую функцию в теги <h1>
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # получаем результат функции
        result = func(*args, **kwargs)
        # создаем html страницу
        html = f"<h1>{result}</h1>"
        return html

    return wrapper


def html_p_red(func):
    """
    Декоратор который оборачивает строковую функцию в теги <p> красный цвет
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # получаем результат функции
        result = func(*args, **kwargs)
        # создаем html страницу
        html = f"<p style='color:red'>{result}</p>"
        return html

    return wrapper


@html_doc("Server reply")
@html_p
def gen_page(message: str) -> str:
    """
    Функция для создания сообщения
    """
    return message


@html_doc("Server bad reply")
@html_p_red
def gen_error_page(message: str) -> str:
    """
    Функция для создания сообщения с ошибкой
    """
    return message


if __name__ == "__main__":
    # тестируем декораторы и функцию

    print(gen_error_page("test error"))
