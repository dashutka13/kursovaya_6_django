# Generated by Django 5.0.2 on 2024-05-04 21:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, verbose_name='Почта')),
                ('first_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Имя')),
                ('last_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Фамилия')),
                ('surname', models.CharField(blank=True, max_length=100, null=True, verbose_name='Отчество')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Комментарий')),
                ('client_owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Владелец')),
            ],
            options={
                'verbose_name': 'клиент',
                'verbose_name_plural': 'клиенты',
            },
        ),
        migrations.CreateModel(
            name='Emailing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_to_send', models.TimeField(verbose_name='время рассылки')),
                ('send_periodicity', models.CharField(choices=[('daily', 'Ежедневная'), ('weekly', 'Раз в неделю'), ('monthly', 'Раз в месяц')], max_length=20, verbose_name='периодичность')),
                ('emailing_status', models.CharField(choices=[('started', 'Запущена'), ('created', 'Создана'), ('done', 'Завершена')], default='created', max_length=20, verbose_name='статус')),
                ('subject', models.CharField(max_length=200, verbose_name='тема письма')),
                ('body', models.TextField(verbose_name='тело письма')),
                ('emailing_clients', models.ManyToManyField(to='emailing.client', verbose_name='подписчики')),
                ('emailing_owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='владелец')),
            ],
            options={
                'verbose_name': 'рассылка',
                'verbose_name_plural': 'рассылки',
                'permissions': [('set_mailing_status', 'Can change the status of mailing')],
            },
        ),
    ]
