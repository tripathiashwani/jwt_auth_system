from account.views import UserRegistrationView,LoginView,UserProfileView,ChangePasswordView,SendResetPasswordEmailView,UserPasswordResetView

from django.urls import path

urlpatterns = [
    path('register/',UserRegistrationView.as_view(),name='register'),
    path('login/',LoginView.as_view(),name='login'),
    path('profile/',UserProfileView.as_view(),name='profile'),
    path('changepassword/',ChangePasswordView.as_view(),name='changepassword'),
    path('send-reset-password-email/',SendResetPasswordEmailView.as_view(),name='send_reset_password_email'),
    path('reset-password/<uid>/<token>/',UserPasswordResetView.as_view(),name='reset_password'),
]
