"""
 ******************************************************************************
 *  Purpose: Label app is created so all the note CRUD  is created,
 *           user can create, update ,delete or search note 
 *  @author  Shubham Kumar
 *  @version 3.8
 *  @since   15/12/2020
 ******************************************************************************
"""

from .models import Label
from .serializers import LabelSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class LabelsList(APIView):
    """
    List all Labels, or create a new labels.
    """
    def get(self, request, format=None):
        labels = Label.objects.all()
        serializer = LabelSerializer(labels, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = LabelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LabelDetail(APIView):
    """
    Retrieve, update or delete a Label instance.
    """
    def get_object(self, pk):
        try:
            return Label.objects.get(pk=pk)
        except Label.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        label = self.get_object(pk)
        serializer = LabelSerializer(label)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        label = self.get_object(pk)
        serializer = LabelSerializer(label, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        label = self.get_object(pk)
        label.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)