from typing import Any
from django.shortcuts import render, HttpResponse
from .models import Student

# Create your views here.

from django.views.generic import ListView, DetailView


def index(r):
    # return HttpResponse("<h1>Академия Ы</h1>")
    return render(r, "base.html")


def students(r):
    students = Student.objects.all()
    return render(r, "students.html", context={"students": students})


def student(r, id):
    student = Student.objects.get(id=id)
    return render(r, "student.html", context={"student": student})


menu = {
    "aaa": ",mmm",
    "ddd": "frftgtggb",
}


class StudentsView(ListView):
    model = Student
    template_name = "students.html"
    context_object_name = "students"

    def get_context_data(self, **kwargs):
        cc = super().get_context_data(**kwargs)
        cc["nemu"] = menu
        return cc


class StudentView(DetailView):
    model = Student
    template_name = "students.html"
    context_object_name = "students"
    pk_url_kwarg = "pk"
