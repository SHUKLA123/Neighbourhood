from django import forms
from bussiness.models import bussiness2,desc

class bussiness2Form(forms.ModelForm):
    class Meta:
        model = bussiness2
        fields = ["bussiness_name","phone","description","photo","street","pincode","district","state","website"]

class descform(forms.ModelForm):
    class Meta:
        model = desc
        fields = ["description",]
