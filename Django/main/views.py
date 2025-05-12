"""
Методы которые будут вызваны при переходе на страницу
шаблон который будет показан при переходе на опред ссылку итд
"""

from django.shortcuts import render
from django.http import HttpResponse
from .duck_fox import get_random_duck_and_its_number, get_foxy_urls


html_config = {"admin": True, "debug": False}


# Create your views here.


# наш какой то индекс
def index(request):
    return HttpResponse("<h4>Проверка работы</h4><p>HttpResponse()</p>")


def default_page(request):
    return render(
        request,
        "main/default_page.html",
        context={
            "html_config": html_config,
        },
    )


def duck(request):
    (img_url, number) = get_random_duck_and_its_number()
    return render(
        request,
        "main/duck.html",
        context={
            "title": f"рандомная утка №{number}",
            "img_url": img_url,
            "number": number,
            "html_config": html_config,
        },
    )


def fox(request, num):
    foxes = get_foxy_urls(num, 100)
    print(foxes)
    return render(
        request,
        "main/fox.html",
        context={
            "title": f"Pандомная лиса, {num} штук",
            "foxes": foxes,
            "number": num,
            "html_config": html_config,
        },
    )


def about(request):
    return HttpResponse("<h4>Страница About</h4>")
