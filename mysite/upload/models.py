from django.db import models

class Ufile(models.Model):
    user_email = models.EmailField()
    ufile = models.FileField(upload_to='/home/niravj/upload/')

    def __unicode__(self):
        return self.user_email

