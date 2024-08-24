from django.db import models

from config import settings

NULLABLE = {'blank': True, 'null': True}


class Messages(models.Model):
    """Модель сообщения"""
    topic = models.CharField(max_length=50, verbose_name="тема письма", null=False, blank=False, unique=True)
    body = models.TextField(verbose_name="тело письма", null=False, blank=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name="Владелец")

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
        return f'{self.full_name} - {self.email}'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'


class Emailing(models.Model):
    """Модель рассылки"""
    PERIOD_DAILY = "Ежедневно"
    PERIOD_WEEKLY = "weekly"
    PERIOD_MONTHLY = "monthly"

    PERIODS = (
        ("PERIOD_DAILY", "ежедневно"),
        ("PERIOD_WEEKLY", "еженедельно"),
        ("PERIOD_MONTHLY", "ежемесячно"),
    )

    STATUS_CREATED = "created"
    STATUS_STARTED = "started"
    STATUS_DONE = "done"

    STATUSES = (
        ('STATUS_DONE', 'завершена'),
        ('STATUS_CREATED', 'создана'),
        ('STATUS_STARTED', 'запущена'),
    )

    title = models.CharField(max_length=100, verbose_name='название рассылки', unique=True, **NULLABLE)
    start_time = models.DateTimeField(verbose_name="Время начала")
    end_time = models.DateTimeField(verbose_name="Время завершения", **NULLABLE)
    send_periodicity = models.CharField(choices=PERIODS, default=PERIOD_DAILY, verbose_name='периодичность')
    emailing_status = models.CharField(choices=STATUSES, default=STATUS_CREATED, verbose_name='статус')
    emailing_clients = models.ManyToManyField(Client, related_name="mailing_settings", verbose_name='клиенты')
    message = models.ForeignKey(Messages, on_delete=models.SET_NULL, **NULLABLE)
    emailing_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='владелец',
                                       null=True)
    is_active = models.BooleanField(default=True, verbose_name="статус активности")

    def __str__(self):
        return f'Рассылка {self.title} в {self.start_time} ({self.send_periodicity})'

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'
        permissions = [
            ("switch_status", "изменение статуса"),
            ("view_mailing", "отображать рассылки")
        ]


class EmailingLog(models.Model):
    """Модель статистики рассылок"""
    STATUS_OK = "ok"
    STATUS_FAILED = "failed"

    STATUS_ATTEMPT = (
        ('STATUS_OK', 'УСПЕШНО'),
        ('STATUS_FAILED', 'НЕ УСПЕШНО'),
    )

    last_try = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата последней попытки", **NULLABLE
    )
    client = models.ForeignKey(
        Client, on_delete=models.SET_NULL, verbose_name="Клиент", **NULLABLE
    )
    settings = models.ForeignKey(
        Emailing, on_delete=models.SET_NULL, verbose_name="Настройки", **NULLABLE
    )

    log_status = models.CharField(max_length=20, choices=STATUS_ATTEMPT, default=STATUS_OK,
                                  verbose_name='статус попытки')
    response = models.CharField(max_length=350, **NULLABLE, verbose_name='ответ сервера')

    class Meta:
        verbose_name = 'попытка рассылки'
        verbose_name_plural = 'попытки рассылки'
