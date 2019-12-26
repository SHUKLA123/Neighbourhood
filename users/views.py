from django.shortcuts import render,redirect, get_object_or_404
from users.models import Profile
from . import forms
from .models import gender2,address1

from django.contrib.auth.decorators import login_required
#Registration
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm,UserUpdateForm, ProfileUpdateForm,gender1Form,GenderUpdateForm,addressForm,eventForm
#for search bar
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib import messages
#for tweet files
from django.conf import settings
from django.core.files.storage import FileSystemStorage

# Profile views
from friendship.models import Friend, Follow, Block
from django.contrib.auth.models import User

#follower
from django.views.decorators.http import require_POST
from common.decorators import ajax_required
from django.http import JsonResponse
from users.models import Contact

# notification
from actions.models import Action
from actions.utils import create_action

#Post
from users.models import tweet9,Event

from bussiness.models import bussiness2
from datetime import date

#comments
from .models import comment
from .forms import CommentForm

#map
from geopy.geocoders import Nominatim
#code

def register(request):
    if request.method == 'POST':
        form1 = UserRegisterForm(request.POST)
        form = forms.gender1Form(request.POST)
        form2 = forms.addressForm(request.POST)
        if form1.is_valid() and form.is_valid() and form2.is_valid():
            form1.save()
            new_item = form1.save()
            cmd = form.save(commit=False)
            cmd1 = form2.save(commit = False)
            username = form1.cleaned_data.get('username')
            user_id = User.objects.get(username = username).id
            print(user_id)
            cmd.user_id = user_id
            cmd1.user_id = user_id

            cmd.save()
            cmd1.save()
            username = form1.cleaned_data.get('username')
            create_action(new_item, 'has created an account')
            a = create_action(new_item, 'has created an account')
            messages.success(request, f'Account created for {username}!')

            return redirect('login')
    else:
        form1 = UserRegisterForm()
        form = gender1Form()
        form2 = addressForm()
    return render(request, 'register.html',{'form1':form1,'form' : form,'form2':form2})


def map(request):
    l = []

    a = request.user
    user_id = User.objects.get(username = a).id
    pincode = address1.objects.get(user_id = user_id).state
    add = address1.objects.filter(state = pincode)
    print(add)
    for i in add:
        d = {}
        username = User.objects.get(id = i.user_id).username
        d["name"] = username
        print(d["name"])
        id = address1.objects.get(user_id = user_id).id
        house = i.house
        street = i.street
        area = i.area
        pincode = i.pincode
        real_add = str(house) + " " +str(street) + " " +str(area) +" " + str(pincode)
        d['address'] = real_add
        geolocator = Nominatim(timeout=3)
        location = geolocator.geocode(pincode)

        lat = location.latitude
        lon = location.longitude
        d['lat'] = lat
        d['lon'] = lon
        l.append(d)
    print(l)
    return render(request,'map.html',{'l':l})




@login_required(login_url="/login/")
def home(request):
    q = {}
    l = []
    a = request.user

    e1 = bussiness2.objects.all()
    user_id = User.objects.get(username = a).id

    id = address1.objects.get(user_id = user_id).id
    house = address1.objects.get(user_id = user_id).house
    street = address1.objects.get(user_id = user_id).street
    area = address1.objects.get(user_id = user_id).area
    pincode = address1.objects.get(user_id = user_id).pincode
    print(pincode)
    real_add = str(house) + " " +str(street) + " " +str(area) +" " + str(pincode)
    ladd = address1.objects.all()

    for i in ladd:
        housel = address1.objects.get(user_id = i.user_id).house
        streetl = address1.objects.get(user_id = i.user_id).street
        pincodel = address1.objects.get(user_id = i.user_id).pincode
        areal = address1.objects.get(user_id = i.user_id).area
        if (int(housel[0:4]) == int(house[0:4])-1 and street == streetl and pincode == pincodel and area == areal) :
            username = User.objects.get(id = i.user_id).username
            messages.info(request, f'your near neighbour {username}!')
            break
        else:
            continue


    for i in ladd:
        housel = address1.objects.get(user_id = i.user_id).house
        streetl = address1.objects.get(user_id = i.user_id).street
        pincodel = address1.objects.get(user_id = i.user_id).pincode
        areal = address1.objects.get(user_id = i.user_id).area
        if (int(housel[0:4]) == int(house[0:4])+1 and street == streetl and pincode == pincodel and area == areal):
            print("d")
            usernamer = User.objects.get(id = i.user_id).username
            messages.info(request, f'Yours near neighbour {usernamer}!')
            break
        else:
            continue



    real_add = str(house) + " " +str(street) + " " +str(area) +" " + str(pincode)
    age1 = gender2.objects.get(user_id = user_id).date_of_birth
    today = date.today()
    b = age1
    l1 = str(today).split("-")
    l2 = str(b).split("-")
    age = int(l1[0])-int(l2[0])
    actions = Action.objects.exclude(user = user_id)
    following_ids = request.user.user_following.values_list('id', flat=True)
    if following_ids:
        actions = actions.filter(user_id__in=following_ids).select_related('user','user__Profile').prefetch_related('target')
    actions = actions[:10]
    if tweet9.objects.filter(user_id = user_id).exists():
            if len(list(tweet9.objects.filter(user_id = user_id))):
                    context = tweet9.objects.filter(user_id = user_id)
                    for j in context:
                            e = j.id
                            l.append(tweet9.objects.get(id = e))
    b = Contact.objects.filter(user_from_id = user_id)
    for i in b:
        d = i.user_to_id
        q[User.objects.get(id = d).username] = Profile.objects.get(id = d).image.url
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST,instance = request.user)
        p_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.Profile)
        if u_form.is_valid and p_form.is_valid:
            u_form.save()
            p_form.save()
            messages.success(request,f'Your Account has been successfully updated')
            return redirect('home')
    else:
        u_form = UserUpdateForm(request.POST,instance = request.user)
        p_form = ProfileUpdateForm(request.POST,instance = request.user.Profile)
    len1 = len(q)


    return render(request,'home.html',{
    'u_form' : u_form,
    'p_form' : p_form,
    'len1' : len1,
    'l' : l,
    'actions' : actions,
    'e1' : e1,
    'age' : age,
    'dob' : age1,
    'real_add' : real_add,
    'id' : id,
    'pincode':pincode
    })


@login_required(login_url="/login/")
#Search bar
def search(request):

    if request.method == 'POST':

        srch = request.POST['srh']

        if srch:

            match = User.objects.filter(Q(username = srch))

            if match:

                c = User.objects.get(username = srch)
                y = User.objects.get(username = srch).id
                id = address1.objects.get(user_id =y).id
                house = address1.objects.get(user_id = y).house
                street = address1.objects.get(user_id = y).street
                area = address1.objects.get(user_id = y).area
                pincode = address1.objects.get(user_id = y).pincode
                z = str(house) + " " +str(street) + " " +str(area) +" " + str(pincode)

                a = Profile.objects.get(user_id = y).image
                b = a.url

                return render(request, 'search.html', {'sr':srch,'b':b,'z':z})

            else:
                l = []
                match = address1.objects.filter(Q(district__icontains = srch)|Q(pincode__icontains = srch))
                if match:
                    for i in match:
                        a = i.user_id
                        ef = User.objects.get(id = a).username
                        s = address1.objects.get(user_id = a).district
                        print(s)
                        a = Profile.objects.get(user_id = a).image
                        k = a.url
                        l.append(ef)
                    return render(request, 'search.html',{"l":l,"s":s,"k":k})


                else:

                    messages.error(request,'no result found')

        else:

            return HttpResponseRedirect('/search/')
    return render(request,'search.html')


#Profile View
def ProfileView(request,username):
    user = get_object_or_404(User, username=username, is_active=True)
    users=User.objects.get(username=username)
    id = User.objects.get(username = user).id
    age1 = gender2.objects.get(user_id = id).date_of_birth
    today = date.today()
    b = age1
    l1 = str(today).split("-")
    l2 = str(b).split("-")
    print(l1[0])
    print(l2[0])
    age = int(l1[0])-int(l2[0])
    gender_real = gender2.objects.get(user_id = id).gender
    if gender_real == "M":
        gender_real = "Male"
    elif gender_real == "F":
        gender_real = "Female"
    else:
        gender_real = "Both"

    user_id = address1.objects.get(user_id = id).id
    house = address1.objects.get(id = user_id).house
    street = address1.objects.get(id = user_id).street
    area = address1.objects.get(id = user_id).area
    pincode = address1.objects.get(id = user_id).pincode
    add = str(house) + " " +str(street) + " " +str(area) +" " + str(pincode)
    imag = Profile.objects.get(user_id = id).image
    d1 = imag.url
    friend = Friend.objects.friends(user)
    q = {}
    e = {}
    b = Contact.objects.filter(user_from_id = id)
    for i in b:
        d = i.user_to_id
        q[User.objects.get(id = d).username] = Profile.objects.get(id = d).image.url

    len1 = len(q)
    b = Contact.objects.filter(user_to_id = id)
    for i in b:
        d = i.user_from_id
        e[User.objects.get(id = d).username] = Profile.objects.get(id = d).image.url

    len2 = len(e)
    return render(request, 'profile_view.html',{
    'users':users,
    'add':add,
    'imag':d1,
    'user':user,
    'q' : q,
    'len1' : len1,
    'e' : e,
    'len2' : len2,
    'gender_real':gender_real,
    'age' : age,
    'dob' : age1
       })

#tweet meaker

def tweet_view(request):
    form = forms.tweet9Form(request.POST)
    file_form = forms.tweet9fileForm(request.POST)
    if request.method == 'POST':
        form = forms.tweet9Form(request.POST) # , request.FILES
        file_form = forms.tweet9fileForm(request.POST, request.FILES)
        files = request.FILES.getlist('file')
        print("sm")
        if form.is_valid() and file_form.is_valid():
            print("nf")
            cmd = form.save(commit=False)
            cmd.user = request.user
            cmd.save()
            id = cmd.id
            cmd1 = file_form.save(commit=False)
            cmd1.tweet9_id=id
            cmd1.save()

            return redirect('post')

    else:
        form = forms.tweet9Form()
        file_form = forms.tweet9fileForm()
    return render(request,'tweet_view.html',{'form':form, 'file_form':file_form})

#tweet shower

def post_list(request):
    l = []
    a = request.user
    user_id = User.objects.get(username = a).id
    contact = Contact.objects.filter(user_from_id = user_id)
    for i in contact:
         b = i.user_to_id
         if tweet9.objects.filter(user_id = b).exists():

             if len(list(tweet9.objects.filter(user_id = b))):

                 context = tweet9.objects.filter(user_id = b)
                 for j in context:

                     e = j.id
                     l.append(tweet9.objects.get(id = e))

         else:
             continue
    return render(request, 'tweet_view1.html', {'l':l})

#event creation

def event_create(request):
    form = forms.eventForm(request.POST)
    if request.method == 'POST':
        form = forms.eventForm(request.POST, request.FILES)
        if form.is_valid():
            cmd = form.save(commit=False)
            cmd.user = request.user
            cmd.pincode = int(request.user.address.pincode)
            cmd.save()
            return redirect('event')

    else:
        form = forms.eventForm()
    return render(request,'event.html',{'form':form})




#user_follow
@ajax_required
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(user_from=request.user,user_to=user)
            else:
                Contact.objects.filter(user_from=request.user,user_to=user).delete()
            return JsonResponse({'status':'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status':'ko'})
    return JsonResponse({'status':'ko'})


#following
def follow_people(request):
    q = {}
    e = {}
    a = request.user
    user_id = User.objects.get(username = a).id
    b = Contact.objects.filter(user_from_id = user_id)
    for i in b:
        d = i.user_to_id
        q[User.objects.get(id = d).username] = Profile.objects.get(id = d).image.url

    len1 = len(q)

    a = request.user
    user_id = User.objects.get(username = a).id
    b = Contact.objects.filter(user_to_id = user_id)
    for i in b:
        d = i.user_from_id
        e[User.objects.get(id = d).username] = Profile.objects.get(id = d).image.url

    len2 = len(e)
    return render(request,'neighbour.html',{
    'q' : q,
    'len1' : len1,
    'e' : e,
    'len2' : len2
    })



#address Update view

def AddressUpdateView(request):
    a = request.user
    print(a.id)
    user_add = address1.objects.get(user_id=a.id)

    if request.method == 'POST':
        a_form = addressForm(request.POST,instance = request.user)
        if a_form.is_valid:
            a_form.save()
            messages.success(request,f'Your Account has been successfully updated')
            return redirect('home')
        else:
            messages.error(request,f'Fill form correctly to update Address.')
    return render(request, 'useraddressupdate.html', {'a_form':a_form, 'user_add':user_add})





#like-system for post
@ajax_required
@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')

    action = request.POST.get('action')

    if image_id and action:
        try:
            image = tweet9.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
                create_action(request.user, 'likes', image)

            else:
                a = image.users_like.remove(request.user)

            return JsonResponse({'status': 'ok','image_id':image_id})
        except:

            pass
    return JsonResponse({'status': 'ko'})


#like-system for event
@ajax_required
@login_required
@require_POST
def event_like(request):
    event_id = request.POST.get('id')
    print(event_id)
    action = request.POST.get('action')
    print(action)
    if event_id and action:
        try:
            event_like_v = Event.objects.get(id=event_id)

            if action == 'like':
                event_like_v.users_like.add(request.user)

            else:
                a = event_like_v.users_like.remove(request.user)

            return JsonResponse({'status': 'ok','event_id':event_id})
        except:


            pass
    return JsonResponse({'status': 'ko'})

from users.models import comment
@require_POST
@ajax_required
def write_comment(request):
    if request.method == 'POST':
        #try:
        id = request.POST.get('id')
        comment_come = request.POST.get('comment')

        a = tweet9.objects.get(id=id).id
        print(a)
        user_dn = str(request.user)
        comment_use_for_ajax = comment.objects.create(
        user = request.user,
        tweet = tweet9.objects.get(id=id),
        content = comment_come,
        )
        user_n = {'id':comment_use_for_ajax.id,'user_dn':user_dn,'tweet_id':a,'content':comment_use_for_ajax.content}
        data = {
        'status' : 'ok',
        'comment':comment_come,
        'user_n':user_n
        }



        return JsonResponse(data)
    return JsonResponse({'status' : 'ko'})



from users.models import comment
@require_POST
@ajax_required
def write_reply(request):
    if request.method == 'POST':
        #try:
        id = request.POST.get('id')
        tweet_id = request.POST.get('tweet_id')
        reply_come = request.POST.get('reply')
        print(id)

        a_reply_to = comment.objects.get(id=id)
        a_reply = comment.objects.get(id=id).id

        user_dn = str(request.user)
        reply_use_for_ajax = comment.objects.create(
        user = request.user,
        tweet = tweet9.objects.get(id=tweet_id),
        reply = a_reply_to,
        content = reply_come,
        )
        user_n = {'id':reply_use_for_ajax.id,'user_dn':user_dn,'comment_use_id':a_reply,'tweet_use_id':tweet_id,'content':reply_use_for_ajax.content}
        data = {
        'status' : 'ok',
        'reply':reply_come,
        'user_n':user_n
        }
        return JsonResponse(data)
    return JsonResponse({'status' : 'ko'})



















"""def update_address(request,id):
    address = address1.objects.get(id=id)
    if request.method == 'POST':
        a_form = addressForm(request.POST,instance=address1)
        if a_form.is_valid():
            a_form.save()
            return redirect('home')
    else:
        a_form = addressForm()
    return render(request,'update.html',{'a_form':a_form})
"""

"""
	action = request.POST.get('action')

from users.models import Profile
from users.models import tweet9
from users.models import Contact
from django.contrib.auth.models import User
from django.db.models import Q
a = 'Vageshwari'
user_id = User.objects.get(username = a).id
contact = Contact.objects.filter(user_from_id = user_id)
for i in contact:
     b = i.user_to_id
     if tweet9.objects.filter(user_id = b).exists() or tweet9.objects.filter(user_id = user_id).exists():
         print("I am Here")
             if len(list(tweet9.objects.filter(user_id = b)))>1 or len(list(tweet9.objects.filter(user_id = user_id)))>1:
                     context = tweet9.objects.filter(user_id = b)
                     context1 = tweet9.objects.filter(user_id = user_id)
                     print(context1)
                     for j in context:
                             e = j.id
                             c = tweet9.objects.get(id = e)
                             print(c)
                     for k in context1:
                             f = k.id
                             g = tweet9.objects.get(id = f)
                             print(g)
             else:
                     c = tweet9.objects.get(user_id = b)
                     g = tweet9.objects.get(user_id = user_id)
                     print(c)
                     print(g)
     else:
             continue

contact = Contact.objects.filter(user_from_id = user_id)
    for i in contact:
     b = i.user_to_id
     if tweet9.objects.filter(user_id = b).exists():
             if len(list(tweet9.objects.filter(user_id = b)))>1:
                     context = tweet9.objects.filter(user_id = b)
                     print(context)
                     for j in context:
                             e = j.id
                             c= tweet9.objects.get(id = e)
                             print(c)
             else:
                     c = tweet9.objects.get(user_id = b)
                     print(c)
     else:
             continue
a = request.user
user_id = User.objects.get(username = a).id
if tweet9.objects.filter(user_id = user_id).exists():
    if len(list(tweet9.objects.filter(user_id = user_id)))>1:
            content = tweet9.objects.filter(user_id = user_id)
            for k in content:
                    e = k.id
                    c = tweet9.objects.get(id = e)
                    print(c)
    else:
            c = tweet9.objects.get(user_id = user_id)
            print(c)

for i in contact:
     b = i.user_to_id
     if tweet9.objects.filter(user_id = b).exists():
             if len(list(tweet9.objects.filter(user_id = b)))>1:
                     context = tweet9.objects.filter(user_id = b)
                     print(context)
                     for j in context:
                             e = j.id
                             c= tweet9.objects.get(id = e)
                             print(c)
             else:
                     c = tweet9.objects.get(user_id = b)
                     print(c)
     else:
             continue

# other way of extract the things
 from django.core.exceptions import ObjectDoesNotExist
 for i in contact:
     print('i')
     b = 10
     print(b)
     try:
             c = tweet9.objects.get(user_id = b)
             print(c)
     except ObjectDoesNotExist:
             continue
"""
