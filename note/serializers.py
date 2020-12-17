from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Notes
from labels.serializers import LabelSerializer


class NotesSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Notes
        fields = '__all__'


