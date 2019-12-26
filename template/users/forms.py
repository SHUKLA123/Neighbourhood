from django import forms
from .models import Profile,gender2,comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from users.models import tweet9,address1,tweet9file,Event

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username','email']

class GenderUpdateForm(forms.ModelForm):


    class Meta:
        model = gender2
        fields = ['professtion','date_of_birth']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

class tweet9Form(forms.ModelForm):
    class Meta:
        model = tweet9
        fields = ['title','description']

class eventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title','file','description']


class CommentForm(forms.ModelForm):
    body = forms.CharField(label = "",widget = forms.Textarea(attrs={'class': 'form-control','placeholder': 'Text go here!!!!', 'rows' : 2 , 'cols' : '100'}))
    class Meta:
        model = comment
        fields = ['content']

class DataInput(forms.DateInput):
    input_type = 'date'
class gender1Form(forms.ModelForm):

    date_of_birth = forms.DateField(widget= DataInput)
    class Meta:
        model = gender2
        fields = ['gender','date_of_birth','professtion']



class tweet9fileForm(forms.ModelForm):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    class Meta:
        model = tweet9file
        fields = ['file']


class addressForm(forms.ModelForm):
    house = forms.CharField(widget = forms.TextInput(
    attrs = {
        'placeholder': 'House/Building/Apt'
    }))
    street = forms.CharField(widget = forms.TextInput(
    attrs = {
        'placeholder': 'Street/Road/Lane'
    }))
    area = forms.CharField(widget = forms.TextInput(
    attrs = {
        'placeholder': 'Area/Locality/Sector'
    }))
    class Meta:
        model = address1
        fields = ['house','street','area','pincode','district','state']
    def clean_house(self):
        house_input = self.cleaned_data['house']
        return house_input


#forms.DateField(widget= DataInput """forms.DateInput(
#        attrs={
#            'placeholder': 'yyyy-mm-dd'
#        }
#    )"""
