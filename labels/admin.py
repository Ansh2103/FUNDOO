from django.contrib import admin

# Register your models here.
from .models import Label

@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ['name','user']

    class Meta :
        model = Label