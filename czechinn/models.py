from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User)
    access_token = models.CharField(max_length=30)

    def __str__(self):
        return '<Profile for "{}">'.format(self.user)

    def get_absolute_url(self):
        return reverse('profile')
