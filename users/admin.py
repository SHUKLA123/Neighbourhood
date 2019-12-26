from django.contrib import admin

# Register your models here.
from .models import tweet9
from .models import Profile,address1,tweet9file,Event
from .models import Contact
from .models import gender2,comment
class tweet9Admin(admin.ModelAdmin):
    list_display = ['title','description','created']
    list_filter = ['created']

admin.site.register(Event)
admin.site.register(Profile)
admin.site.register(tweet9, tweet9Admin)
admin.site.register(tweet9file)
admin.site.register(Contact)
admin.site.register(gender2)
admin.site.register(address1)
admin.site.register(comment)
