from django.db import models
from django.db import models
from django.contrib.auth.models import User as auth_user

from django.db.models import CharField, Model
# Create your models here.
class MovieModel(models.Model):
    movie= models.CharField(max_length=240)
