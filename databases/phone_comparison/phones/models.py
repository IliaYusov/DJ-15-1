from django.db import models

# Create your models here.


class Manufacturer(models.TextChoices):
    APPLE = 'Apple'
    SAMSUNG = 'Samsung'
    XIAOMI = 'Xiaomi'


class Phone(models.Model):
    name = models.CharField("Модель", max_length=50)
    manufacturer = models.TextField("Производитель", choices=Manufacturer.choices)
    price = models.IntegerField("Цена")
    os = models.CharField("Операционная система", max_length=20)
    dpi = models.IntegerField("Число пикселей на дюйм")
    cpu = models.CharField("Процессор", max_length=50)
    screen_resolution = models.CharField("Разрешение экрана", max_length=20)
    additional_info = models.TextField("Дополнительно", default=None, blank=True, null=True)

    def __str__(self):
        return f'{self.id}: {self.name}'

    class Meta:
        abstract = True


class PhoneGeneric(Phone):
    pass


class PhoneApple(Phone):
    face_id = models.BooleanField("FaceId")


class PhoneSamsung(Phone):
    stylus = models.BooleanField("Наличие стилуса")


class PhoneXiaomi(Phone):
    ir_port = models.BooleanField("Инфракрасный порт")
