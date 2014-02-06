from django import forms
from django.forms import Form

from upload.models import UserProfile,Ufile

class UserFileForm(Form):
    user_email = forms.EmailField()
    user_file = forms.FileField()
    class Meta:
        pass
