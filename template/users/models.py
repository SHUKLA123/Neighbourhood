from django.db import models
from PIL import Image
# Create your models here.
from django.contrib.auth.models import User


class gender2(models.Model):
    user = models.OneToOneField(User,related_name="gender", on_delete = models.CASCADE)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('B', 'Both'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    professtion = models.CharField(max_length = 160)

class address1(models.Model):
    user = models.OneToOneField(User,related_name="address", on_delete = models.CASCADE)
    house = models.CharField(max_length = 120)
    street = models.CharField(max_length = 120)
    area = models.CharField(max_length = 120)
    pincode = models.CharField(max_length = 6)
    district = models.CharField(max_length = 25)
    state = models.CharField(max_length = 50)


class Profile(models.Model):
    user = models.OneToOneField(User,related_name="Profile", on_delete = models.CASCADE)
    image = models.ImageField(default = 'default.jpg', upload_to = 'media')
    
    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)

        img =  Image.open(self.image.path)
        if img.height >300 or img.width>300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)

from django.conf import settings
class tweet9(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name="post_created")
    title = models.CharField(max_length = 255, blank = True)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add = True,db_index = True)
    users_like = models.ManyToManyField(User,related_name = 'image_liked',blank = True)
    total_likes = models.PositiveIntegerField(db_index=True, default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-created',)

class tweet9file(models.Model):
    file = models.FileField(upload_to="file")
    tweet9 = models.ForeignKey(tweet9, on_delete=models.CASCADE, related_name='files')

class Event(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name="event_created")
    title = models.CharField(max_length = 255, blank = True)
    file = models.FileField(upload_to="file")
    pincode = models.CharField(max_length=6)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add = True,db_index = True)
    users_like = models.ManyToManyField(User,related_name = 'event_liked',blank = True)
    total_likes = models.PositiveIntegerField(db_index=True, default=0)


class comment(models.Model):
    user = models.ForeignKey(User, related_name = "tweet_comment_user")
    tweet  = models.ForeignKey(tweet9, related_name = "tweet")
    content = models.TextField()
    reply = models.ForeignKey('comment',null = True, related_name = "replies_user_model")
    allow_annon =  models.BooleanField(default = True)
    timestamp = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    class Meta:
        ordering = ('-timestamp',)
    def __str__(self):
        return 'Commented By {} on {}'.format(self.user,self.tweet)

from django.conf import settings
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name = 'profile')
    following = models.ManyToManyField(settings.AUTH_USER_MODEL,blank = True,related_name = 'followed_by')

    def __str__(self):
        return str(self.following.all().count)

class Contact(models.Model):
    user_from = models.ForeignKey(User,related_name = 'user_from_set')
    user_to = models.ForeignKey(User,related_name = 'user_to_set')
    created = models.DateTimeField(auto_now_add = True, db_index = True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{} user_follows {}'.format(self.user_from, self.user_to)


User.add_to_class('user_following', models.ManyToManyField('self', through = Contact, related_name = 'user_followers', symmetrical = False))
