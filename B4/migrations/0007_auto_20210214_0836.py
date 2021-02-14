# Generated by Django 3.0.8 on 2021-02-14 08:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('B4', '0006_auto_20210214_0824'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='standart_vichet',
            name='itogo',
        ),
        migrations.AlterField(
            model_name='amortizatia',
            name='date_amortizatia',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 14, 8, 36, 43, 650893), verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='eda',
            name='date_eda',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 14, 8, 36, 43, 649111), verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='minfin',
            name='date_minfin',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 14, 8, 36, 43, 648524), verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='nds',
            name='date_nds',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 14, 8, 36, 43, 651908), verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='prochee',
            name='date_prochee',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 14, 8, 36, 43, 651401), verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='razvlechenia',
            name='date_razvlechenia',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 14, 8, 36, 43, 650323), verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='standart_vichet',
            name='eda',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='standart_vichet',
            name='hata',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='standart_vichet',
            name='mobila',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='standart_vichet',
            name='proezd',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='transport',
            name='date_transport',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 14, 8, 36, 43, 649804), verbose_name='Дата'),
        ),
    ]
