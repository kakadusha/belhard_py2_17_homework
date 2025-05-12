from django.contrib import admin
from .models import Student

# Register your models here.

# admin.site.register(Student)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("id", "surname", "name", "sex", "average_grade", "average_grade2")
    search_fields = ("name", "surname", "average_grade")
    list_filter = ("sex", "active")

    def short_name(self, obj):
        return f"{obj.surname} {obj.name[0]}."

    def average_grade(self, obj):
        gs = [g for g in range(obj.id, 10)]
        return str((sum(gs) / 10)) + obj.surname

    def average_grade2(self, obj):
        from django.db.models import Avg

        res = Student.objects.filter(name=obj.name).aggregate(Avg("age", default=0))
        return res  # ["grade__avg"]

    short_name.short_discripton = "Короткое имя"
