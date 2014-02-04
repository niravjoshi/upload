from django import forms
from django.forms import ModelForm

from upload.models import Ufile

class UploadFile(ModelForm):
    class Meta:
        model = Ufile
