from django.db import models

class Ufile(models.Model):
    user_email = models.EmailField()
    user_file = models.FileField(upload_to='.')

    def __unicode__(self):
        return self.user_email

