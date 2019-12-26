from django.shortcuts import render,redirect
from . import forms
from bussiness.models import bussiness2,desc
from bussiness.forms import bussiness2Form,descform
from django.contrib.auth.models import User
from users.models import Profile,address1
from users.models import Contact
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.contrib import messages

# Create your views here.
def display(request):
    a = request.user
    b = User.objects.get(username = a).id
    e = bussiness2.objects.all()
    if bussiness2.objects.filter(user_id = b).exists():
        q = {}
        customer = {}
        a = request.user
        user_id = User.objects.get(username = a).id
        c = bussiness2.objects.filter(user_id = b)
        b = User.objects.get(username = a).id
        if desc.objects.filter(user_to = b).exists():
            c1 = desc.objects.filter(user_to = b)[0:7]
        else:
            c1 = "No one is going to like you"
        for j in c:
            e = j.id
            f = bussiness2.objects.get(id = e)
            d = Profile.objects.filter(district = j.district)
            n = 0
            for i in d:
                n = n + 1
            q[bussiness2.objects.get(id = e)] = n
        b = Contact.objects.filter(user_from_id = user_id)
        for i in b:
            d = i.user_to_id
            customer[User.objects.get(id = d).username] = Profile.objects.get(id = d).image.url
        customer =  len(customer)
        return render(request,'bussiness.html',{'q':q,'customer':customer,'c1':c1})
    else:
        e = bussiness2.objects.all()
        return render(request,'bussiness.html',{'e':e})


def nearby(request):
    a1 = request.user
    a3 = User.objects.get(username = a1).id
    a2 = Profile.objects.get(user_id = a3).district
    if request.method == 'POST':
        srch = request.POST['srh']
        if srch:
            l = []
            m = {}
            f = {}
            li = list(srch.split(" "))
            for i in li:
                match = bussiness2.objects.filter(Q(bussiness_name__icontains = i))
                if match:
                    for i in match:
                        a = i.user_id
                        v = i.id
                        c = User.objects.get(id = a).username
                        d = address1.objects.get(user_id = a).pincode
                        e = address1.objects.get(user_id = User.objects.get(username = request.user).id).pincode
                        y = bussiness2.objects.get(id = v)
                        print(d,e)
                        l.append(c)
                        if int(d) == int(e):
                            print("d")
                            f[bussiness2.objects.get(id = v)] = User.objects.get(id = a).username
                        else:
                            m[bussiness2.objects.get(id = v)] = User.objects.get(id = a).username
                    return render(request, 'nearby.html', {'m':m,'l':l,'f':f})
            else:
                messages.error(request,'no result found')
        else:
            return HttpResponseRedirect('/nearby/')
    return render(request, 'nearby.html')

def bussiness_form(request):
    form = forms.bussiness2Form(request.POST)
    if request.method == 'POST':
        form = forms.bussiness2Form(request.POST)
        if form.is_valid():
            cmd = form.save(commit=False)
            cmd.user = request.user
            cmd.save()
            return redirect('buss')

    else:
        form = forms.bussiness2Form()
    return render(request,'buss_name.html',{'form':form})

def request_user(request,user_id):
    if request.method == 'POST':
        form = forms.descform(request.POST)
        if form.is_valid():
            print("B")
            cmd = form.save(commit = False)
            cmd.user = request.user
            cmd.user_to = user_id
            cmd.save()
            return redirect('nearby')
    else:
        form = forms.descform()
    return render(request,"request_user.html",{'form':form})
