"""
 ******************************************************************************
 *  Purpose: note app is created so all the note CRUD  is created,
 *           user can create, update ,delete or search note 
 *  @author  Shubham Kumar
 *  @version 3.8
 *  @since   15/12/2020
 ******************************************************************************
"""
# import json
# import logging
# from .models import Notes
# from django.http import HttpResponse
# from django.contrib.auth.models import User
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from django.conf import settings
# from fundoo.settings import  file_handler
# from rest_framework.generics import GenericAPIView
# from rest_framework.permissions import IsAuthenticated
# from .serializers import NotesSerializer,UpdateSerializer,CollaboratorsSerializer,ShareSerializer

# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
# logger.addHandler(file_handler)

# class NoteCreate(GenericAPIView):
#     """
#         Summary:
#         --------
#             Note class will let authorized user to create and get notes.
#         Methods:
#         --------
#             get: User will get all the notes.
#             post: User will able to create new note.
#     """
#     serializer_class = NotesSerializer

#     def post(self,request):
#         """
#              Summary:
#              --------
#                  New note will be create by the User.
#              Exception:
#              ----------
#                  KeyError: object
#              Returns:
#              --------
#                  response: SMD format of note create message or with error message
#         """
#         user = request.user
#         try:
#             data = request.data
#             if len(data) == 0:
#                 raise KeyError
#             serializer = NotesSerializer(data=data, partial=True)
#             if serializer.is_valid():
#                 serializer.save(user_id=user.id)
#                 response = {'success': True, 'message': "note created", 'data': []}
#                 return Response(response,status=200)
#             else:
#                 logger.error(" %s for  %s", user, serializer.errors)
#                 response = {'success': False, 'message': "note was not created", 'data': []}
#                 return HttpResponse(json.dumps(response, indent=2), status=400)
#         except Exception as e:
#             print(e)
#             logger.error("got %s error for creating note for user %s", str(e),user)
#             response = {'success': False, 'message': "something went wrong", 'data': []}
#             return Response(response, status=400)


    #def get(request):

# from .models import Notes
# from note.serializers import NotesSerializer
# from rest_framework import generics


# class NotesList(generics.ListCreateAPIView):
#     queryset = Notes.objects.all()
#     serializer_class = NotesSerializer


# class NotesDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Notes.objects.all()
#     serializer_class = NotesSerializer


from .models import Notes
from .serializers import NotesSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class NotesList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        notesQS = Notes.objects.all()
        serializer = NotesSerializer(notesQS, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = NotesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NotesDetail(APIView):
    """
    Retrieve, update or delete a Notes instance.
    """
    def get_object(self, pk):
        try:
            return Notes.objects.get(pk=pk)
        except Notes.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        note = self.get_object(pk)
        serializer = NotesSerializer(note)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        note = self.get_object(pk)
        serializer = NotesSerializer(note, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        note = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)