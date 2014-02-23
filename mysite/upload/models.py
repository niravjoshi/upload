from django.db import models
from django.contrib.auth.models import User


class Ufile(models.Model):
    user_profile = models.ForeignKey(User)
    user_file = models.FileField(upload_to='.')
    file_name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.file_name
