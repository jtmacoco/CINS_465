from django.db import models
from django.contrib.auth.models import User as auth_user
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
# Create your models here.
class MovieModel(models.Model):
    movie = models.CharField(max_length=240)
    author = models.ForeignKey(auth_user,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.author.username)+" " + str(self.movie)

class ProfileModel(models.Model):
    image = models.ImageField(
    max_length = 144,
    upload_to = 'uploads/%Y/%m/%d/',
    null = True
    )
    thumbnail = ImageSpecField(
    source='image', processors=[ResizeToFill(100,100)]
    )
    about = models.CharField(max_length=240)
    author = models.ForeignKey(auth_user,on_delete=models.CASCADE)
