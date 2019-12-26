from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class bussiness2(models.Model):
    user = models.ForeignKey(User,related_name="bussiness", on_delete = models.CASCADE)
    bussiness_name = models.CharField(max_length = 254)
    phone = models.CharField(max_length = 10, blank=False, unique=True)
    description =  models.TextField()
    photo = models.ImageField(default = 'default.jpg', upload_to = 'media')
    street = models.CharField(max_length = 120,blank = False)
    pincode = models.CharField(max_length = 6)
    district = models.CharField(max_length = 120,blank = False)
    state = models.CharField(max_length = 120,blank = False)
    website = models.URLField(max_length = 200, blank = True)

class desc(models.Model):
    user = models.ForeignKey(User,related_name="desc", on_delete = models.CASCADE)
    description = models.CharField(max_length = 100)
    user_to = models.IntegerField()
