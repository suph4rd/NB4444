from datetime import datetime

from django.db import models

class standart_vichet(models.Model):
    hata = models.FloatField(max_length=255)
    proezd = models.FloatField(max_length=255)
    mobila = models.FloatField(max_length=255)
    eda = models.FloatField(max_length=255)
    itogo = models.FloatField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = 'Стандартные вычеты'
        verbose_name_plural = 'Стандартные вычеты'


class nlg(models.Model):
    date_nlg = models.DateTimeField(verbose_name='Дата', default=datetime.now())
    text_nlg = models.TextField(verbose_name='Текст', blank=True)
    image_nlg = models.ImageField(blank=True, upload_to="foto\%Y\%m\%d", verbose_name='Фотоверсия')

    def __str__(self):
        return str(self.date_nlg)

    class Meta:
        verbose_name = 'Нлж'
        verbose_name_plural = 'Нлж'
        ordering = ['-date_nlg', '-id']


class minfin(models.Model):
    date_minfin = models.DateTimeField(verbose_name='Дата', default=datetime.now())
    ostatoc_minfin = models.FloatField()
    sum_minfin = models.FloatField()
    describe_minfin = models.CharField(max_length=255)
    type_table = models.CharField(max_length=255, blank=True, null=True)
    id_insert = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.ostatoc_minfin

    class Meta:
        verbose_name = 'Минфин'
        verbose_name_plural = 'Минфин'
        ordering = ['-date_minfin', '-id']


class eda(models.Model):
    date_eda = models.DateTimeField(verbose_name='Дата', default=datetime.now())
    ostatoc_eda = models.CharField(max_length=255, blank=True)
    sum_eda = models.CharField(max_length=255)
    describe_eda = models.CharField(max_length=255)

    def __str__(self):
        return self.ostatoc_eda

    class Meta:
        verbose_name = 'Еда'
        verbose_name_plural = 'Еда'
        ordering = ['-date_eda', '-id']


class transport(models.Model):
    date_transport = models.DateTimeField(verbose_name='Дата', default=datetime.now())
    ostatoc_transport = models.CharField(max_length=255, blank=True)
    sum_transport = models.CharField(max_length=255)
    describe_transport = models.CharField(max_length=255)

    def __str__(self):
        return self.ostatoc_transport

    class Meta:
        verbose_name = 'Транспорт'
        verbose_name_plural = 'Транспорт'
        ordering = ['-date_transport', '-id']


class razvlechenia(models.Model):
    date_razvlechenia = models.DateTimeField(verbose_name='Дата', default=datetime.now())
    ostatoc_razvlechenia = models.CharField(max_length=255, blank=True)
    sum_razvlechenia = models.CharField(max_length=255)
    describe_razvlechenia = models.CharField(max_length=255)

    def __str__(self):
        return self.ostatoc_razvlechenia

    class Meta:
        verbose_name = 'Развлечения'
        verbose_name_plural = 'Развлечения'
        ordering = ['-date_razvlechenia', '-id']


class amortizatia(models.Model):
    date_amortizatia = models.DateTimeField(verbose_name='Дата', default=datetime.now())
    ostatoc_amortizatia = models.CharField(max_length=255, blank=True)
    sum_amortizatia = models.CharField(max_length=255)
    describe_amortizatia = models.CharField(max_length=255)

    def __str__(self):
        return self.ostatoc_amortizatia

    class Meta:
        verbose_name = 'Амортизация'
        verbose_name_plural = 'Амортизация'
        ordering = ['-date_amortizatia', '-id']


class prochee(models.Model):
    date_prochee = models.DateTimeField(verbose_name='Дата', default=datetime.now())
    ostatoc_prochee = models.CharField(max_length=255, blank=True)
    sum_prochee = models.CharField(max_length=255)
    describe_prochee = models.CharField(max_length=255)

    def __str__(self):
        return self.ostatoc_prochee

    class Meta:
        verbose_name = 'Прочее'
        verbose_name_plural = 'Прочее'
        ordering = ['-date_prochee', '-id']


class nds(models.Model):
    date_nds = models.DateTimeField(verbose_name='Дата', default=datetime.now())
    ostatoc_nds = models.FloatField()
    sum_nds = models.FloatField()
    describe_nds = models.CharField(max_length=255)
    type_table = models.CharField(max_length=255, blank=True, null=True, default='НДС')
    id_insert = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.ostatoc_nds

    class Meta:
        verbose_name = 'Ндс'
        verbose_name_plural = 'Ндс'
        ordering = ['-date_nds', '-id']