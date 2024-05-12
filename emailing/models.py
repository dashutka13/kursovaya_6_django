from django.db import models

from config import settings

NULLABLE = {'blank': True, 'null': True}


class Messages(models.Model):
    """Модель сообщения"""
    topic = models.CharField(max_length=50, verbose_name="тема письма", null=False, blank=False, unique=True)
    body = models.TextField(max_length=500, verbose_name="тело письма", null=False, blank=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.topic

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"


class Client(models.Model):
    """Модель клиента"""
    email = models.EmailField(unique=True, verbose_name='Почта')
    full_name = models.CharField(max_length=500, verbose_name='ФИО', **NULLABLE)
    description = models.TextField(**NULLABLE, verbose_name='Описание')
    client_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                     verbose_name='Владелец')

    def __str__(self):
        """Возвращает email клиента"""
        return self.email

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'


class Emailing(models.Model):
    """Модель рассылки"""

    PERIODS = (
        ("ежедневно", "daily"),
        ("еженедельно", "weekly"),
        ("ежемесячно", "monthly"),
    )

    STATUSES = (
        ('завершена', 'завершена'),
        ('создана', 'создана'),
        ('запущена', 'запущена'),
    )

    title = models.CharField(max_length=100, verbose_name='название рассылки', unique=True, **NULLABLE)
    time_to_send = models.TimeField(verbose_name='время рассылки')
    send_periodicity = models.CharField(choices=PERIODS, verbose_name='периодичность')
    emailing_status = models.CharField(choices=STATUSES, default='создана', verbose_name='статус')
    emailing_clients = models.ManyToManyField(Client, verbose_name='клиенты')
    message = models.ForeignKey(Messages, on_delete=models.SET_NULL, **NULLABLE)
    emailing_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='владелец',
                                       null=True)
    is_published = models.BooleanField(default=True, verbose_name='опубликовано')

    def __str__(self):
        return f'Рассылка {self.subject} в {self.time_to_send} ({self.send_periodicity})'

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'
        permissions = [
            ('set_mailing_status', 'Can change the status of mailing'),
        ]


class EmailingLog(models.Model):
    """Модель статистики рассылок"""
    STATUS_ATTEMPT = (
        ('УСПЕШНО', 'УСПЕШНО'),
        ('НЕ УСПЕШНО', 'НЕ УСПЕШНО'),
    )

    created_time = models.DateTimeField(auto_now_add=True, verbose_name='дата и время последней попытки')
    log_status = models.CharField(max_length=20, choices=STATUS_ATTEMPT, verbose_name='статус попытки')
    log_emailing = models.ForeignKey(Emailing, on_delete=models.CASCADE, verbose_name='рассылка')
    response = models.TextField(**NULLABLE, verbose_name='ответ сервера')

    def __str__(self):
        return f"Статус: {self.log_status} Время: {self.created_time} Ответ сервера: {self.response}"

    class Meta:
        verbose_name = 'лог'
        verbose_name_plural = 'логи'
