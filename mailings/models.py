from django.conf import settings
from django.db import models
from django.utils.timezone import now

NULLABLE = {
    'blank': True,
    'null': True
}


class Client(models.Model):
    first_name = models.CharField(max_length=150, verbose_name='имя')
    last_name = models.CharField(max_length=150, verbose_name='фамилия')
    email = models.EmailField(unique=True, verbose_name='почта')
    comment = models.TextField(verbose_name='комментарий', **NULLABLE)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='владелец')

    def __str__(self):
        return f'{self.email} ({self.first_name} {self.last_name})'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'


class Mailing(models.Model):
    PERIOD_DAILY = 'Ежедневно'
    PERIOD_WEEKLY = 'Раз в неделю'
    PERIOD_MONTHLY = 'Раз в месяц'

    PERIODS = (
        (PERIOD_DAILY, 'Ежедневно'),
        (PERIOD_WEEKLY, 'Раз в неделю'),
        (PERIOD_MONTHLY, 'Раз в месяц'),
    )

    STATUS_CREATED = 'Создана'
    STATUS_STARTED = 'Запущена'
    STATUS_DONE = 'Завершена'

    STATUSES = (
        (STATUS_CREATED, 'Создана'),
        (STATUS_STARTED, 'Запущена'),
        (STATUS_DONE, 'Завершена'),
    )

    message_subject = models.CharField(max_length=300, verbose_name='тема сообщения')
    message_boby = models.TextField(verbose_name='тело сообщения', **NULLABLE)

    mailing_time = models.TimeField(default='10:00', verbose_name='время рассылки')
    period = models.CharField(max_length=40, choices=PERIODS, verbose_name='периодичность рассылки')
    status = models.CharField(max_length=40, choices=STATUSES, default=STATUS_CREATED,
                              verbose_name='статус рассылки')
    date_start = models.DateField(default=now, verbose_name='начало рассылки')
    date_end = models.DateField(verbose_name='завершение рассылки', **NULLABLE)

    clients = models.ManyToManyField(Client, verbose_name='клиенты')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='владелец')

    def __str__(self):
        return self.message_subject

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'


class MailingLog(models.Model):
    date_last_attempt = models.DateTimeField(verbose_name='дата и время последней попытки')
    status = models.BooleanField(max_length=20, verbose_name='статус попытки')

    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='рассылка')
    error = models.TextField(verbose_name='сообщение об ошибке', **NULLABLE)

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'
