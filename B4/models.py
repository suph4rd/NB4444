from datetime import datetime
from django.db import models
from django.db.models import Sum


class StandartVichet(models.Model):
    hata = models.DecimalField('Жильё', max_digits=10, decimal_places=2)
    proezd = models.DecimalField('Проезд', max_digits=10, decimal_places=2)
    mobila = models.DecimalField('Телефон', max_digits=10, decimal_places=2)
    eda = models.DecimalField('Еда', max_digits=10, decimal_places=2)

    @property
    def itogo(self):
        return f"{self.hata + self.proezd + self.mobila + self.eda}"

    class Meta:
        verbose_name = 'Стандартные вычеты'
        verbose_name_plural = 'Стандартные вычеты'


class Nlg(models.Model):
    date_nlg = models.DateTimeField('Дата', default=datetime.now())
    text_nlg = models.TextField('Текст', blank=True, null=True)
    image_nlg = models.ImageField('Фотоверсия', blank=True, null=True, upload_to="foto/%Y/%m/%d")

    def __str__(self):
        return str(self.date_nlg)

    class Meta:
        verbose_name = 'Нлж'
        verbose_name_plural = 'Нлж'
        ordering = ['-date_nlg', '-id']


MINFIN_CHOICES = (
    (0, 'Еда'),
    (1, 'Развлечения'),
    (2, 'Проезд'),
    (3, 'Телефон'),
    (4, 'Амортизация'),
    (5, 'Прочее'),
    (6, 'НДС'),
)


class Minfin(models.Model):
    date_create = models.DateTimeField('Дата', default=datetime.now())
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    describe = models.CharField('Описание', max_length=255)
    type_table = models.IntegerField('Тип операции', max_length=255, choices=MINFIN_CHOICES, blank=True, null=True)

    @property
    def balance(self):
        return Minfin.objects.aggregate(balance=Sum('price')).get('balance') * -1

    def __str__(self):
        return f"{self.date_create}  {self.price} {self.describe}"

    class Meta:
        verbose_name = 'Минфин'
        verbose_name_plural = 'Минфин'
        ordering = ['-date_create', '-id']
