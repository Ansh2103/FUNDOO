from django.urls import path
from . import views
from django.conf.urls import include, url

urlpatterns = [
    path('register/', views.Registrations.as_view(), name="registration"),
    path('login/', views.Login.as_view(), name="login"),
    path('forgotpassword', views.ForgotPassword.as_view(),name="forgotPassword"),
    #path('activate/<surl>/', views.activate, name="activate"),
    #path('reset_password/<surl>/', views.reset_password, name="reset_password"),
    #path('resetpassword/<user_reset>', views.ResetPassword.as_view(), name="resetpassword"),
    path('logout/', views.Logout.as_view() ,name="logout"),

]
