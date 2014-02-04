from django.db import models

class Ufile(models.Model):
    user_email = models.EmailField(max_length=50,unique = True)
    #ufile = models.FileField(upload_to=None)

    def __unicode__(self):
        return self.user_email

