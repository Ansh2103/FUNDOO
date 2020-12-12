from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.db import models
from colorful.fields import RGBColorField

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



# Create your models here.
class Notes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    title = models.CharField(max_length=500, blank=True, )
    description = models.TextField(max_length=500, )
    image = models.ImageField(blank=True, null=True, upload_to="media")
    is_archive = models.BooleanField(verbose_name="is_archived", default=False)
    is_trashed = models.BooleanField(verbose_name="delete_note", default=False)
    label = models.ManyToManyField(Label, related_name="label", blank=True)
    collaborators = models.ManyToManyField(User, related_name='collaborators', blank=True)
    is_copied = models.BooleanField(verbose_name="make a copy", default=False)
    checkbox = models.BooleanField(verbose_name="check box", default=False)
    is_pined = models.BooleanField(verbose_name="is pinned", default=False)
    reminder = models.DateTimeField(blank=True, null=True)
    color = RGBColorField(colors=['#FF0000', '#00FF00', '#0000FF'], blank=True, null=True)

    def __str__(self):
        return self.title

    def __repr__(self):
        return "Note({!r},{!r},{!r})".format(self.user, self.title, self.description)

    class Meta:
        """
        name is given which will be displayed in admin page
        """
        verbose_name = 'Note'
        verbose_name_plural = 'Notes'