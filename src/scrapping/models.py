from django.db import models

# Create your models here.
class City(models.Model):
    """
    create table BD
    """
    #python manage.py makemigrations
    #python manage.py migrate
    name = models.CharField(max_length=50,
                            verbose_name='name city')
    slug = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name = 'city name'
        verbose_name_plural ='city names'

    def __str__(self):
        return self.name
