from django.db import models

from upload.constants import FILENAME

class UserProfile(models.Model):
    user_email = models.EmailField(unique=True)

    def __unicode__(self):
        return self.user_email

class Ufile(models.Model):
    user_profile = models.ForeignKey(UserProfile)
    user_file = models.FileField(upload_to='.')
    file_name = models.CharField(max_length=100, default=FILENAME)

    def __unicode__(self):
        return self.file_name
