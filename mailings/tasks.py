from datetime import datetime

from background_task import background
from django.conf import settings
from django.core.mail import send_mail

from mailings.models import Mailing, MailingLog


@background
def my_scheduled_task(mailing_pk):
    mailing = Mailing.objects.get(pk=mailing_pk)
    clients = [client.email for client in mailing.clients.all()]
    status = None
    error = 'no error'

    print('create mailing', mailing.message_subject)

    try:
        status = True
        send_mail(
            subject=mailing.message_subject,
            message=mailing.message_boby,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=clients,
            fail_silently=False
        )
    except Exception as exception:
        status = False
        error = exception
    finally:
        mailing_pk = str(mailing_pk)
        mailing_log = MailingLog.objects.create(
            date_last_attempt=datetime.now(),
            status=status,
            mailing_id=mailing_pk,
            error=error
        )
        mailing_log.save()


@background
def set_status_running(mailing_pk):
    mailing = Mailing.objects.get(pk=mailing_pk)
    mailing.status = 'Запущена'
    mailing.save()


@background
def set_status_done(mailing_pk):
    mailing = Mailing.objects.get(pk=mailing_pk)
    mailing.status = 'Завершена'
    mailing.save()
