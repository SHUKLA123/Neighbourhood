from django import template
from users.models import comment,tweet9file,Event
register=template.Library()

def user_comment_data(value):
    extract = comment.objects.filter(tweet_id = value,reply=None)
    return extract

register.filter('extract',user_comment_data)

def user_reply_data(value):
    extract = comment.objects.filter(reply = value)
    return extract

register.filter('extract_reply',user_reply_data)

def post_images(value):
    image = tweet9file.objects.filter(tweet9_id = value)
    return image

register.filter('image_s',post_images)

def Event_find(value):
    event = Event.objects.filter(pincode = value.address.pincode)
    print("The event is {} for pincode {}".format(event,value.address.pincode))
    return event

register.filter('event',Event_find)
