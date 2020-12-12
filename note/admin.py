from django.contrib import admin
from .models import Label,Notes
# Register your models here.

@admin.register(Notes)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['user', "description", 'title', 'image', 'is_archive', 'is_trashed', 'reminder']
    list_filter = ['reminder']

    class Meta:
        model = Notes

@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ['name','user']

    class Meta :
        model = Label