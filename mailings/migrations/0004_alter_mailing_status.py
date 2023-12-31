# Generated by Django 4.2.5 on 2023-09-14 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailings', '0003_alter_mailing_period_alter_mailing_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailing',
            name='status',
            field=models.CharField(choices=[('Создана', 'Создана'), ('Запущена', 'Запущена'), ('Завершена', 'Завершена')], default='Создана', max_length=40, verbose_name='статус рассылки'),
        ),
    ]
