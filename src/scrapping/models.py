import jsonfield
from django.db import models
from scrapping.utils import from_cyrillic_to_eng


# Create your models here.
class City(models.Model):
    """
    create table BD
    """
    # python manage.py makemigrations
    # python manage.py migrate
    name = models.CharField(max_length=50,
                            verbose_name='name city', unique=True)
    slug = models.CharField(max_length=50, blank=True, unique=True)

    class Meta:
        verbose_name = 'city name'
        verbose_name_plural = 'city names'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.slug == '':
            self.slug = from_cyrillic_to_eng(str(self.name))
            super().save(*args, **kwargs)


class language(models.Model):
    """
    create table BD
    """
    # python manage.py makemigrations
    # python manage.py migrate
    name = models.CharField(max_length=50,
                            verbose_name='Program language', unique=True)
    slug = models.CharField(max_length=50, blank=True, unique=True)

    class Meta:
        verbose_name = 'Program language'
        verbose_name_plural = 'Program languages'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.slug == '':
            self.slug = from_cyrillic_to_eng(str(self.name))
            super().save(*args, **kwargs)


class Vacancy(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=300, verbose_name='Title')
    company = models.CharField(max_length=100, verbose_name='Company')
    description = models.TextField(verbose_name='Description')

    city = models.ForeignKey('City', on_delete=models.CASCADE, verbose_name='City')
    language = models.ForeignKey('language', on_delete=models.CASCADE, verbose_name='language')
    timestamp = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'vacancy'
        verbose_name_plural = 'vacancies'

    def __str__(self):
        return self.title

class Error(models.Model):
    timestamp = models.DateField(auto_now_add=True)
    data = jsonfield.JSONField()

    # def __str__(self):
    #     return self.title

