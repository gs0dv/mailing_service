from django.contrib import admin

from mailings.models import Mailing, Client, MailingLog

admin.site.register(Client)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'message_subject', 'mailing_time', 'period', 'status', 'date_start', 'date_end')


@admin.register(MailingLog)
class MailingLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_last_attempt', 'status', 'mailing_id', 'mailing', 'error')
