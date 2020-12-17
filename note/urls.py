from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url

from note import views

urlpatterns = [

    #path("notes/", views.NoteCreate.as_view(), name="notes"),
    path('notes/', views.NotesList.as_view()),
    path('notes/<int:pk>/', views.NotesDetail.as_view()),

]

