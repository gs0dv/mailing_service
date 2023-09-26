# Generated by Django 4.2.5 on 2023-09-14 11:07

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=150, verbose_name='имя')),
                ('last_name', models.CharField(max_length=150, verbose_name='фамилия')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='почта')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='комментарий')),
            ],
            options={
                'verbose_name': 'клиент',
                'verbose_name_plural': 'клиенты',
            },
        ),
        migrations.CreateModel(
            name='Mailing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_subject', models.CharField(max_length=300, verbose_name='тема сообщения')),
                ('message_boby', models.TextField(blank=True, null=True, verbose_name='тело сообщения')),
                ('mailing_time', models.TimeField(default='10:00', verbose_name='время рассылки')),
                ('period', models.CharField(choices=[('daily', 'Ежедневно'), ('weekly', 'Раз в неделю'), ('monthly', 'Раз в месяц')], max_length=20, verbose_name='периодичность рассылки')),
                ('status', models.CharField(choices=[('created', 'Создана'), ('started', 'Запущена'), ('done', 'Завершена')], default=('created', 'Создана'), max_length=20, verbose_name='статус рассылки')),
                ('date_start', models.DateField(default=django.utils.timezone.now, verbose_name='начало рассылки')),
                ('date_end', models.DateField(blank=True, null=True, verbose_name='завершение рассылки')),
            ],
            options={
                'verbose_name': 'рассылка',
                'verbose_name_plural': 'рассылки',
            },
        ),
        migrations.CreateModel(
            name='MailingLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_last_attempt', models.DateTimeField(verbose_name='дата и время последней попытки')),
                ('status', models.CharField(choices=[('ok', 'Успешно'), ('failed', 'Ошибка')], max_length=20, verbose_name='статус попытки')),
                ('error', models.TextField(blank=True, null=True, verbose_name='сообщение об ошибке')),
                ('mailing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mailings.mailing', verbose_name='рассылка')),
            ],
            options={
                'verbose_name': 'Лог',
                'verbose_name_plural': 'Логи',
            },
        ),
    ]
