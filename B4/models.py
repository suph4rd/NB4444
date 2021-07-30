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