from django.db import models
from django.db.models import Sum


NULL_BLANK = {
    "null": True,
    "blank": True
}


class TimeModel(models.Model):
    created_at = models.DateTimeField("Дата создания", auto_now_add=True, **NULL_BLANK)
    updated_at = models.DateTimeField("Дата изменения", auto_now=True, **NULL_BLANK)

    class Meta:
        abstract = True


class StandartVichet(TimeModel):
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


class Nlg(TimeModel):
    # created_at = models.DateTimeField('Дата', default=datetime.now())
    text_nlg = models.TextField('Текст', **NULL_BLANK)
    image_nlg = models.ImageField('Фотоверсия', **NULL_BLANK, upload_to="foto/%Y/%m/%d")

    def __str__(self):
        return str(self.created_at)

    class Meta:
        verbose_name = 'Нлж'
        verbose_name_plural = 'Нлж'
        ordering = ['-created_at', '-id']


MINFIN_CHOICES = (
    (0, 'Еда'),
    (1, 'Развлечения'),
    (2, 'Проезд'),
    (3, 'Телефон'),
    (4, 'Амортизация'),
    (5, 'Прочее'),
    (6, 'НДС'),
)


class Minfin(TimeModel):
    # date_create = models.DateTimeField('Дата', default=datetime.now())
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    describe = models.CharField('Описание', max_length=255)
    type_table = models.IntegerField('Тип операции', max_length=255, choices=MINFIN_CHOICES, blank=True, null=True)

    @property
    def balance(self):
        return Minfin.objects.aggregate(balance=Sum('price')).get('balance') * -1

    def __str__(self):
        return f"{self.created_at}  {self.price} {self.describe}"

    class Meta:
        verbose_name = 'Минфин'
        verbose_name_plural = 'Минфин'
        ordering = ['-created_at', '-id']
