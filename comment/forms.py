from django import forms
from .models import comments
class CommentForm(forms.ModelForm):
    content = forms.CharField(label = "",widget = forms.Textarea(attrs={'class': 'form-control','placeholder': 'Text go here!!!!', 'rows' : 2 , 'cols' : '100'}))
    class Meta:
        model = comments
        fields = ['content']
