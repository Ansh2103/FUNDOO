from .models import Label
from django.contrib.auth.models import User
from rest_framework import serializers

class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ['name']