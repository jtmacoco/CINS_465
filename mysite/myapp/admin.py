from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.MovieModel)
admin.site.register(models.ProfileModel)