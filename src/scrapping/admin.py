from django.contrib import admin
from .models import City,language,Vacancy,Error,url


# Register your models here.
admin.site.register(City)
admin.site.register(language)
admin.site.register(Vacancy)
admin.site.register(Error)
admin.site.register(url)