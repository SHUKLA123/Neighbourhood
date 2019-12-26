from django.db import models
# Create your models here.
class Photo(models.Model):
    image = models.ImageField(upload_to = 'pictures/', max_length = 255,null = True,blank = True)
