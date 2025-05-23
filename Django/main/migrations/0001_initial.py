# Generated by Django 5.2.1 on 2025-05-13 11:26

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('py', 'Python'), ('js', 'JavaScript'), ('c', 'C++'), ('an', 'Android')], max_length=20, verbose_name='Курс')),
                ('course_num', models.SmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)], verbose_name='Номер курса')),
                ('start_date', models.DateField(null=True, verbose_name='Начало курса')),
                ('end_date', models.DateField(null=True, verbose_name='Окончание курса')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Курс',
                'verbose_name_plural': 'Курсы',
                'ordering': ['name', 'course_num'],
                'unique_together': {('name', 'course_num')},
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Имя')),
                ('surname', models.CharField(max_length=30, verbose_name='Фамилия')),
                ('age', models.SmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(18), django.core.validators.MaxValueValidator(99)], verbose_name='Возраст')),
                ('sex', models.CharField(choices=[('m', 'Мужчина'), ('f', 'Женщина')], max_length=10, verbose_name='Пол')),
                ('active', models.BooleanField(verbose_name='Активный')),
                ('photo', models.ImageField(blank=True, upload_to='phontos/%Y/%m/%d', verbose_name='Фото')),
                ('slug', models.SlugField(help_text='только латинские', max_length=255, unique=True, verbose_name='URL')),
                ('time_create', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Время создания')),
                ('time_update', models.DateTimeField(auto_now=True, null=True, verbose_name='Время изменения')),
                ('course', models.ManyToManyField(blank=True, to='main.course', verbose_name='Посещаемые курсы')),
            ],
            options={
                'verbose_name': 'Студент',
                'verbose_name_plural': 'Студенты',
                'ordering': ['surname'],
            },
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Оценка')),
                ('date', models.DateField(null=True, verbose_name='Дата оценки')),
                ('date_add', models.DateField(auto_now_add=True, null=True, verbose_name='Дата добавления')),
                ('date_update', models.DateField(auto_now=True, null=True, verbose_name='Дата изменения')),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.course', verbose_name='Курс')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grades', to='main.student', verbose_name='Чья оценка')),
            ],
            options={
                'verbose_name': 'Оценка',
                'verbose_name_plural': 'Оценки',
            },
        ),
        migrations.AddIndex(
            model_name='student',
            index=models.Index(fields=['surname'], name='main_studen_surname_307540_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='student',
            unique_together={('name', 'surname')},
        ),
    ]
