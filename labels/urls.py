from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from labels import views

urlpatterns = [
    path('labels/', views.LabelsList.as_view()),
    path('labels/<int:pk>/', views.LabelDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)