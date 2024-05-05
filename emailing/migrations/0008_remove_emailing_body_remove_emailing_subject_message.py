# Generated by Django 5.0.2 on 2024-05-05 10:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emailing', '0007_alter_emailing_emailing_clients_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emailing',
            name='body',
        ),
        migrations.RemoveField(
            model_name='emailing',
            name='subject',
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=50, unique=True, verbose_name='тема письма')),
                ('body', models.TextField(max_length=500, verbose_name='тело письма')),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Сообщение',
                'verbose_name_plural': 'Сообщения',
            },
        ),
    ]