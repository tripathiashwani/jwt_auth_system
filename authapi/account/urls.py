from account.views import UserRegistrationView,LoginView,UserProfileView,ChangePasswordView
from django.urls import path

urlpatterns = [
    path('register/',UserRegistrationView.as_view(),name='register'),
    path('login/',LoginView.as_view(),name='login'),
    path('profile/',UserProfileView.as_view(),name='profile'),
    path('changepassword/',ChangePasswordView.as_view(),name='changepassword'),
]
