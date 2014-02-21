from django import forms
from django.forms import Form
from django.contrib.auth.models import User

from upload.models import UserProfile,Ufile

class UserFileForm(Form):
    user_email = forms.EmailField()
    user_file = forms.FileField()
    class Meta:
        pass

class UserForm(Form):
    first_name = forms.CharField(max_length=32, required=True)
    last_name = forms.CharField(max_length=32, required=True)
    email = forms.EmailField(max_length=50, required=True)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput, required=True)
    class Meta:
        model = User

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        return cleaned_data

