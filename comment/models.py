from django.db import models
from django.conf import settings
# Create your models here.
class comments(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = "comment_user")
    pincode  = models.CharField(max_length = 6)
    reply = models.ForeignKey('comments',null = True, related_name = "replies")
    content = models.TextField()
    allow_annon =  models.BooleanField(default = True)
    timestamp = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.pincode
