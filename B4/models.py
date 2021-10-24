from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


NULL_BLANK = {
    "null": True,
    "blank": True
}


class TimeModel(models.Model):
    created_at = models.DateTimeField("Дата создания", auto_now_add=True, **NULL_BLANK)
    updated_at = models.DateTimeField("Дата изменения", auto_now=True, **NULL_BLANK)

    class Meta:
        abstract = True


class DefaultDeductions(TimeModel):
    house = models.DecimalField('Жильё', default=0, max_digits=10, decimal_places=2)
    travel = models.DecimalField('Проезд', default=0, max_digits=10, decimal_places=2)
    phone = models.DecimalField('Телефон', default=0, max_digits=10, decimal_places=2)
    food = models.DecimalField('Еда', default=0, max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Стандартные вычеты'
        verbose_name_plural = 'Стандартные вычеты'

    def __str__(self):
        return f"{self.id} {self.created_at}"

    @property
    def total(self):
        return f"{self.house + self.travel + self.phone + self.food}"


class Note(TimeModel):
    text = models.TextField('Текст', **NULL_BLANK)
    image = models.ImageField('Фотоверсия', **NULL_BLANK, upload_to="foto/%Y/%m/%d")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')

    class Meta:
        verbose_name = 'Заметки'
        verbose_name_plural = 'Заметки'
        ordering = ['-created_at', '-id']

    def __str__(self):
        return f"{self.pk} {self.created_at}"


class Plan(TimeModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='plans')
    name = models.CharField('Название плана', max_length=255)

    class Meta:
        verbose_name = 'План'
        verbose_name_plural = 'Планы'
        ordering = ['-created_at', '-id']

    def __str__(self):
        return f"{self.id} {self.name}"

    def get_absolute_url(self):
        return reverse('b4:plan_detail', args=(self.id,))


class Section(TimeModel):
    name = models.CharField('Название раздела', max_length=255)
    is_active = models.BooleanField('Активный')

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'
        ordering = ['is_active', '-created_at', '-id']

    def __str__(self):
        return self.name


class AbstractTask(TimeModel):
    plan = models.ForeignKey('Plan', verbose_name='План', on_delete=models.CASCADE)
    section = models.ForeignKey('Section', verbose_name='Секция', on_delete=models.CASCADE)
    description = models.TextField('Описание')
    is_ready = models.BooleanField('Выполнено')

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.id} {self.plan} {self.section}"


class Task(AbstractTask):
    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        ordering = ['-created_at', '-id']

    def get_absolute_url(self):
        return reverse('b4:plan_detail', args=(self.plan_id,))


class DefaultTasks(AbstractTask):
    is_default = models.BooleanField('Задача по умолчанию')

    class Meta:
        verbose_name = 'Задача по умолчанию'
        verbose_name_plural = 'Задачи по умолчанию'
        ordering = ['is_default', '-created_at', '-id']
