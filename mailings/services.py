from datetime import datetime

from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail

from mailings.models import Mailing
from background_task.models import Task, CompletedTask
from mailings.tasks import my_scheduled_task, set_status_running, set_status_done

active_user = None


def create_task_mailing(created_object):
    created_object.status = 'Создана'
    created_object.save()

    periods = {
        'Ежедневно': 86400,
        'Раз в неделю': 604800,
        'Раз в месяц': 2419200
    }
    repeat = periods[created_object.period]

    date_start = datetime(
        year=created_object.date_start.year,
        month=created_object.date_start.month,
        day=created_object.date_start.day,
        hour=created_object.mailing_time.hour,
        minute=created_object.mailing_time.minute,
        second=created_object.mailing_time.second
    )

    # date_start = datetime(
    #     year=2023,
    #     month=9,
    #     day=21,
    #     hour=18,
    #     minute=58,
    #     second=0
    # )

    if created_object.date_end:
        date_end = datetime(
            year=created_object.date_end.year,
            month=created_object.date_end.month,
            day=created_object.date_end.day,
            hour=created_object.mailing_time.hour,
            minute=created_object.mailing_time.minute,
            second=created_object.mailing_time.second
        )

        # date_end = datetime(
        #     year=2023,
        #     month=9,
        #     day=21,
        #     hour=18,
        #     minute=59,
        #     second=0
        # )

        my_scheduled_task(created_object.pk, schedule=date_start, repeat=repeat, repeat_until=date_end)
        set_status_done(created_object.pk, schedule=date_end)
    else:
        my_scheduled_task(created_object.pk, schedule=date_start, repeat=repeat)

    set_status_running(created_object.pk, schedule=date_start)


def delete_task_mailing(pk):
    Task.objects.filter(task_params=f'[[{pk}], {{}}]').delete()
    CompletedTask.objects.filter(task_params=f'[[{pk}], {{}}]').delete()


def set_active_user(user):
    global active_user
    active_user = user


def get_active_user():
    return active_user


def get_caches_object(mailing_pk):
    if settings.CACHE_ENABLED:
        key = 'mailing'
        returned_object = cache.get(key)
        if returned_object is None:
            returned_object = Mailing.objects.get(pk=mailing_pk)
            cache.set(key, returned_object)
    else:
        returned_object = Mailing.objects.get(pk=mailing_pk)

    return returned_object
