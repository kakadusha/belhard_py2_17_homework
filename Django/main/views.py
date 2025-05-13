"""
Методы которые будут вызваны при переходе на страницу
шаблон который будет показан при переходе на опред ссылку итд
"""

from django.shortcuts import render
from django.http import HttpResponse
from django.db.models.query import QuerySet
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .duck_fox import get_random_duck_and_its_number, get_foxy_urls
from .models import Student


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


def students(request):
    students = Student.objects.all()
    return render(request, "main/students.html", context={"students": students})


# на уроке не работала т.к. я был авторизован как админ 😂
# @login_required(login_url='/login/')
def student(request, id):
    student = Student.objects.get(id=id)
    return render(request, "main/student.html", context={"student": student})


my_menu = [
    {"menu1": "url1"},
    {"menu2": "url2"},
]


class StudentsView(ListView):
    model = Student
    template_name = "main/students.html"
    context_object_name = "students"

    # для уточнения запроса если нет def get
    # def get_queryset(self) -> QuerySet[Any]:
    #     return Student.objects.filter(name='Вася')

    # для добавления в контекст доп данных если нет def get
    # def get_context_data(self, **kwargs) -> dict[str, Any]:
    #     context =  super().get_context_data(**kwargs)
    #     context['menu'] = menu
    #     return context

    # ---------------------------------------
    # http://127.0.0.1:8000/students2/?f=ася
    def get(self, request, *args, **kwargs):
        f = request.GET.get("f", default="")
        print(f)
        students = Student.objects.filter(name__contains=f).all()
        return render(
            request, self.template_name, context={"students": students, "menu": my_menu}
        )


class StudentView(LoginRequiredMixin, DetailView):
    model = Student
    template_name = "main/student.html"
    slug_url_kwarg = "name_slug"
    context_object_name = "student"
    # pk_url_kwarg = 'pk' # т.к. тут slug ссылка по id уже не нужна
    login_url = "/login/"


def login(request):
    return HttpResponse("<h1> ЛОГИН </h1>")
