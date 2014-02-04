from django import forms
from django.forms import ModelForm

from upload.models import Ufile

class UploadFile(ModelForm):
    user_email = forms.EmailField(max_length=50, required=True)
    class Meta:
        model = Ufile
