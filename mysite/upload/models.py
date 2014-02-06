from django.db import models

class UserProfile(models.Model):
    user_email = models.EmailField(unique=True)

    def __unicode__(self):
        return self.user_email

class Ufile(models.Model):
    user_profile = models.ForeignKey(UserProfile)
    user_file = models.FileField(upload_to='.')

    def __unicode__(self):
        return self.user_profile
