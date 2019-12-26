from django.contrib import admin
from testapp.models import Photo
# Register your models here.
class PhotoAdmin(admin.ModelAdmin):
    list_display = ['image']
