from django import forms
from testapp.models import Photo
class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = '__all__'
from allauth.account.forms import SignupForm
from django import forms
class CustomSignupForm(SignupForm):
    Address = forms.CharField(max_length=50, label='Address')
    def signup(self, request, user):
        user.Address = self.cleaned_data['Address']
        return user
