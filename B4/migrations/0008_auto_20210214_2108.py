# Generated by Django 3.0.8 on 2021-02-14 21:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('B4', '0007_auto_20210214_0836'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='standart_vichet',
            new_name='StandartVichet',
        ),
        migrations.DeleteModel(
            name='amortizatia',
        ),
        migrations.DeleteModel(
            name='eda',
        ),
        migrations.DeleteModel(
            name='nds',
        ),
        migrations.DeleteModel(
            name='prochee',
        ),
        migrations.DeleteModel(
            name='razvlechenia',
        ),
        migrations.DeleteModel(
            name='transport',
        ),
        migrations.AlterModelOptions(
            name='minfin',
            options={'ordering': ['-date_create', '-id'], 'verbose_name': 'Минфин', 'verbose_name_plural': 'Минфин'},
        ),
        migrations.RenameField(
            model_name='minfin',
            old_name='describe_minfin',
            new_name='describe',
        ),
        migrations.RenameField(
            model_name='minfin',
            old_name='ostatoc_minfin',
            new_name='price',
        ),
        migrations.RemoveField(
            model_name='minfin',
            name='date_minfin',
        ),
        migrations.RemoveField(
            model_name='minfin',
            name='id_insert',
        ),
        migrations.RemoveField(
            model_name='minfin',
            name='sum_minfin',
        ),
        migrations.AddField(
            model_name='minfin',
            name='date_create',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 14, 21, 8, 21, 920815), verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='minfin',
            name='type_table',
            field=models.IntegerField(blank=True, choices=[(0, 'Еда'), (1, 'Развлечения'), (2, 'Проезд'), (3, 'Телефон'), (4, 'Амортизация'), (5, 'Прочее'), (6, 'НДС')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='nlg',
            name='date_nlg',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 14, 21, 8, 21, 920134), verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='nlg',
            name='image_nlg',
            field=models.ImageField(blank=True, null=True, upload_to='foto/%Y/%m/%d', verbose_name='Фотоверсия'),
        ),
    ]
