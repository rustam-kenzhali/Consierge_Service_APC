from django.db import models
from django.contrib.auth.models import AbstractUser
from phone_field import PhoneField
from django.urls import reverse
import os


class Service(models.Model):
    service_title = models.CharField(max_length=100, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    service_icon_src = models.ImageField(upload_to="service/icons/", verbose_name='Иконка')
    service_img_src = models.ImageField(upload_to="service/image/", verbose_name='Картинка')
    bg_img = models.ImageField(upload_to="service/bg/", verbose_name='Бекграунд')


    def __str__(self):
        return self.service_title

    def get_absolute_url(self):
        return reverse('service', kwargs={'service_slug': self.slug})

    class Meta:
        verbose_name = 'Сервис'
        verbose_name_plural = 'Сервисы'
        ordering = ['id']


class Service_category(models.Model):
    category_name = models.CharField(max_length=100, db_index=True, verbose_name='Заголовок')

    service = models.ForeignKey('Service', on_delete=models.PROTECT, verbose_name='Сервис')

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']


class Partners(models.Model):
    partner_name = models.CharField(max_length=100, db_index=True, verbose_name='Заголовок')
    partner_description = models.CharField(max_length=255, verbose_name='Опизание')
    partner_city = models.CharField(max_length=100, verbose_name='Город')
    partner_price = models.CharField(max_length=100, verbose_name='Цена')
    partner_image = models.ImageField(upload_to="partner/image/", verbose_name='Фото')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    category = models.ForeignKey('Service_category', on_delete=models.PROTECT, verbose_name='Категория')

    def get_absolute_url(self):
        return reverse('', kwargs={'partner_slug': self.slug})

    class Meta:
        verbose_name = 'Партнер'
        verbose_name_plural = 'Партнеры'
        ordering = ['id']

    def __str__(self):
        return self.partner_name


class CS_User(AbstractUser):
    STATUS = (
        ('b2c', 'b2b'),
        ('b2b', 'b2b'),
        ('moderator', 'moderator'),
        ('admin', 'admin')
    )

    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    def __str__(self) -> str:
        return self.username + ' ' + self.email

    is_b2b = models.BooleanField(default=False)

    # status = models.CharField(max_length=100, choices=STATUS, default='b2c')
    full_name = models.CharField(max_length=255, default='', blank=True)
    company_name = models.CharField(max_length=255, default='Должность', blank=True)
    company_role = models.CharField(max_length=255, default='Компания', blank=True)
    phone = PhoneField(blank=True)
    address = models.CharField(max_length=255, default='', blank=True)
    image = models.ImageField(upload_to="user/image", default='user/image/user.png' , verbose_name='Иконка', blank=True)
    # birthdate = models.DateField()

    services = models.ManyToManyField('Service')


def create_id_path(instance, filename):
    return os.path.join(
        'user',
        'ID',
        instance.username,
        filename
    )


class Order(models.Model):
    userID = models.CharField(max_length=255, verbose_name='ID пользователя')
    username = models.CharField(max_length=255, verbose_name='Пользователь')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    item = models.ForeignKey('Partners', on_delete=models.PROTECT, verbose_name='Предмет покупки')
    is_active = models.BooleanField(default=False, verbose_name='Оплата покупки')

    first_name = models.CharField(max_length=100, verbose_name='Имя')
    second_name = models.CharField(max_length=100, verbose_name='Фамилия')
    last_name = models.CharField(max_length=100, verbose_name='Отчество')

    user_id_card = models.FileField(upload_to=create_id_path, verbose_name='Уд', blank=True)

    time_start = models.DateTimeField(verbose_name='Время начала заказа', blank=True)
    time_end = models.DateTimeField(verbose_name='Время конца заказа', blank=True)
    count = models.IntegerField(verbose_name='Колличество')
    city = models.CharField(max_length=100, verbose_name='Город')
    address = models.CharField(max_length=100, verbose_name='Адрес', blank=True)
    info = models.CharField(max_length= 1000, verbose_name='Детали', blank=True)



