from django.urls import path
from api.views import *

# admin@mail.com
# topen+1
urlpatterns = [
    path('login', Login, name = 'post_login: { username:string, password:string }'),
    path('logout', LogoutView.as_view(), name = 'get_logout ? user=[email]'),
    path('reset_password_email', ResetPasswordEmail.as_view(), name = 'post_reset_password_email: { email:string } '),
    path('verify_user_token_email', VerifyUserTokenEmail.as_view(), name = 'post_verify_user_token_email: { token:string }'),
    path('change_password_email', ChangePasswordEmail.as_view(), name = 'post_change_password_email: { token:string, password:string }'),
]
