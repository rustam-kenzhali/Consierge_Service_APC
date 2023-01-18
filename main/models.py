from django.db import models

class Service(models.Model):
    service_title = models.CharField(max_length=100, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    service_icon_src = models.ImageField(upload_to="service/icons/", verbose_name='Иконка')
    service_img_src = models.ImageField(upload_to="service/image/", verbose_name='Иконка')
    bg_img = models.ImageField(upload_to="service/bg/", verbose_name='Иконка')


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

    category = models.ForeignKey('Service_category', on_delete=models.PROTECT, verbose_name='Категория')

    def __str__(self):
        return self.partner_name

    class Meta:
        verbose_name = 'Партнер'
        verbose_name_plural = 'Партнеры'
        ordering = ['id']