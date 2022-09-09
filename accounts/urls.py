from django.urls import path, include
from .api.views import EmailLogin, UsernameLogin, SignUp, LogOut

urlpatterns = [
    path("login/email/", EmailLogin.as_view(), name="email-login"),
    path("login/username/", UsernameLogin.as_view(), name="email-login"),
    path("signup/", SignUp.as_view(), name="signup"),
    path("logout/", LogOut.as_view(), name="logout"),
]
