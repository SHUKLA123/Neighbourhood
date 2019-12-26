from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from allauth.account.views import SignupView
# Create your views here.


class mysignin(SignupView):
    def image(request):
        if request.method == "POST":
            upload = request.FILES['image']
            fs = FileSystemStorage()
            fs.save(upload.name,uplad)
            print(uplad.name)
            prin(upload.size)
        return render(request,'signup.html')



"""
from django.core.files.storage import FileSystemStorage
from .forms import PhotoForm,MyCustomSignupForm
from . import models
from testapp.models import Photo
from allauth.account.views import SignupView

class Mysignup(SignupView):
    def image_upload1(self,request,**kwargs):
        ret = super(MyCustomSignupForm, self).get_context_data(**kwargs)
        if request.method == 'POST':
            form = MyCustomSignupForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return ret
        else:
            form = MyCustomSignupForm()
        return ret

def update_image(request,id):
    photo = Photo.objects.get(id = id)
    if request.method == 'POST':
        form1 = PhotoForm(request.POST,instance = photo)
        if form.is_valid():
            form1.save()
            return redirect('/')
    return render(request,'a.html',{'photo':photo})

def show_image(request):
    photo1 = Photo.objects.all()
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('a.html')
    else:
        form = PhotoForm()
    return render(request,'a.html',{'photo1':photo1,'form':form})
"""
