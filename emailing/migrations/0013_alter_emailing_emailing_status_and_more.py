# Generated by Django 5.0.2 on 2024-05-05 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emailing', '0012_alter_emailinglog_log_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailing',
            name='emailing_status',
            field=models.CharField(choices=[('READY', 'Запущена'), ('CREATED', 'Создана'), ('FINISHED', 'Завершена'), ('FINISHED_WITH_ERROR', 'Завершена с ошибкой')], default='CREATED', verbose_name='статус'),
        ),
        migrations.AlterField(
            model_name='emailing',
            name='send_periodicity',
            field=models.CharField(choices=[('DAILY', 'Ежедневная'), ('WEEKLY', 'Раз в неделю'), ('MONTHLY', 'Раз в месяц')], verbose_name='периодичность'),
        ),
    ]
