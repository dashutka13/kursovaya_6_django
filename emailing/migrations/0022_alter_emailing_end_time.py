# Generated by Django 5.0.2 on 2024-08-23 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emailing', '0021_alter_emailing_start_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailing',
            name='end_time',
            field=models.DateTimeField(verbose_name='Время завершения'),
        ),
    ]
