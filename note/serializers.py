from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Notes, Label

class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ['name']


class CollaboratorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']


class NotesSerializer(serializers.ModelSerializer):
    label = LabelSerializer(many=True, read_only=True)
    collaborators = CollaboratorsSerializer(many=True, read_only=True)
    class Meta:
        model = Notes
        fields = ['title', 'description', 'label','is_archive', 'collaborators', 'image', 'reminder', 'color']


class ShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = ['title', 'description']


class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = ['title', 'description', 'label','is_archive', 'collaborators'
            , "is_copied", 'checkbox', 'is_pined', 'is_trashed', 'color', 'reminder']