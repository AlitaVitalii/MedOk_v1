import uuid
from datetime import date

from django.db import models

# Create your models here.


class Queen(models.Model):
    #  Пчелиная матка
    year = models.IntegerField()
    title = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return '%s, %s' % (self.year, self.title)


class Beehive(models.Model):
    #  Улий
    number = models.IntegerField()
    row_num = models.CharField(max_length=20)
    queen = models.ForeignKey(Queen, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=100)
    text = models.TextField(max_length=1000)
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
    type_hive = models.CharField(max_length=3, choices=TIPE_HIVE, blank=True, default='rut')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID")
    is_active = models.BooleanField(default=True)

    VOLUME_STATUS = (
        ('0', 'Меньше 10 рамок'),
        ('1', '1 корпус'),
        ('2', '2 корпуса'),
        ('3', '3 корпуса'),
        ('4', '4 корпуса'),
        ('5', '5 корпусов!!!'),
    )

    volume = models.CharField(max_length=1, choices=VOLUME_STATUS, blank=True, default=1)
    pub_date = models.DateField(default=date.today)

    class Meta:
        ordering = ['number']

    def __str__(self):
        return '%s, %s' % (self.number, self.title)



class Action(models.Model):
    #  Действие выполненное с улием (ПС)
    beehive = models.ForeignKey(Beehive, on_delete=models.CASCADE)
    text = models.TextField(max_length=1000)
    post_date = models.DateField(default=date.today)

    class Meta:
        ordering = ['post_date']

    def __str__(self):
        return self.text


class Reminder(models.Model):
    #  Совет на будующий осмотр
    beehive = models.ForeignKey(Beehive, on_delete=models.CASCADE)
    text = models.TextField(max_length=1000)
    post_date = models.DateField(default=date.today)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.text
