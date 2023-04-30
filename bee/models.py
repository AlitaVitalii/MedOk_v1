import uuid
from datetime import date

from django.db import models
from django.urls import reverse


# Create your models here.


class Row(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('row_detail', args=[str(self.pk)])


class Queen(models.Model):
    #  Пчелиная матка
    year = models.IntegerField('Год рождения')
    title = models.CharField('Порода', max_length=100)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-year']

    def __str__(self):
        return '%s, %s' % (self.year, self.title)

    def get_absolute_url(self):
        return reverse('queen_detail', args=[str(self.pk)])


class Beehive(models.Model):
    #  Улей
    number = models.IntegerField('Номер')
    row = models.ForeignKey(Row, on_delete=models.SET_NULL, verbose_name='Ряд', null=True, blank=True)
    queen = models.ForeignKey(
        Queen, verbose_name='Матка', on_delete=models.SET_NULL,
        null=True, blank=True, help_text='Матка'
    )
    title = models.CharField(max_length=100, verbose_name='Название')
    text = models.TextField(max_length=1000, verbose_name='Описание')
    TIPE_HIVE = (
        ('rut', 'Рут'),
        ('dad', 'Дадан'),
        ('old', 'Лежак'),
        ('n-1', "Нук"),
        ('n-2', "Нук 2М"),
        ('n-3', "Нук 3М"),
        ('n-4', "Нук 4М"),
        ('xxx', "XNYA"),
    )
    type_hive = models.CharField(
        max_length=3, choices=TIPE_HIVE, verbose_name='Тип улья', blank=True, default='rut')

    # id = models.UUIDField(primary_key=True, default=uuid.uuid4,
    #                       help_text="Unique ID")
    is_active = models.BooleanField(default=True)

    VOLUME_STATUS = (
        ('0', 'Меньше 10 рамок'),
        ('1', '1 корпус'),
        ('2', '2 корпуса'),
        ('3', '3 корпуса'),
        ('4', '4 корпуса'),
        ('5', '5 корпусов!!!'),
    )

    volume = models.CharField(
        max_length=1, choices=VOLUME_STATUS, verbose_name='К-во корпусов', blank=True, default=1)
    pub_date = models.DateField(default=date.today)

    class Meta:
        ordering = ['number']

    def __str__(self):
        return '%s, %s' % (self.number, self.title)

    def get_absolute_url(self):
        return reverse('beehive_detail', args=[str(self.pk)])


class Action(models.Model):
    #  Действие выполненное с ульем (ПС)
    beehive = models.ForeignKey(Beehive, on_delete=models.CASCADE, verbose_name='Улей')
    text = models.TextField(max_length=1000, verbose_name='Действие')
    post_date = models.DateField(default=date.today, verbose_name='Дата')

    class Meta:
        ordering = ['-post_date', '-pk']

    def __str__(self):
        title_text = self.text[:25] + ('...' if len(self.text[:]) > 25 else '')
        return title_text

    def get_absolute_url(self):
        return reverse('action_detail', args=[str(self.pk)])


class Reminder(models.Model):
    #  Совет на будующий осмотр
    beehive = models.ForeignKey(Beehive, verbose_name='Улей', on_delete=models.CASCADE)
    text = models.TextField(max_length=1000, verbose_name='Текст')
    post_date = models.DateField(default=date.today, verbose_name='Дата')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-is_active', 'post_date']

    def get_absolute_url(self):
        return reverse('reminder_detail', args=[str(self.pk)])


class Work(models.Model):
    #  Запись групповых работ с ПС
    text = models.TextField(max_length=1000, verbose_name='Текст')
    beehive = models.ManyToManyField(Beehive, verbose_name='ПС')
    post_date = models.DateField(default=date.today, verbose_name='Дата')

    def get_absolute_url(self):
        return reverse('reminder_detail', args=[str(self.pk)])

