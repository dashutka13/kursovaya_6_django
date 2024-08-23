# Generated by Django 5.0.2 on 2024-08-23 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emailing', '0019_alter_emailing_options_alter_emailinglog_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailing',
            name='emailing_status',
            field=models.CharField(choices=[('STATUS_DONE', 'завершена'), ('STATUS_CREATED', 'создана'), ('STATUS_STARTED', 'запущена')], default='created', verbose_name='статус'),
        ),
        migrations.AlterField(
            model_name='emailing',
            name='send_periodicity',
            field=models.CharField(choices=[('PERIOD_DAILY', 'ежедневно'), ('PERIOD_WEEKLY', 'еженедельно'), ('PERIOD_MONTHLY', 'ежемесячно')], default='Ежедневно', verbose_name='периодичность'),
        ),
    ]
