from django.db import models
from django.contrib.auth.models import User, AbstractUser


# Create your models here.
class Label(models.Model):
    name = models.CharField("name of label", max_length=254)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='label_user', default="admin")

    def __str__(self):
        return self.name
   

    def __repr__(self):
        return "Label({!r},{!r})".format(self.user, self.name)

    class Meta:
        """
        name is given which will be displayed in admin page
        """
        verbose_name = 'label'
        verbose_name_plural = 'labels'
